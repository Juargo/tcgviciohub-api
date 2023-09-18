# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import redis
import os


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASS =  os.getenv("REDIS_PASS")

class MyscraperPipeline:
    def process_item(self, item, spider):
        return item

class PriceNormalizationPipeline:

    def process_item(self, item, spider):
        raw_price = item.get('product_price', '')

        if raw_price:
            # Eliminar todos los caracteres no numéricos, excepto el punto
            normalized_price = re.sub(r'[^0-9.]', '', raw_price)
            
            # Eliminar los puntos, ya que son separadores de miles
            normalized_price = normalized_price.replace('.', '')

            # Convertir a entero
            try:
                normalized_price = int(normalized_price)
            except ValueError:
                normalized_price = None  # or set to some default value

            # Actualizar el precio en el item
            item['product_price'] = normalized_price

        return item

class RedisPipeline:
    def open_spider(self, spider):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS)

    def process_item(self, item, spider):
        store_name = spider.name

        # Obtén el siguiente ID único para la tienda
        unique_id = self.redis_client.incr(f"{store_name}:product_id_counter")

        key = f"{store_name}:product:{unique_id}"
        fields = {
            'product_link': item['product_link'],
            'product_image': item['product_image'],
            'product_name': item['product_name'],
            'product_available_label': item['product_available_label'],
            'product_price': item['product_price'],
        }

        cleaned_fields = {k: (v if v is not None else "null") for k, v in item.items()}
        self.redis_client.hset(key, mapping=cleaned_fields)

        return item