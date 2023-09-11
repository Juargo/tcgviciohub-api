"""This module contains the Scrapy spider for magicsur.cl."""

import scrapy
from myscraper.items import ProductItem
class MagicSur(scrapy.Spider):
    """This class defines a Scrapy spider for magicsur.cl."""

    name = "magicsur"
    allowed_domains = ["magicsur.cl"]
    start_urls = ["https://www.magicsur.cl/14-pokemon-tcg"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.js-product-miniature-wrapper')

        for product in products:
            product_item = ProductItem()
            product_available_label= product.css('.product-block__status::text').get()
            if product_available_label!='Agotado':
                product_item['product_link']= product.css('a::attr(href)').get()
                product_item['product_image']= product.css('img::attr(data-src)').get()
                product_item['product_name']=  product.css('.product-title a::text').get()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.product-price::text').get()
                yield product_item
        # Siguientes páginas
        # next_page = response.css('.next::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
        