from copy import deepcopy

import scrapy
from lxml import etree
from scrapy import Selector
from spider_qunaer import items
from warehouse import models

# parent_item.instance.children.add(child_item.instance)

class QunaerSpider(scrapy.Spider):
    name = 'qunaer'
    # allowed_domains = ['travel.qunar.com']
    # 启始
    start_urls = ['https://travel.qunar.com/p-cs300022-changsha-jingdian']
    # 记录页面
    page_num = 1
    models.SpiderLog.objects.create()
    # models.Scenery.objects.all().delete()
    # models.Evaluate.objects.all().delete()

    """
    处理景点页面的信息
    """
    def parse(self, response):
        # 先创建一个景点对象
        item_scenery = items.SpiderSceneryItem()
        # 获取到景点的列表
        scenery_list = response.xpath("//ul[@class='list_item clrfix']/li")
        # 拿到每个景点
        for i in scenery_list:
            # 这里获取景点名称、排名等信息
            item_scenery["scenery_name"] = i.xpath("./div/div/a/span/text()").extract_first()
            item_scenery["rank"] = i.xpath("./div/div/div/span[2]/span/text()").extract_first()
            item_scenery["people_percent"] = i.xpath("./div/div[2]/span/span/text()").extract_first()
            # 删除原来的数据
            scenery = models.Scenery.objects.filter(scenery_name=item_scenery["scenery_name"]).first()
            if scenery:
                scenery.evaluates.all().delete()
                scenery.delete()
            # 拿到详情页的链接
            detail_url = i.xpath("./a/@href").extract_first()
            if not models.Scenery.objects.filter(scenery_name=item_scenery["scenery_name"]).first():
                # 这里对详情页发起请求，结果会传到get_detail()
                yield scrapy.Request(detail_url, callback=self.get_detail, encoding="utf-8",dont_filter=True ,
                                     meta={"item_scenery": deepcopy(item_scenery)})

        # 下一页，总共爬取100页
        if self.page_num < 100:
            self.page_num += 1
            yield scrapy.Request(url=f"{self.start_urls[0]}-1-{self.page_num}", callback=self.parse)

    """处理详情页的信息"""
    def get_detail(self, response):
        # 拿到景点的详细信息
        item_scenery = response.meta["item_scenery"]
        score = response.xpath('//*[@id="js_mainleft"]/div[4]/div/div[2]/div[1]/div[1]/span[1]/text()').extract_first()
        if score:
            try:
                item_scenery["score"] = float(score)
            except Exception as e:
                print(f"score err{score}")
                item_scenery["score"] = 0
        else:
            item_scenery["score"] = 0
        play_time = response.xpath('//div[@class="time"]/text()').extract_first()
        if play_time:
            item_scenery["play_time"] = play_time.split("：")[1]
        else:
            item_scenery["play_time"] = None
        city = response.xpath('//td[@class="td_l"]/dl[1]/dd/span/text()').extract_first()
        print(f"city:{city}")
        item_scenery["city"] = city

        # 这里提交，数据会到pipelines处理
        yield item_scenery
        # item_scenery.save()

        # 第一页评论
        self.get_evalute(response)
        i = 0
        # 第2-5页评论
        for path in response.xpath("//div[@class='b_paging']/a"):
            if i >= 4:
                break
            evalute_path = path.xpath("./@href").extract_first()
            i += 1
            print("evalute_path:", evalute_path)
            yield scrapy.Request(evalute_path, callback=self.get_evalute, encoding="utf-8", dont_filter=True,
                                 meta={"item_scenery": deepcopy(item_scenery)})


    def get_evalute(self, response):
        """
        处理评论数据
        """
        item_scenery = response.meta["item_scenery"]
        evalute_list = response.xpath("//ul[@id='comment_box']/li")
        if not evalute_list:
            return None
        for evalute in evalute_list:
            # 创建评论类，获取到评论的信息
            item_evalute = items.SpiderEvaluteItem()
            item_evalute["content"] = evalute.xpath("./div[1]/div[1]/div[@class='e_comment_content']").xpath('string(.)').extract()[0].replace("阅读全部", "").replace("\n","").replace("\r", "")  # 内容
            item_evalute['send_time'] = evalute.xpath("./div[1]/div[1]/div[5]/ul/li[1]/text()").extract_first()  # 评论时间
            item_evalute['user_name'] = evalute.xpath("./div[2]/div[2]/a/text()").extract_first()  # 用户名
            score = evalute.xpath("./div[1]/div[1]/div[2]/span/span/@class").extract_first()
            if score:
                score = score.split("star_")[-1]
            if score:
                item_evalute['score'] = score   # 评分
            else:
                item_evalute['score'] = 0
            item_evalute['scenery_name'] = item_scenery['scenery_name']  # 景点名
            # 这里提交，数据会到pipelines处理
            # item_evalute.save()
            yield item_evalute
            item_scenery.instance.evaluates.add(item_evalute.instance)
        # yield item_scenery
