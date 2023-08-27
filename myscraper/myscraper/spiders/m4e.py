import scrapy


class M4e(scrapy.Spider):
    name = "m4e"
    allowed_domains = ["m4e.cl"]
    start_urls = ["https://www.m4e.cl/juegos-de-cartas/pokemon"]

    def parse(self, response):
        products = response.css('.product-block')

        for product in products:
            yield{
                'link': product.css('a::attr(href)').get(),
                'img': product.css('img::attr(src)').get(),
                'nombre': product.css('h3 a::text').get(),
                'stock_label': product.css('.quick-view a::text').get(),
                'precio': product.css('.block-price::text').get(),
            }
        
        # Siguientes páginas
        next_page = response.css('a.square-button:nth-of-type(2)::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

# El stock se puede saber del max input