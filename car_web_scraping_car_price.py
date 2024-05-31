import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import csv 





start_page = 1
End_pages = 500

List_of_all= []

for page in range(start_page,End_pages + 1):
    url = "https://www.cars.com/shopping/results/?makes[]=&maximum_distance=all&models[]=&page="+str(page)+"&stock_type=all&zip="
    page = requests.get(url)
    soup=BeautifulSoup(page.text,"html.parser")
    all_cars =  soup.find_all("div",{"class" : "vehicle-card inventory-ad"})
    
    
    def car_info(all_cars):

        cards_number = soup.find_all("div",class_="vehicle-card ep-theme-hubcap") 
        number_of_car = len(cards_number)
        list_cars = []


        for i in range(number_of_car):
            try:
                car_title = cards_number[i].find("div",class_= "vehicle-details").find("a").text.strip()
            except AssertionError:
                car_title = "null"

            try:
                car_status = cards_number[i].find("p",{"class":"stock-type"}).text.strip()
            except AttributeError:
                car_status = "null"

            try:
                car_price = cards_number[i].find("div",{"class":"price-section price-section-vehicle-card"}).find("span",{"class":"primary-price"}).text.strip()
            except AttributeError:
                car_price = "null"

            # dealer information
            try:
                dealer_name = cards_number[i].find("div",{"class":"vehicle-dealer"}).find("div",{"class":"dealer-name"}).find("strong").text.strip()
            except AttributeError:
                dealer_name = "null"

            try:
                dealer_Rate = cards_number[i].find("div",{"class":"vehicle-dealer"}).find("span",class_="sds-rating__count").text.strip()
            except AttributeError:
                dealer_Rate = "null"
            try:
                dealer_nu_review = cards_number[i].find("div",{"class":"vehicle-dealer"}).find("span",class_="test1 sds-rating__link sds-button-link").text.strip()
            except AttributeError:
                dealer_nu_review = "null"
            try:
                dealer_location = cards_number[i].find("div",{"class":"vehicle-dealer"}).find("div",class_="miles-from").text.strip()
            except AttributeError:
                dealer_location = "null"

            try:
                tel_number = cards_number[i].find("div",class_="contact-buttons").find("spark-button").get("href").strip()
            except AttributeError:
                tel_number = "null"
                
            list_cars.append({"car_name":car_title,"car_status":car_status,"car_price":car_price, "dealer_name":dealer_name,"dealer_Rate":dealer_Rate,"dealer_reviews":dealer_nu_review,"dealer_location":dealer_location,"tel_number":tel_number})
        
        return list_cars
    
    
    
    df = car_info(all_cars)
    keys = df[0].keys()
    List_of_all.extend(df)
    print(List_of_all)
    
    with open("D:/projects/web_scrapping_Cars/All_cars_data.csv","w") as file_car:
        file_writer = csv.DictWriter(file_car,keys)
        file_writer.writeheader()
        file_writer.writerows(List_of_all)
       # print("the file as been created")