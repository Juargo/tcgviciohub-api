"""This module contains the Scrapy spider for dementegames.cl."""

import scrapy
from myscraper.items import ProductItem
class DementeGames(scrapy.Spider):
    """This class defines a Scrapy spider for dementegames.cl."""

    name = "dementegames"
    allowed_domains = ["dementegames.cl"]
    start_urls = ["https://dementegames.cl/74-pokemon-tcg"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('article')

        for product in products:
            product_item = ProductItem()
            product_available_label= product.css('.out-of-stock::text').get()
            if product_available_label!='Agotado':
                product_item['product_link']= product.css('a::attr(href)').get()
                product_item['product_image']= product.css('img::attr(src)').get()
                product_item['product_name']= product.css('.h3 a::text').get()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.price::text').get()
            yield product_item
        # Siguientes páginas
        next_page = response.css('.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
# El stock se puede saber del max input
