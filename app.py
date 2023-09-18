"""This module contains the Principal APP API."""

import os
import redis
from flask import Flask, jsonify
from flask_cors import CORS
# from itertools import groupby

app = Flask(__name__)
CORS(app)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASS =  os.getenv("REDIS_PASS")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)

@app.route('/get_products', methods=['GET'])
def get_products():
    """This function gets all products from Redis"""

    # Obtener todas las claves que coincidan con el patrón '*:product:*'
    all_keys = r.keys('*:product:*')
    # Extraer los nombres de las tiendas únicas desde las claves
    product_stores = list(set(key.split(":")[0] for key in all_keys))
    response_data = []

    # Crear un pipeline Redis
    pipeline = r.pipeline()

    # Precargar todos los hgetall en el pipeline
    for store in product_stores:
        i = 1
        while True:
            product_key = f"{store}:product:{i}"
            if product_key in all_keys:
                pipeline.hgetall(product_key)
                i += 1
            else:
                break

    # Ejecutar todos los comandos en el pipeline en una sola ronda
    results = pipeline.execute()

    # Procesar los resultados
    result_index = 0
    for store in product_stores:
        # store_products = []
        i = 1
        while True:
            product_key = f"{store}:product:{i}"
            if product_key in all_keys:
                product_data = results[result_index]
                result_index += 1

                response_data.append({
                    'product_link': product_data.get('product_link', ''),
                    'product_name': product_data.get('product_name', ''),
                    'product_image': product_data.get('product_image', ''),
                    'product_available_label': product_data.get('product_available_label', ''),
                    'product_price': product_data.get('product_price', ''),
                    'store_name':store
                })
                i += 1
            else:
                break
        # response_data.append({store_products})

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)


# def get_products():
#     """This class defines get all products redis"""
#     # Usa SCAN en lugar de KEYS para evitar bloquear el servidor de Redis
#     cursor = '0'
#     all_keys = []
#     while cursor != 0:
#         cursor, keys = r.scan(cursor=cursor, match='*:product:*', count=1000)
#         all_keys.extend(keys)
#     # Ordena y agrupa las claves por tienda
#     sorted_keys = sorted(all_keys, key=lambda x: x.split(":")[0])
#     grouped_keys = groupby(sorted_keys, key=lambda x: x.split(":")[0])
#     response_data = []

#     for store, keys in grouped_keys:
#         store_products = []
#         # Realiza una sola llamada a hgetall para cada grupo de productos de una tienda
#         for product_key in keys:
#             product_data = r.hgetall(product_key)
#             if product_data:
#                 store_products.append({
#                     'product_link': product_data.get('product_link', ''),
#                     'product_name': product_data.get('product_name', ''),
#                     'product_image': product_data.get('product_image', ''),
#                     'product_available_label': product_data.get('product_available_label', ''),
#                     'product_price': product_data.get('product_price', '')
#                 })
#         response_data.append({store: store_products})
#     return jsonify(response_data)
# def get_products():
#     product_stores = ['carduniverse', 'araucaniagaming']
#     response_data = []
#     for store in product_stores:
#         store_products = []
#         i = 1
#         while True:
#             product_key = f"{store}:product:{i}"
#             product_data = r.hgetall(product_key)

#             if not product_data:
#                 break

#             store_products.append({
#                 'product_link': product_data.get('product_link', ''),
#                 'product_name': product_data.get('product_name', ''),
#                 'product_image': product_data.get('product_image', ''),
#                 'product_available_label': product_data.get('product_available_label', ''),
#                 'product_price': product_data.get('product_price', '')
#             })
#             i += 1

#         response_data.append({store: store_products})

#     return jsonify(response_data)

# if __name__ == '__main__':
#     app.run(debug=True)
