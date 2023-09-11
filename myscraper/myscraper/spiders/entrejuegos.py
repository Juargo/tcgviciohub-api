"""This module contains the Scrapy spider for entrejuegos.cl."""

import scrapy
from myscraper.items import ProductItem
class EntreJuegos(scrapy.Spider):
    """This class defines a Scrapy spider for entrejuegos.cl."""

    name = "entrejuegos"
    allowed_domains = ["entrejuegos.cl"]
    start_urls = ["https://www.entrejuegos.cl/1072-pokemon"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.js-product')

        for product in products:
            product_item = ProductItem()
            product_available_label=  product.css('.stock-label::text').get()
            if product_available_label!='Agotado':
                product_item['product_link']= product.css('.thumbnail-top a::attr(href)').get()
                product_item['product_image']= product.css('img::attr(src)').get()
                product_item['product_name']= product.css('.product-title a::text').get()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.price::text').get().strip()
                yield product_item
        # Siguientes páginas
        next_pages = response.css('.page-list>li a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)
