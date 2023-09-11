"""This module contains the Scrapy spider for storedevastation.cl."""

import scrapy
from myscraper.items import ProductItem
class StoreDevastation(scrapy.Spider):
    """This class defines a Scrapy spider for storedevastation.cl."""

    name = "storedevastation"
    allowed_domains = ["storedevastation.cl"]
    start_urls = ["https://www.storedevastation.com/collections/productos-pokemon-tcg"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('.product.Norm')

        for product in products:
            product_item = ProductItem()
            product_available_label= product.css('.product-block__status::text').get()
            if product_available_label!='Agotado':
                product_item['product_link']=product.css('.productLink::attr(href)').get()
                product_item['product_image']= product.css('img::attr(src)').get()
                product_item['product_name']= product.css('.productTitle::text').get().strip()
                product_item['product_available_label']= product_available_label
                product_item['product_price']= product.css('.money::text').get()
                yield product_item
        # Siguientes páginas
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        