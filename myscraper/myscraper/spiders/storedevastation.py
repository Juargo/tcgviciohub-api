import scrapy


class StoreDevastation(scrapy.Spider):
    name = "storedevastation"
    allowed_domains = ["storedevastation.cl"]
    start_urls = ["https://www.storedevastation.com/collections/productos-pokemon-tcg"]

    def parse(self, response):
        products = response.css('.product.Norm')

        for product in products:
            yield{
                'link': product.css('.productLink::attr(href)').get(),
                'img': product.css('img::attr(src)').get(),
                'nombre': product.css('.productTitle::text').get(),
                'stock_label': product.css('.product-block__status::text').get(),
                'precio': product.css('.money::text').get(),
            }
        
        # Siguientes páginas
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

