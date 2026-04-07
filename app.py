from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    tag = req.get('fulfillmentInfo', {}).get('tag')
    session_params = req.get('sessionInfo', {}).get('parameters', {})

    selected_product = session_params.get('selected_product')
    remove_product = session_params.get('remove_product')
    cart_items = session_params.get('cart_items', {})
    intent = req.get('intentInfo', {}).get('displayName')

    message = ""

    # -------------------------------
    # PRODUCT SEARCH (STATIC)
    # -------------------------------
    if tag == "product_search":
        message = "Here are some products:\n- iPhone 13\n- iPhone 14\n- Samsung"

    # -------------------------------
    # CART HANDLER (MAIN LOGIC)
    # -------------------------------
    elif tag == "cart_handler":

        # -------------------------------
        # ADD TO CART
        # -------------------------------
        if intent == "cart.add":
            if selected_product:
                if selected_product in cart_items:
                    cart_items[selected_product] += 1
                else:
                    cart_items[selected_product] = 1

                message = f"{selected_product} added to cart"
#------------CART REMOVE-------------
        
        elif intent == "cart.remove":
            if remove_product in cart_items:
                del cart_items[remove_product]
                message = f"{remove_product} removed from cart"
            else:
                message = "Item not found in cart"
#-------------- CLEAR CART-------
        
        elif intent == "cart.clear":
            cart_items = {}
            message = "Your cart is now empty"
        
        # -------------------------------
        # VIEW CART
        # -------------------------------
        elif intent == "cart.view":
            pass  # handled below

        # -------------------------------
        # DEFAULT: SHOW CART
        # -------------------------------
        if cart_items:
            items = "\n".join([f"{k} (x{v})" for k, v in cart_items.items()])
            message += f"\n\nYour cart contains:\n{items}"
        else:
            if not message:
                message = "Your cart is empty"

    return jsonify({
        "sessionInfo": {
            "parameters": {
                "cart_items": cart_items
            }
        },
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [message]}}
            ]
        }
    })


if __name__ == '__main__':
    app.run(port=8080)
