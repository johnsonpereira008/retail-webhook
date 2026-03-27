from flask import Flask, request, jsonify
import random

app = Flask(__name__)
@app.route('/webhook', methods = ['POST'])
def webhook():

    
    req = request.get_json()
    tag = req.get('fulfillmentInfo', {}).get('tag')
    params = req.get('sessionInfo', {}).get('parameters', {})
    brand = params.get('brand')
    category = params.get('product_category')

    if tag == 'product_search':
        if brand:
            response_text = f"Here are some {brand} products: Iphone13, Iphone14"
        elif category:
            response_text = f"Here are some {category} categories: phones, laptops,shoes"
        else:
            response_text = "Here are some popular products"

        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [response_text]
                        }
                    }
                ]
            }
        }
        )
    
    elif tag == 'order_tracking':
        status = random.choice(["Shipped", "Out for Delivery", "Delivered"])
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [f"Your order status is: {status}"]
                        }
                    }
                ]
            }
        }
        )
    return jsonify({
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [f"Webhook received, but the tag was not recognized."]
                        }
                    }
                ]
            }
        }
        )
