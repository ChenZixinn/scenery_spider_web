# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from warehouse.models import Scenery, Evaluate
from scrapy_djangoitem import DjangoItem



class SpiderSceneryItem(DjangoItem):
    django_model = Scenery


class SpiderEvaluteItem(DjangoItem):
    django_model = Evaluate

"""
景点实体类
"""
# class SpiderSceneryItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     # 景点名称，人数百分比，景点排名，评分，建议浏览时间
#     scenery_name = scrapy.Field()
#     people_percent = scrapy.Field()
#     rank = scrapy.Field()
#     score = scrapy.Field()
#     play_time = scrapy.Field()
#     city = scrapy.Field()
#
#
# """
# 评论实体类
# """
# class SpiderEvaluteItem(scrapy.Item):
#     content = scrapy.Field()  # 内容
#     send_time = scrapy.Field()  # 评论时间
#     user_name = scrapy.Field()  # 用户名
#     score = scrapy.Field()  # 评分
#     scenery_name = scrapy.Field()  # 景点id