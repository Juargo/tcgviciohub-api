"""This module contains the Scrapy spider for araucaniagaming.cl."""

import scrapy
from myscraper.items import ProductItem
class WoocommerceSpider(scrapy.Spider):
    """This class defines a Scrapy spider for araucaniagaming.cl."""

    name = "araucaniagaming"
    allowed_domains = ["araucaniagaming.cl"]
    start_urls = ["https://araucaniagaming.cl/productos/jcc-pokemon/"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.products li .product-block')

        for product in products:
            product_item = ProductItem()
            product_available_label= product.css('.stock-label::text').get()
            if product_available_label!='Out Of Stock':
                product_item['product_link']= product.css('.woocommerce-loop-product__title a::attr(href)').get() # pylint: disable=line-too-long
                product_item['product_image']= product.css('img::attr(data-src)').get()
                product_item['product_name']= product.css('.woocommerce-loop-product__title a::text').get() # pylint: disable=line-too-long
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.woocommerce-Price-amount *::text').getall()[1] # pylint: disable=line-too-long
                yield product_item
        # Siguientes páginas
        next_pages = response.css('.page-numbers>li a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)
