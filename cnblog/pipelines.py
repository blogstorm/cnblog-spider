# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class MysqlPipeline(object):
    def __init__(self):
        # connection database
        self.connect = pymysql.connect(host='xxx', user='xxx', passwd='xxx',
                                       db='blogstorm')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")

    def process_item(self, item, spider):
        title = item['title'][0]
        url = item['url'][0]
        content = item['content'][0]
        tags = item['tags']
        if tags:
            tags = ','.join(tags)
        else:
            tags = ''
        update_time = item['update_time'][0].split()[0]

        # sql语句
        insert_sql = """
        insert into article(title, url, content, tags, update_time) 
        VALUES (%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d'))
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (title, url, content, tags,
                                         update_time))
        # 提交，不进行提交无法保存到数据库
        self.connect.commit()
        return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.connect.close()



