from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASS =  os.getenv("REDIS_PASS")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)

@app.route('/get_products', methods=['GET'])
def get_products():
    # Utiliza el comando KEYS para encontrar todas las keys que coinciden con el patrón "*:product:*"
    all_keys = r.keys('*:product:*')
    
    # Extrae los nombres de las tiendas únicas desde las keys
    product_stores = list(set(key.split(":")[0] for key in all_keys))
    
    response_data = []

    for store in product_stores:
        store_products = []
        i = 1
        while True:
            product_key = f"{store}:product:{i}"
            product_data = r.hgetall(product_key)
            
            if not product_data:
                break

            store_products.append({
                'product_link': product_data.get('product_link', ''),
                'product_name': product_data.get('product_name', ''),
                'product_image': product_data.get('product_image', ''),
                'product_available_label': product_data.get('product_available_label', ''),
                'product_price': product_data.get('product_price', '')
            })
            i += 1

        response_data.append({store: store_products})

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)

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

