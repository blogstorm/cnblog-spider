# -*- coding: utf-8 -*-
import scrapy
from cnblog.items import CnblogItem
import copy


class CnblogSpiderSpider(scrapy.Spider):
    name = "cnblog_spider"
    allowed_domains = ["cnblogs.com"]
    url = 'https://www.cnblogs.com/sitehome/p/'
    offset = 1
    start_urls = [url+str(offset)]

    def parse(self, response):

        # 获取当前页面的所有博文链接
        urls = response.xpath('//a[@class="titlelnk"]/@href').extract()
        # 爬取当前页面的所有博文链接的内容
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_content)

        print("第{0}页爬取完成".format(self.offset))
        if self.offset < 200:        #爬取到第几页
            self.offset += 1
        url2 = self.url+str(self.offset)    #拼接url
        yield scrapy.Request(url=url2, callback=self.parse)

    def parse_content(self, response):

        item = CnblogItem()
        # 正文
        item['content'] = response.xpath('//div[@id="cnblogs_post_body"]').extract()
        # 标题
        item['title'] = response.xpath('//a[@id="cb_post_title_url"]/text()').extract()
        # url
        item['url'] = response.xpath('//a[@id="cb_post_title_url"]/@href').extract()
        # 发布时间
        item['update_time'] = response.xpath('//span[@id="post-date"]/text()').extract()
        # blogid ，用于获取分类和tag
        blogid = response.xpath('//script').re(r'currentBlogId = (\d[0-9])')[0]
        url = item['url'][0]
        # 构造获取分类的url
        category_url = url[:url.index('/', 24)] + \
                       '/ajax/CategoriesTags.aspx?blogId=' + \
            blogid + '&postId=' + url[url.index('/', 24)+3:-5]
        # 获取分类
        yield scrapy.Request(url=category_url, meta=copy.deepcopy({'item': item}), callback=self.parse_category)

    def parse_category(self, response):
        item = response.meta['item']
        # 解析分类或标签
        item['tags'] = response.xpath('//div[@id="BlogPostCategory"]/a/text()').extract() + response.xpath('//div[@id="EntryTag"]/a/text()').extract()
        yield item
