import scrapy


class EntreJuegos(scrapy.Spider):
    name = "entrejuegos"
    allowed_domains = ["entrejuegos.cl"]
    start_urls = ["https://www.entrejuegos.cl/1072-pokemon"]

    def parse(self, response):
        products = response.css('.js-product')

        for product in products:
            yield{
                'link': product.css('.thumbnail-top a::attr(href)').get(),
                'img': product.css('img::attr(src)').get(),
                'nombre': product.css('.product-title a::text').get(),
                'stock_label': product.css('.stock-label::text').get(),
                'precio': product.css('.price::text').get(),
            }
        
        # Siguientes páginas
        next_pages = response.css('.page-list>li a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)

# El stock se puede saber del max input