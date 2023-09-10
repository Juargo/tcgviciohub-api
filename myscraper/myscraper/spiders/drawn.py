"""This module contains the Scrapy spider for drawn.cl."""

import scrapy
from myscraper.items import ProductItem

class Drawn(scrapy.Spider):
    """This class defines a Scrapy spider for drawn.cl."""

    name = "drawn"
    allowed_domains = ["drawn.cl"]
    start_urls = ["https://drawn.cl/sellado-pokemon-cartas-vaporeon-silver-tempest/"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.product-small .col-inner')

        for product in products:
            product_item = ProductItem()
            product_available_label= product.css('.product-block__status::text').get()
            if product_available_label!='Agotado':
                product_item['product_link']= product.css('a::attr(href)').get()
                product_item['product_image']= product.css('img::attr(src)').get()
                product_item['product_name']= product.css('.product-title a::text').get()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.woocommerce-Price-amount *::text').getall()[1]
            yield product_item
        # Siguientes páginas
        # next_page = response.css('.next::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
# TO-DO: VER CUAL ES LA ETIQUTA PARA AGOTADO Y NEXT
