import scrapy


class Playcenter(scrapy.Spider):
    name = "playcenter"
    allowed_domains = ["playcenter.cl"]
    start_urls = ["https://playcenter.cl/etiqueta-producto/pokemon/"]

    def parse(self, response):
        products = response.css('.products li')

        for product in products:
            yield{
                'link': product.css('.astra-shop-thumbnail-wrap a::attr(href)').get(),
                'img': product.css('img::attr(src)').get(),
                'nombre': product.css('.woocommerce-loop-product__title::text').get(),
                'stock_label': product.css('.ast-shop-product-out-of-stock::text').get(),
                'precio': product.css('.woocommerce-Price-amount *::text').getall()[1],
            }
        
        # Siguientes páginas
        next_page = response.css('.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

# El stock se puede saber del max input