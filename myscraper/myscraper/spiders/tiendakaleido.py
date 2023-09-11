"""This module contains the Scrapy spider for tiendakaleido.cl."""

import scrapy
from myscraper.items import ProductItem
class TiendaKaleido(scrapy.Spider):
    """This class defines a Scrapy spider for tiendakaleido.cl."""

    name = "tiendakaleido"
    allowed_domains = ["tiendakaleido.cl"]
    start_urls = ["https://tiendakaleido.cl/categoria-producto/tcg/tcg-pokemon/"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.products li')

        for product in products:
            product_item = ProductItem()
            product_available_label= product.css('.ast-shop-product-out-of-stock::text').get()
            if product_available_label!='Agotado':
                product_item['product_link']= product.css('.astra-shop-thumbnail-wrap a::attr(href)').get() # pylint: disable=line-too-long
                product_item['product_image']= product.css('img::attr(data-srcset)').get()
                product_item['product_name']= product.css('.woocommerce-loop-product__title::text').get() # pylint: disable=line-too-long
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.woocommerce-Price-amount *::text').getall()[1] # pylint: disable=line-too-long
                yield product_item
        # Siguientes páginas
        next_page = response.css('.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            