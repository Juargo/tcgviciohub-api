import scrapy


class Drawn(scrapy.Spider):
    name = "drawn"
    allowed_domains = ["drawn.cl"]
    start_urls = ["https://drawn.cl/sellado-pokemon-cartas-vaporeon-silver-tempest/"]

    def parse(self, response):
        products = response.css('.product-small .col-inner')

        for product in products:
            yield{
                'link': product.css('a::attr(href)').get(),
                'img': product.css('img::attr(src)').get(),
                'nombre': product.css('.product-title a::text').get(),
                'stock_label': product.css('.product-block__status::text').get(),
                'precio':  product.css('.woocommerce-Price-amount *::text').getall()[1],
            }
        
        # Siguientes páginas
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)

# El stock se puede saber del max input