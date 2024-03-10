import scrapy
from cnnscrapper.items import CnnscrapperItem


class CnnspiderSpider(scrapy.Spider):
    name = "cnnspider"
    allowed_domains = ["cnn.com"]
    start_urls = ["http://www.cnn.com/HEALTH/archive/index.html"]
    # http://www.cnn.com/HEALTH/archive/index.html

    def parse(self, response):
        articles = response.xpath('.//div[@class="archive-item video cnn_skn_spccovstrylst"]')
        for article in articles:
            cnnitem = CnnscrapperItem()
            cnnitem['title'] = article.xpath('.//h2/a/text()').get()
            cnnitem['subtitle'] = article.xpath('.//p//text()').get()
            cnnitem['date'] = article.xpath('.//h2/span/text()').get().replace('updated ', '')
            link = article.xpath('.//h2/a/@href').get()

            if link is not None:
                yield response.follow(link, callback=self.parse_article, meta = {'item': cnnitem})
            

    def parse_article(self, response):
        texts = response.xpath('.//div[@class="article__content-container"]//p[@class="paragraph inline-placeholder"]/text()').getall()
        text = ''.join(texts)
        item = response.meta.get('item', {})
        if texts:
            item['text'] = text
        else: 
            item['text'] = response.xpath('.//div[@class="media__video-description media__video-description--inline"]/text()').get()
      
        yield item
        # date and subtitle in meta item
