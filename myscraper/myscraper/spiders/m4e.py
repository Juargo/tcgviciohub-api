"""This module contains the Scrapy spider for m4e.cl."""

import scrapy
from myscraper.items import ProductItem
class M4e(scrapy.Spider):
    """This class defines a Scrapy spider for m4e.cl."""

    name = "m4e"
    allowed_domains = ["m4e.cl"]
    start_urls = ["https://www.m4e.cl/juegos-de-cartas/pokemon"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.product-block')

        for product in products:
            product_item = ProductItem()
            product_available_label= product.css('.quick-view a::text').get()
            if product_available_label!='Agotado':
                relative_url = product.css('a::attr(href)').get()
                product_url = 'https://www.m4e.cl' + relative_url
                product_item['product_link']= product_url
                product_item['product_image']= product.css('img::attr(src)').get()
                product_item['product_name']= product.css('h3 a::text').get()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.block-price::text').get()
                yield product_item
        # Siguientes páginas
        next_page = response.css('a.square-button:nth-of-type(2)::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
