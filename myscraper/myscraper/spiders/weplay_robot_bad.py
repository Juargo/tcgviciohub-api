"""This module contains the Scrapy spider for weplay.cl."""

import scrapy
from myscraper.items import ProductItem
class WePlay(scrapy.Spider):
    """This class defines a Scrapy spider for weplay.cl."""

    name = "weplay"
    allowed_domains = ["weplay.cl"]
    start_urls = ["https://www.weplay.cl/juegos-de-mesa-y-cartas/cartas-y-mazos.html?brand_id=2049"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.products li')

        for product in products:
            product_item = ProductItem()
            product_available_label= product.css('.ast-shop-product-out-of-stock::text').get()
            if product_available_label!='Agotado':
                product_item['product_link']= product.css('a::attr(href)').get()
                product_item['product_image']= product.css('img::attr(data-src)').get()
                product_item['product_name']= product.css('.product-item-link::text').get()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.price::text').get()
                yield product_item
        # Siguientes páginas
        next_page = response.css('.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            