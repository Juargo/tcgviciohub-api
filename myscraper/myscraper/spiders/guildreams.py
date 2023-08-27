import scrapy


class Guildreams(scrapy.Spider):
    name = "guildreams"
    allowed_domains = ["guildreams.com"]
    start_urls = ["https://www.guildreams.com/collection/pokemon"]

    def parse(self, response):
        products = response.css('.product-block')

        for product in products:
            yield{
                'link': product.css('a::attr(href)').get(),
                'img': product.css('picture img::attr(data-src)').get(),
                'nombre': product.css('.bs-product-info h2::text').get(),
                'stock_label': product.css('.product-block__status::text').get(),
                'precio': product.css('.bs-product-final-price::text').get(),
            }
        
        # Siguientes páginas
        next_pages = response.css('.pagination >li a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)


# El stock se puede saber del max input