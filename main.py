from fastapi import FastAPI
from fastapi import Request
import db_helper
import func_helper
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()

inprogress_orders = {}

# food_items = {
#     "indian" : ["Samosa", "Dosa"],
#     "american" : ["Hot Dog", "Apple Pie"],
#     "italian" : ["Ravioli", "Pizza"]
# }

# @app.get("/get_items/{cuisine}")
# async def get_items(cuisine):
#     return food_items.get(cuisine)

# @app.get("/")
# async def root():
#     return {"message": "hello"}
"""uvicorn main:app --reload"""
"""ngrok http 8000"""
@app.post("/")
async def handle_request(request: Request):
    # retrieve the JSON data from the request
    payload = await request.json()

    # extract the necessary information from the payload
    # based on the structure of webhook request from dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    # if intent == "track.order - context: ongoing-tracking":
    #     response = track_order(parameters)
    #     return response
    
    """Maps every intent to the function which handles that intent"""
    session_id = func_helper.extract_session_id(output_contexts[0]['name'])
    intent_handler_dict = {
        "order.add - context: ongoing-order": add_to_order,
        "order.remove - context: ongoing-order": remove_from_order,
        "order.complete - context:ongoing-order": complete_order,
        "track.order - context: ongoing-tracking": track_order

    }

    return intent_handler_dict[intent](parameters, session_id)



def add_to_order(parameters:dict, session_id):
    food_items = parameters["food-item"]
    quantities = parameters["number"]
      
    if len(food_items) != len(quantities):
        fulfillmentText = "Sorry I didn't understand. Can you please specify the food items and quantities clearly"
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        
        order_str = func_helper.get_string_from_food_dict(inprogress_orders[session_id])
        fulfillmentText = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={"fulfillmentText": fulfillmentText})


def complete_order(parameters:dict, session_id: str):
    """This function will get triggered when the customer
    has completed its order...so it will link up with the database"""
    if session_id not in inprogress_orders:
        fulfillmentText = f"I am having trouble to find your order. Sorry! Can you place the order again?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillmentText = "Sorry, I Couldnt process your order due to backend error. Try once again"
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fulfillmentText = f"Awesome! Here is your order id: {order_id}" \
            f"Your order total is {order_total} which you can pay at the time of delivery!"
    
    # after our order is placed we have to remove this record from inprogress order
    # else it will mess things up
        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillmentText
    })

def save_to_db(order: dict):
    """This function will save my food item and
    quantity and order it in database 
    """
    # order = {"biryani":2, "chole":1}
    next_order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1
        
    db_helper.insert_order_tracking(next_order_id, "in_progress")
    
    return next_order_id
"""This function will receive parameters (Dict) as an argument
and which will interact with database to track my order"""   
def track_order(parameters:dict, session_id):
    order_id = int(parameters['order_id'])
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillmentText = f"The order status for order id: {order_id} is : {order_status}"
    else:
        fulfillmentText = f"No order found with order id: {order_id}"

    return JSONResponse(content = {
        "fulfillmentText": fulfillmentText
    })


def remove_from_order(parameters:dict, session_id: str):
    #step1: locate the session id record
    #step2: get the key, value from dictionary
    #step3: remove the food items. request: ["noodles", "chicken biryani"]
    if session_id not in inprogress_orders:
        return JSONResponse(content = {
        "fulfillmentText": "I am having trouble to find your order. Sorry! Can you place the order again?"})
    
    current_order = inprogress_orders[session_id]
    food_items = parameters["food-item"]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]
    
    if len(removed_items) > 0:
        fulfillmentText = f'Removed {", ".join(removed_items)} from your order'

    if len(no_such_items) > 0:
        fulfillmentText = f'Your current order does not have {", ".join(no_such_items)} these items'

    if len(current_order.keys()) == 0:
        fulfillmentText += " Your order is empty! "
    
    else:
        order_str = func_helper.get_string_from_food_dict(current_order)
        fulfillmentText += f" Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText":fulfillmentText
    })