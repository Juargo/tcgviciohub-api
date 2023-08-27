import scrapy


class Geekers(scrapy.Spider):
    name = "geekers"
    allowed_domains = ["geekers.cl"]
    start_urls = ["https://www.geekers.cl/pokemon-tcg"]

    def parse(self, response):
        products = response.css('.product-block')

        for product in products:
            yield{
                'link': product.css('.product-block__caption-info a::attr(href)').get(),
                'img': product.css('img::attr(src)').get(),
                'nombre': product.css('.product-block__name::text').get(),
                'stock_label': product.css('.product-block__status::text').get(),
                'precio': product.css('.product-block__price_value::text').get(),
            }
        
        # Siguientes páginas
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

# El stock se puede saber del max input