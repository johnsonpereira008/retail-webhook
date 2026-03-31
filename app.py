from flask import Flask, request, jsonify
import random   # 👈 THIS LINE goes at the TOP

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Get tag from Dialogflow
    tag = req['fulfillmentInfo']['tag']

    # Get parameters (brand, category)
    session_params = req.get('sessionInfo', {}).get('parameters', {})
    brand = session_params.get('brand')
    category = session_params.get('product_category')

    # 🔥 PRODUCT SEARCH LOGIC WITH FAILURE SIMULATION
    if tag == "product_search":

        # Simulate failure randomly
        if True:
            return jsonify({
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": ["Sorry, we are unable to fetch products right now. Please try again."]}}
                    ]
                }
            })

        # If API works
        if brand:
            response_text = f"Here are some {brand} products: iPhone 13, iPhone 14"
        elif category:
            response_text = f"Here are some {category}: phones, laptops, shoes"
        else:
            response_text = "Here are some popular products"

        return jsonify({
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
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [f"Your order status is: {status}"]}}
                ]
            }
        })

    return jsonify({})
