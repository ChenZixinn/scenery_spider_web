# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pandas as pd
import pymysql
from sqlalchemy import create_engine, NVARCHAR, VARCHAR, TEXT, DATETIME, FLOAT, INTEGER
from itemadapter import ItemAdapter
from spider_qunaer.items import *
from warehouse.models import Scenery, Evaluate


class SpiderQunaerPipeline(object):
    def process_item(self, item, spider):
        item.save()
        # print(f"保存：{item}")
        return item