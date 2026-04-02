from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    tag = req.get('fulfillmentInfo', {}).get('tag')
    session_params = req.get('sessionInfo', {}).get('parameters', {})

    brand = session_params.get('brand')
    category = session_params.get('product_category')
    selected_product = session_params.get('selected_product')
    cart_items = session_params.get('cart_items', [])

    # 🛍️ PRODUCT SEARCH
    if tag == "product_search":

        if random.choice([True, False]):
            return jsonify({
                "sessionInfo": {
                    "parameters": {
                        "api_failed": True
                    }
                },
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": ["Temporary issue, retrying..."]}}
                    ]
                }
            })

        response_text = f"Here are some products"

        return jsonify({
            "sessionInfo": {
                "parameters": {
                    "api_failed": False
                }
            },
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [response_text]}}
                ]
            }
        })

    # 🛒 ADD TO CART
    elif tag == "add_to_cart":

        if selected_product:
            cart_items.append(selected_product)

        return jsonify({
            "sessionInfo": {
                "parameters": {
                    "cart_items": cart_items
                }
            },
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [f"{selected_product} added to cart"]}}
                ]
            }
        })

    return jsonify({})
