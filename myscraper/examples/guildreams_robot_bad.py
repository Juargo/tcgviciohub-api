"""This module contains the Scrapy spider for guildreams.cl."""

import scrapy
from myscraper.items import ProductItem
class Guildreams(scrapy.Spider):
    """This class defines a Scrapy spider for guildreams.cl."""

    name = "guildreams"
    allowed_domains = ["guildreams.com"]
    start_urls = ["https://www.guildreams.com/collection/pokemon"]


    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.product-block')

        for product in products:
            product_item = ProductItem()
            product_available_label= product.css('.product-block__status::text').get()
            if product_available_label!='Agotado':
                product_item['product_link']= product.css('a::attr(href)').get()
                product_item['product_image']= product.css('picture img::attr(data-src)').get()
                product_item['product_name']= product.css('.bs-product-info h2::text').get()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.bs-product-final-price::text').get()
                yield product_item
         # Siguientes páginas
        next_pages = response.css('.pagination >li a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)
                