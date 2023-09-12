# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


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