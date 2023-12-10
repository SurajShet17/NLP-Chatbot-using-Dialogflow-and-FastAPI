import re

"""This function will extract unique id from url from dialogflow and return the 
session id with the help of re module in python"""
def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string
    
    return ""

def get_string_from_food_dict(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])