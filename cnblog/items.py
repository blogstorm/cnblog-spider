import scrapy


class CnblogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义需要保存的字段
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    update_time = scrapy.Field()