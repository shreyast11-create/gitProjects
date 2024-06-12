import requests
from bs4 import BeautifulSoup
from csv import writer


url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=2," \
      "3&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House," \
      "Villa&cityName=Gurgaon"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
soup_list = soup.find_all("div", class_="mb-srp__list")

item_list = []

with open("housing.csv", "w", encoding="utf8", newline="") as f:
    f_writer = writer(f)
    header = ["Location", "Carpet/Super Area", "Price"]
    f_writer.writerow(header)
    for item in soup_list:
        location = item.h2.text
        area = item.find("div", class_="mb-srp__card__summary--value").text
        price = item.find("div", class_="mb-srp__card__price--amount").text
        f_writer.writerow([location, area, price])

