from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Get tag
    tag = req['fulfillmentInfo']['tag']

    # Get parameters
    session_params = req.get('sessionInfo', {}).get('parameters', {})
    brand = session_params.get('brand')
    category = session_params.get('product_category')

    # 🛍️ PRODUCT SEARCH
    if tag == "product_search":

        # 🔥 Simulate failure
        if random.choice([True, False]):
            return jsonify({
                "sessionInfo": {
                    "parameters": {
                        "api_failed": True   # 👈 VERY IMPORTANT
                    }
                },
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": ["Temporary issue, retrying..."]}}
                    ]
                }
            })

        # ✅ Success case
        if brand:
            response_text = f"Here are some {brand} products"
        elif category:
            response_text = f"Here are some {category}"
        else:
            response_text = "Here are some popular products"

        return jsonify({
            "sessionInfo": {
                "parameters": {
                    "api_failed": False   # 👈 RESET FLAG
                }
            },
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [response_text]}}
                ]
            }
        })

    # 🚚 ORDER TRACKING
    elif tag == "order_tracking":
        status = random.choice(["Shipped", "Out for delivery", "Delivered"])
        return jsonify({
            "sessionInfo": {
                "parameters": {
                    "api_failed": False
                }
            },
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [f"Your order status is: {status}"]}}
                ]
            }
        })
    elif tag == "add_to_cart":
    product = session_params.get("selected_product", "item")

    return jsonify({
        "sessionInfo": {
            "parameters": {
                "cart_items": [product]
            }
        },
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [f"{product} added to cart"]}}
            ]
        }
    })

    return jsonify({})
