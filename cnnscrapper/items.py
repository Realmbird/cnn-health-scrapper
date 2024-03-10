# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CnnscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 'title''subtitle''date''link' 'text'
    title = scrapy.Field()
    subtitle = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
