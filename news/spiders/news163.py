import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from news.items import NewsItem


# https://news.163.com/20/1123/08/FS3T3D4G000189FH.html
# https://dy.163.com/article/FS2VIFFJ05504DP0.html
# https://dy.163.com/article/FS31UR6U0519QIKK.html
# https://news.163.com/20/1123/\d+/.*.html
class News163Spider(CrawlSpider):
    name = 'news163'
    allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com/']

    rules = (
        Rule(LinkExtractor(allow=r'https://news.163.com/20/1123/\d+/.*.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = NewsItem()
        item['news_thread'] = response.url.strip().split('/')[-1][:-5]
        self.get_title(response, item)
        self.get_time(response, item)
        self.get_source(response, item)
        self.get_text(response, item)
        self.get_url(response, item)
        return item

    def get_title(self, response, item):
        title = response.css('title::text').extract()[0]
        if title:
            print('title: {}'.format(title))
            item['news_title'] = title

    def get_time(self, response, item):
        time = response.css('div.post_time_source::text').extract()[0]
        time = time.strip().replace('来源:', '').replace('\u3000', '')
        if time:
            print(('time: {}').format(time))
            item['news_time'] = time

    def get_source(self, response, item):
        source_name = response.css('#ne_article_source::text').extract()[0]
        if source_name:
            print('source: {}'.format(source_name))
            item['news_source'] = source_name
        source_url = response.css('#ne_article_source::attr(href)').extract()[0]
        if source_url:
            print('source_url: {}'.format(source_url))
            item['source_url'] = source_url

    def get_text(self, response, item):
        news_body = response.css('div#endText p::text').extract()
        if news_body:
            item['news_body'] = news_body

    def get_url(self, response, item):
        url = response.url
        if url:
            item['news_url'] = url
