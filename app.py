from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    
    tag = req['fulfillmentInfo']['tag']

    if tag == "product_search":
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": ["Here are products: iPhone 13 - ₹60,000, Samsung S22 - ₹55,000"]}}
                ]
            }
        })

    elif tag == "order_tracking":
        status = random.choice(["Shipped", "Out for delivery", "Delivered"])
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [f"Your order status is: {status}"]}}
                ]
            }
        })

    return jsonify({})