### 1、项目介绍

本项目Scrapy进行数据爬取，并使用Django框架+PyEcharts实现可视化大屏。效果如下：
![image-20230612133737420](/Users/chenzixin/Library/Mobile Documents/com~apple~CloudDocs/Documents/Code/python/scenery_spider_web/README.assets/image-20230612133737420.png)

![f280a159-35f3-4d8a-bcef-012dd20dd279](/Users/chenzixin/Library/Mobile Documents/com~apple~CloudDocs/Documents/Code/python/scenery_spider_web/README.assets/f280a159-35f3-4d8a-bcef-012dd20dd279.png)

![91c6e606-349a-498f-9e9a-6e5b0ea3f3b4](/Users/chenzixin/Library/Mobile Documents/com~apple~CloudDocs/Documents/Code/python/scenery_spider_web/README.assets/91c6e606-349a-498f-9e9a-6e5b0ea3f3b4.png)

每个模块都有详情页，可以通过点击首页各个模块的标签，进行访问。

基于数据可视化的游客行为分析系统，包含以下几类图表：

- 景点数量各区县分布地图
- 景点数量各区县分布图
- 景点评分分布图
- 景点浏览时间分布图
- 景点评论词云图
- 景点浏览人数占比分析
- 景点人数占比分析
- 景点评分数据排名

还有登录注册界面，可以自己注册账号。

### 2、python库安装

本项目使用的python环境是3.8，Django4.0。（建议3.8及以上，不然可能装不了Django4）

**这里以conda环境为例：**

```shell
# 创建虚拟环境
conda create --name py38 python=3.8.13
 
# 激活环境
conda activate py38

# 安装库
pip install -i https://pypi.douban.com/simple -r requirements.txt
```



### 3、MySQL部署

#### 3.1、创建库

```shell
# 创建数据库
create database hunan_web;
 
# 使用数据库
use hunan_web;
```



#### 3.2、创建表

sql文件存在了部分数据，可以直接使用。（请检查路径，确保能访问到这个文件。）

```shell
# 导入数据
source ./data_bak/hunan_web_2023-05-12.sql
```



#### 3.3、设置数据库信息

在 [settings.py](hunan_web/settings.py)文件中修改数据库连接信息

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
        "NAME": "hunan_web",
        "USER": "用户名",
        "PASSWORD": "密码",
        "HOST": "127.0.0.1",
        "POST": 3306
    }
}
```



### 4、爬虫运行

##### 进行增量爬取

```shell
# 启动scrapy爬虫
scrapy crawl qunaer
```



运行可能会有问题，使用以下方法解决

```shell
# ImportError: cannot import name 'SSLv3_METHOD' from 'OpenSSL.SSL'
pip3 install pyopenssl==22.0.0
 
# AttributeError: module 'lib' has no attribute 'OpenSSL_add_all_algorithms'
pip3 install cryptography==38.0.4
```



如果上面的方法也不能解决，就把scrapy库升级到最新版本。

```python
# 升级
pip install --upgrade scrapy
```



### 5、web运行

启动后根据提示访问链接即可。

```python
# 运行web，默认8000端口
python manage.py runserver
```



### 其他

看到很多小伙伴star了，感谢你们喜欢这个项目。如果遇到问题可以提交issue给我一起改进这个项目吧。

也看到了很多小伙伴转载到其他平台了，希望可以注明出处让更多人看到，谢谢你们。
