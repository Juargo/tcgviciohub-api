import scrapy


class ShopifySpider(scrapy.Spider):
    name = "shopify"
    allowed_domains = ['carduniverse.cl']
    start_urls = ["https://carduniverse.cl/collections/pokemon-tcg"]
    

    def parse(self, response):
        for product in response.css('a.product-card'):
            # Extraer la URL del producto
            product_link = response.urljoin(product.css('::attr(href)').get())
            
            # Extraer la URL de la imagen
            image_url = product.css('img.lazyload::attr(data-src)').get()
            if image_url and image_url.startswith('//'):
                image_url = 'https:' + image_url.replace('{width}', '720')

            # Extraer el nombre del producto
            product_name = product.css('div.product-card__name::text').get().strip()

            # Extraer la disponibilidad del producto
            availability = 'Agotado' if product.css('div.product-card__availability::text').get() == 'Agotado' else 'Disponible'

            # Extraer el precio del producto
            price = product.css('div.product-card__price span.money::text').get()
            
            # Empaquetar todo en un diccionario y enviarlo
            yield {
                'link': product_link,
                'image': image_url,
                'name': product_name,
                'availability': availability,
                'price': price
            }

        # Paginación: Encuentra el enlace a la siguiente página y sigue
        next_page = response.css('div.pagination span.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
