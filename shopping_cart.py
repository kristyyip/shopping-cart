# shopping_cart.py

#from pprint import pprint
from datetime import datetime

import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017

# print(products)
# pprint(products)
# TODO: write some Python code here to produce the desired output

# capturing user inputs

subtotal = 0 # to define the variable
selected_ids = [] # to define the list

while True:
    selected_id = input("Please input a product identifier: ") # receive product identifier from user
    if selected_id == "DONE": # stop capturing inputs if user is finished
        break
    elif [p for p in products if str(p["id"]) == str(selected_id)]: # validating product identifier
        selected_ids.append(selected_id)
    else:
        print("Hey, are you sure that product identifier is correct? Please try again!")

# info display / output - print or email receipt
while True:
    receipt_choice = input("Would you like to have the receipt emailed? ")

    if (receipt_choice.lower() == "no"): #print receipt
        ## print store name
        print("---------------------------------")
        print("MARKET BASKET")
        print("www.shopmarketbasket.com")
        print("---------------------------------")

        ## print current date and time
        ## source: tecadmin.net/get-current-date-time-python/
        current_datetime = datetime.now()
        print("CHECKOUT AT: " + current_datetime.strftime("%Y-%m-%d %I:%M %p"))
        print("---------------------------------")

        ## print selected ids
        print("SELECTED PRODUCTS:")

        for selected_id in selected_ids:
            matching_products = [p for p in products if str(p["id"]) == str(selected_id)] # need to convert both to string so that they can be compared
            matching_product = matching_products[0]
            subtotal = subtotal + matching_product["price"] # to keep a running total of the shopping cart
            price_usd = " (${0:.2f})".format(matching_product["price"])
            print(" ... " + matching_product["name"] + price_usd)
        print("---------------------------------")

        ## print total price
        print("SUBTOTAL: ${0:.2f}".format(subtotal))
        tax = subtotal * .0875 # calculating sales tax
        print("TAX: ${0:.2f}".format(tax))
        total_price = subtotal + tax # calculating total after tax
        print("TOTAL: ${0:.2f}".format(total_price))
        print("---------------------------------")
        print("THANKS, SEE YOU AGAIN SOON!")
        print("---------------------------------")
        
        break
    elif (receipt_choice.lower() == "yes"): #email receipt
        html_list_items = [] # to define the list

        for selected_id in selected_ids:
            matching_products = [p for p in products if str(p["id"]) == str(selected_id)] # need to convert both to string so that they can be compared
            matching_product = matching_products[0]
            subtotal = subtotal + matching_product["price"] # to keep a running total of the shopping cart
            price_usd = " (${0:.2f})".format(matching_product["price"])
            html_list_items.append(matching_product["name"] + price_usd) # to store the matching products

        # capture current date and time
        current_datetime = datetime.now()
        timestamp = current_datetime.strftime("%B %d, %Y at %I:%M %p")

        # calculate tax and total price
        tax = subtotal * .0875
        total_price = subtotal + tax

        # format the totals
        subtotal = "${0:.2f}".format(subtotal)
        tax = "${0:.2f}".format(tax)
        total_price = "${0:.2f}".format(total_price)

        load_dotenv()  

        SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
        MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")

        client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
        print("CLIENT:", type(client))

        subject = "Your Receipt from Market Basket"

        # body of the email
        html_content = f"""
            <img src="https://www.shareicon.net/data/128x128/2016/05/04/759867_food_512x512.png">
            <h3>Hello, this is your receipt from Market Basket!</h3>
            <p>Date: {timestamp}</p>
            <p>You ordered: {html_list_items}</p>
            <p>Subtotal: {subtotal}</p>
            <p>Tax: {tax}</p>
            <p>Total: {total_price}</p>
            <h3>Thank you for shopping at Market Basket. Please come again soon!</h3>
        """

        print("HTML:", html_content)

        message = Mail(from_email=MY_ADDRESS, to_emails=MY_ADDRESS, subject=subject, html_content=html_content)

        try:
            response = client.send(message)

            print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
            print(response.status_code) #> 202 indicates SUCCESS
            print(response.body)
            print(response.headers)

        except Exception as e:
            print("OOPS", e.message)
        
        break
    else:
        print("Sorry, that wasn't a valid choice. Please choose 'yes' or 'no'.")