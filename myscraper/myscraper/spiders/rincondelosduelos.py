import scrapy


class ElRinconDeLosDuelos(scrapy.Spider):
    name = "elRinconDeLosDuelos"
    allowed_domains = ["elreinodelosduelos.cl"]
    start_urls = ["https://elreinodelosduelos.cl/categoria-producto/pokemon-tcg/"]

    def parse(self, response):
        products = response.css('.product-grid-item')

        for product in products:
            yield{
                'link': product.css('a::attr(href)').get(),
                'img': product.css('img::attr(src)').get(),
                'nombre': product.css('a::text').get(),
                'stock_label': product.css('.stock-label::text').get(),
                'precio': product.css('.woocommerce-Price-amount *::text').getall()[1],
            }
        
        # Siguientes páginas
        next_pages = response.css('.page-numbers>li a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                yield response.follow(next_page, self.parse)

# El stock se puede saber del max input