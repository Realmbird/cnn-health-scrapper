import scrapy
from cnnscrapper.items import CnnscrapperItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait


class CnnspiderSpider(scrapy.Spider):
    name = "cnnspider"
    # allowed_domains = ["cnn.com"]
    # start_urls = ["http://www.cnn.com/HEALTH/archive/index.html"]
    # http://www.cnn.com/HEALTH/archive/index.html
    # url = 'http://www.cnn.com/HEALTH/archive/index.html'
	# yield SeleniumRequest(url=url, callback=self.parse)
    def start_requests(self):
        url = 'http://www.cnn.com/HEALTH/archive/index.html'
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)


    def parse(self, response):
        # Your existing code to process articles
        driver = response.meta['driver']

        articles = response.xpath('.//div[@class="archive-item video cnn_skn_spccovstrylst"]')
        for article in articles:
            cnnitem = CnnscrapperItem()
            cnnitem['title'] = article.xpath('.//h2/a/text()').get()
            cnnitem['subtitle'] = article.xpath('.//p//text()').get()
            cnnitem['date'] = article.xpath('.//h2/span/text()').get().replace('updated ', '')
            link = article.xpath('.//h2/a/@href').get()

            if link is not None:
                yield response.follow(link, callback=self.parse_article, meta = {'item': cnnitem})
        #add next page or script code here
        # Try to click the next page button and then process articles again
        try:
            next_page_button = driver.find_element(By.CSS_SELECTOR, '.next')
            next_page_button.click()
            
            # Wait for the next set of articles to load dynamically
            WebDriverWait(driver, 10)

            # After the next set of articles has loaded, call parse method again to process these articles
            # Since it's the same page (URL not changed), directly use Selenium to scrape without a new request
            self.parse(response)
        except Exception as e:
            self.logger.info(f'No more pages to load or error: {e}')


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
