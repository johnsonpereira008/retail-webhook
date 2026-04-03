from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    tag = req.get('fulfillmentInfo', {}).get('tag')
    session_params = req.get('sessionInfo', {}).get('parameters', {})

    selected_product = session_params.get('selected_product')
    remove_product = session_params.get('remove_product')
    cart_items = session_params.get('cart_items', [])
    intent = req.get('intentInfo', {}).get('displayName')

    # -------------------------------
    # PRODUCT SEARCH
    # -------------------------------
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

        return jsonify({
            "sessionInfo": {
                "parameters": {
                    "api_failed": False
                }
            },
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": ["Here are some products"]}}
                ]
            }
        })

    # -------------------------------
    # CART HANDLER (ALL ACTIONS)
    # -------------------------------
    elif tag == "cart_handler":

        message = ""

        # ADD

        cart_action = session_params.get('cart_action')

        if intent == "select.product" or intent == "cart.add" or cart_action == "add":
            if selected_product:
                cart_items.append(selected_product)

        # Build cart view
                items = "\n".join([f"{i+1}. {item}" for i, item in enumerate(cart_items)])

                message = f"{selected_product} added to cart\n\nYour cart contains:\n{items}"
        
        # REMOVE
        elif intent == "cart.remove":
            if remove_product in cart_items:
                cart_items.remove(remove_product)
                message = f"{remove_product} removed from cart"
            else:
                message = "Item not found in cart"

        # CLEAR
        elif intent == "cart.clear":
            cart_items = []
            message = "Your cart is now empty"

        # VIEW
        elif intent == "cart.view":
            if not cart_items:
                message = "Your cart is empty"
            else:
                items = "\n".join([f"{i+1}. {item}" for i, item in enumerate(cart_items)])
                message = f"Your cart contains:\n{items}"

        # DEFAULT FALLBACK
        if not message:
            if cart_items:
                items = "\n".join([f"{i+1}. {item}" for i, item in enumerate(cart_items)])
                message = f"Your cart contains:\n{items}"
            else:
                message = "Your cart is empty"

        return jsonify({
            "sessionInfo": {
                "parameters": {
                    "cart_items": cart_items
                    "cart_action": None
                }
            },
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [message]}}
                ]
            }
        })

    return jsonify({})
