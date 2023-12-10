
# Natural Language Processing Chatbot using Dialogflow and FastAPI

## Objective:
The primary goal of the project is to create an intelligent chatbot capable of understanding user queries related to food orders and providing relevant responses. The chatbot is integrated with Dialogflow for NLP and utilizes FastAPI as the backend to process requests, interact with a MySQL database, and manage the flow of conversations.

## Core Features:

#### Order Management:
Users can add items to their food orders, specifying the quantity of each item.
Items can be removed from the order as well.
The chatbot keeps track of in-progress orders using the inprogress_orders dictionary.

#### Order Completion:
Users can complete their orders, triggering the chatbot to save the order details to a MySQL database.
The system generates a unique order ID for each completed order.

#### Order Tracking:
Users can inquire about the status of their orders by providing the order ID.
The chatbot retrieves the order status from the database and communicates it to the user.

#### Dialogflow Integration:
The project leverages Dialogflow for natural language understanding.
Webhook endpoints in FastAPI handle incoming requests from Dialogflow, extracting intent and parameters.

#### Database Interaction:
The system uses a MySQL database to store order information, including items, quantities, order status, and total order price.
Database interactions include inserting order items, tracking order status, and calculating total order prices.

#### Session Management:
Session IDs are used to keep track of user interactions and maintain the context of ongoing orders.

## Project Components:

#### FastAPI Backend:
The FastAPI framework is employed to handle HTTP requests, define endpoints, and manage the business logic of the chatbot.

#### Dialogflow Webhook:
The project acts as a webhook for Dialogflow, receiving JSON payloads and processing them to determine user intent and parameters.

#### Database Layer:
The MySQL database is central to the project, storing information about orders, order items, and order tracking.

#### Helper Functions (func_helper.py):
Functions for extracting session IDs and formatting food dictionaries are included to enhance code modularity.

#### Error Handling:
While the project demonstrates the core functionality, incorporating robust error handling throughout the codebase is recommended for production use.

#### Security Measures:
Proper security measures should be implemented, especially concerning database connections and user data handling.
Future Considerations:

#### Asynchronous Operations:
Consider implementing asynchronous database queries to enhance the performance of the FastAPI application.

#### Unit Testing:
Develop unit tests to ensure the reliability and correctness of the code.

#### Documentation:
Enhance code documentation by adding comments and providing detailed explanations for better code understanding and maintainability.


## Requirements

- Python 3.x
- All libraries contained in requirements.txt file

## Installation

1. Clone this repository to your local machine.
2. Install all the required Python packages (present in requirements.txt file) by running the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository.
2. After installing all the dependencies in requirements.txt file,
run server launch command uvicorn which will be used to run the backend server.

```bash
uvicorn main:app --reload
```
3. Install ngrok which will be used to create secure https secured protocol.

4. Make sure to change the content and style location our your choice.


## Contact

For any issues or questions, please contact surajshet5555@gmail.com.

---
