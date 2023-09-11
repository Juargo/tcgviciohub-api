"""This module contains the Scrapy spider for lafortalezapuq.cl."""

import scrapy
from myscraper.items import ProductItem
class LaFortaleza(scrapy.Spider):
    """This class defines a Scrapy spider for lafortalezapuq.cl."""

    name = "lafortalezapuq"
    allowed_domains = ["lafortalezapuq.cl"]
    start_urls = ["https://www.lafortalezapuq.cl/tcg/pok"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.shop')

        for product in products:
            product_item = ProductItem()
            product_available_label=  product.css('.product-out-of-stock::text').get()
            if product_available_label!='Agotado':
                relative_url = product.css('a::attr(href)').get()
                product_url = 'https://www.lafortalezapuq.cl' + relative_url
                product_item['product_link']= product_url
                product_item['product_image']= product.css('img::attr(src)').get()
                product_item['product_name']= product.css('section h5::text').get()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.product-price::text').get().strip()
                yield product_item
        # Siguientes páginas
        next_page = response.css('.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            