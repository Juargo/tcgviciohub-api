import scrapy


class LaFortaleza(scrapy.Spider):
    name = "lafortalezapuq"
    allowed_domains = ["lafortalezapuq.cl"]
    start_urls = ["https://www.lafortalezapuq.cl/tcg/pok"]

    def parse(self, response):
        products = response.css('.shop')

        for product in products:
            yield{
                'link': product.css('a::attr(href)').get(),
                'img': product.css('img::attr(src)').get(),
                'nombre': product.css('section h5::text').get(),
                'stock_label': product.css('.product-out-of-stock::text').get(),
                'precio': product.css('.product-price::text').get(),
            }
        
        # Siguientes páginas
        next_page = response.css('.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

# El stock se puede saber del max input