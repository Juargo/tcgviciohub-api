import scrapy


class WePlay(scrapy.Spider):
    name = "weplay"
    allowed_domains = ["weplay.cl"]
    start_urls = ["https://www.weplay.cl/juegos-de-mesa-y-cartas/cartas-y-mazos.html?brand_id=2049"]

    def parse(self, response):
        products = response.css('.products li')

        for product in products:
            yield{
                'link': product.css('a::attr(href)').get(),
                'img': product.css('img::attr(data-src)').get(),
                'nombre': product.css('.product-item-link::text').get(),
                'stock_label': product.css('.ast-shop-product-out-of-stock::text').get(),
                'precio': product.css('.price::text').get(),
            }
        
        # Siguientes páginas
        next_page = response.css('.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)