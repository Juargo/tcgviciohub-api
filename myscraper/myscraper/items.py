# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    product_link = scrapy.Field()
    product_image = scrapy.Field()
    product_name = scrapy.Field()
    product_available_label = scrapy.Field()
    product_price = scrapy.Field()
    # product_stock_number = scrapy.Field()
    # product_expansion
    # product_idioma
