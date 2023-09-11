"""This module contains the Scrapy spider for geekers.cl."""

import scrapy
from myscraper.items import ProductItem
class Geekers(scrapy.Spider):
    """This class defines a Scrapy spider for geekers.cl."""

    name = "geekers"
    allowed_domains = ["geekers.cl"]
    start_urls = ["https://www.geekers.cl/pokemon-tcg"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.product-block')

        for product in products:
            product_item = ProductItem()
            product_available_label=  product.css('.product-block__status::text').get()
            if product_available_label!='Agotado' and product_available_label!='No disponible' :
                product_item['product_link']= product.css('.product-block__caption-info a::attr(href)').get() # pylint: disable=line-too-long
                product_item['product_image']= product.css('img::attr(src)').get()
                product_item['product_name']= product.css('.product-block__name::text').get()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.product-block__price_value::text').get() # pylint: disable=line-too-long
                yield product_item
        # Siguientes páginas
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
