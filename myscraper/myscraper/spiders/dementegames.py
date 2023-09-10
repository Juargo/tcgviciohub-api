import scrapy


class DementeGames(scrapy.Spider):
    name = "dementegames"
    allowed_domains = ["dementegames.cl"]
    start_urls = ["https://dementegames.cl/74-pokemon-tcg"]

    def parse(self, response):
        products = response.css('article')

        for product in products:
            yield{
                'link': product.css('a::attr(href)').get(),
                'img': product.css('img::attr(src)').get(),
                'nombre': product.css('.h3 a::text').get(),
                'stock_label': product.css('.out-of-stock::text').get(),
                'precio': product.css('.price::text').get(),
            }
        
        # Siguientes páginas
        next_page = response.css('.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

# El stock se puede saber del max input