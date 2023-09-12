"""This module contains the Scrapy spider for carduniverse.cl."""

import scrapy
from myscraper.items import ProductItem
class Carduniverse(scrapy.Spider):
    """This class defines a Scrapy spider for carduniverse.cl."""

    name = "carduniverse"
    allowed_domains = ['carduniverse.cl']
    start_urls = ["https://carduniverse.cl/collections/pokemon-tcg"]

    # pylint: disable=arguments-differ
    def parse(self, response):
        products = response.css('a.product-card')

        for product in products:
            product_item = ProductItem()
            raw_label = product.css('div.product-card__availability::text').get()
            product_available_label=''
            if raw_label is not None:
                product_available_label = raw_label.strip()
            if product_available_label!='Agotado':
                relative_url = product.css('::attr(href)').get()
                product_url = 'https://carduniverse.cl' + relative_url
                product_item['product_link']= product_url
                image_url = product.css('img.lazyload::attr(data-src)').get()
                if image_url and image_url.startswith('//'):
                    image_url = 'https:' + image_url.replace('{width}', '720')
                product_item['product_image']= image_url
                product_item['product_name']= product.css('div.product-card__name::text').get().strip() # pylint: disable=line-too-long
                product_item['product_available_label']= product_available_label
                # Obtener el precio
                regular_price = product.css('s.product-card__regular-price span.money::text').get()
                sale_price = product.css('div.product-card__price span.money:last-child::text').get()

                if sale_price:
                    product_item['product_price'] = sale_price
                else:
                    product_item['product_price'] = regular_price
                yield product_item
        # Paginación: Encuentra el enlace a la siguiente página y sigue
        next_page = response.css('div.pagination span.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
