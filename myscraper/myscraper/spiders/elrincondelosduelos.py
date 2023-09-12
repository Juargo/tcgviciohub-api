"""This module contains the Scrapy spider for elreinodelosduelos.cl."""

import scrapy
from myscraper.items import ProductItem
class ElRinconDeLosDuelos(scrapy.Spider):
    """This class defines a Scrapy spider for elreinodelosduelos.cl."""

    name = "elRinconDeLosDuelos"
    allowed_domains = ["elreinodelosduelos.cl"]
    start_urls = ["https://elreinodelosduelos.cl/categoria-producto/pokemon-tcg/"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.product-grid-item')

        for product in products:
            product_item = ProductItem()
            product_available_label= product.css('.stock-label::text').get()
            if product_available_label!='Agotado':
                product_item['product_link']= product.css('a::attr(href)').get()
                product_item['product_image']= product.css('img::attr(src)').get()
                product_item['product_name']= product.css('.wd-entities-title a::text').get()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.woocommerce-Price-amount *::text').getall()[1] # pylint: disable=line-too-long
                yield product_item
        # Siguientes páginas
        next_pages = response.css('.page-numbers>li a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)
