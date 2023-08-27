import scrapy


class MagicSur(scrapy.Spider):
    name = "magicsur"
    allowed_domains = ["magicsur.cl"]
    start_urls = ["https://www.magicsur.cl/14-pokemon-tcg"]

    def parse(self, response):
        products = response.css('.js-product-miniature-wrapper')

        for product in products:
            yield{
                'link': product.css('a::attr(href)').get(),
                'img': product.css('img::attr(data-src)').get(),
                'nombre': product.css('.product-title a::text').get(),
                'stock_label': product.css('.product-block__status::text').get(),
                'precio': product.css('.product-price::text').get(),
            }
        
        # Siguientes páginas
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)

# El stock se puede saber del max input