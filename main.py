from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import lxml
import requests
import datetime as dt
import pandas as pd

# service = Service("/Users/samuelfacey/Documents/Coding/chromedriver")

# driver = webdriver.Chrome(service=service)

# search_for_price = False

# // Searches and scrapes Zillow Data, then formats into a CSV file

def search(search_link):

    # // Beautiful Soup setup
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }   

    response = requests.get(url=search_link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    # // Scrapes the data from the Zillow "cards"
    cards = soup.find_all(class_="list-card-info")

    home_info = []

    # // Takes the data from individual properties, and appends them to a dictinoary
    for item in cards:
        
        dict = {}

        try:
            weblink = item.find(name="a")
            dict["Zillow link"] = weblink["href"]
        except TypeError:
            pass

        try:
            address = (item.find(name="address")).getText()
            dict["Address"] = address
        except AttributeError:
            pass

        try:
            price = item.find(name="div", class_="list-card-price")
            dict["Price"] = price.getText()
        except AttributeError:
            pass

        try:
            details = item.find(class_="list-card-details")
            
            d_list = []
            for items in details:
                if items == "- House for sale":
                    pass
                else:
                    d_list.append(items.getText())
            dict["Beds, Baths, Square Feet, Property Type"] = d_list
        except TypeError:
            pass
        
        home_info.append(dict)
    
    # // Creates the CSV file using the list of dictionaries
    date = (dt.datetime.now()).date()
    data = pd.DataFrame(home_info)
    data.to_csv(f"/Users/samuelfacey/Documents/Coding/Python/Zillow Property Finder/Zillow Search Result {date}.csv")


link = input("If you have a search link from Zillow.com, paste it here. If not, press 'Enter' to continue: ")

# // If user wants to create a custom link using the program
if link == "":

    custom_link = "https://www.zillow.com/homes/"

    buy_or_rent = input("Are you looking to Buy, or Rent, a home? Leave enpty for Buy, press '1' for Rent: ")

    if buy_or_rent != "":
        custom_link += "for_rent/"

    search_input = input("Enter an address, neighborhood, city, or ZIP code: ")

    # // Formats the input for the hyperlink
    search_query = ""

    for char in search_input:
        if char == ",":
            char = " "
        if char == " ":
            char = "-"
        search_query += char
    
    custom_link += f"{search_query}/"

    # price_input = input("Enter your max price. Leave empty if no preference: ")

    # if price_input != "":
    #     search_for_price = True

    houses_or_all = input("Press '1' to show only houses, leave empty to show all property types.")

    if houses_or_all == "0":
        custom_link += "houses/"

    bed_input = input("How many bedrooms? Press '5' for 5 or greater. Leave empty if no preference: ")

    if bed_input != "":
        custom_link += f"{bed_input}-_beds/"

    bath_input = input("How many bathrooms? Leave empty if no preference: ")

    if bath_input != "":
        custom_link += f"{bath_input}-_baths/"

    # sqft = input("Do you have a preference for a minimum sq. footage for the home? Y/N: ").lower()

    # if sqft == "y":
    #     print("What is you minimum requirement? Type in your selection from the following:")
    #     sqft = input("500, 750, 1000, 1250, 1500, 1750, \n2000, 2250, 2500, 2750, 3000, \n3500, 4000, 5000, 7500")

    # lot = input("Do you have a preference for a minimum lot size one acre or greater? Y/N? ")

    # if lot == "y":
    #     print("What is you minimum requirement? Type the number from the following:")
    #     lot = input("1/2 acre, 1 acre, 2 acres, 5 acres, 10 acres, 20 acres, 50 acres, 100 acres")
    
    search(search_link=f"{custom_link}")

else:
    search(search_link=link)

#--🚀 Zillow Property Finder by CaptLynx 2022 🚀--#