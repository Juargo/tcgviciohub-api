import scrapy


class WoocommerceSpider(scrapy.Spider):
    name = "wooCommerce"
    allowed_domains = ["araucaniagaming.cl"]
    start_urls = ["https://araucaniagaming.cl/productos/jcc-pokemon/"]

    def parse(self, response):
        products = response.css('.products li .product-block')

        for product in products:
            yield{
                'link': product.css('.woocommerce-loop-product__title a::attr(href)').get(),
                'img': product.css('img::attr(data-src)').get(),
                'nombre': product.css('.woocommerce-loop-product__title a::text').get(),
                'stock_label': product.css('.stock-label::text').get(),
                'precio': product.css('.woocommerce-Price-amount *::text').getall()[1],
            }
        
        # Siguientes páginas
        next_pages = response.css('.page-numbers>li a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)
