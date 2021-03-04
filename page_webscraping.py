import bs4
import requests
from bs4 import BeautifulSoup as bs
import getGeo
import time
import numpy as np

start_time = time.time()

# Set start url
my_url = requests.get('link')

# id
id = 1
counter = 1

# Create and open csv file
filename = "Houses.csv"
f = open(filename, "w")
# Set headers in csv
headers = "id,price,sq,rooms,floor,year,address,city,latitude,longitude\n"
f.write(headers)


# Check if there is next page
next_page = "xyz"

# Stops if there wasn't next page
print("Start while loop")
while next_page != "":

    print(f"Page {counter}...")

    # Take url content with soup
    soup = bs(my_url.content, "html.parser")

    # Find all sales announcements
    containers = soup.find_all("div", class_ = "offer-item-details")

    # open a sale announcement one at a time
    # start from 4th, because first 3 are randomly recommended from all announcements --> avoid of duplicates
    # print("Start for loop")
    for container in containers[3:]:
        # print(f"Object {id}...")

        # set a link to a sales announcement
        uObject_url = requests.get(container.a['href'])
        soup_ob = bs(uObject_url.content, "html.parser")

        # Set id
        id = id

        # Get pirce from website sales announcement
        try:
            price = soup_ob.find("strong", class_ = "css-srd1q3").text
            # remove currency name
            price = price.replace("zł", "").replace(" ", "").replace(",", ".")
            try:
                price = float(price)
            except:
                try:
                    price = int(price)
                except:
                    price = np.nan
        except:
            price = np.nan

        # Get square meters from website sales announcement
        try:
            sq = soup_ob.find("div", {'aria-label' : 'Powierzchnia'})
            sq = sq.find("div", {'class' : 'css-1ytkscc ecjfvbm0'}).text
            sq = sq.replace("m²", "").replace(" ", "").replace(",", ".")
            try:
                sq = float(sq)
            except:
                sq = np.nan
        except:
            sq = np.nan


        # Get number of rooms from website sales announcement
        try:
            rooms = soup_ob.find("div", {'aria-label' : 'Liczba pokoi'})
            rooms = rooms.find("div", {'class' : 'css-1ytkscc ecjfvbm0'}).text
            try:
                rooms = int(rooms)
            except:
                rooms = np.nan
        except:
            rooms = np.nan

        # Get floor from website sales announcement
        try:
            floor = soup_ob.find("div", {'aria-label' : 'Piętro'})
            floor = floor.find("div", {'class' : 'css-1ytkscc ecjfvbm0'}).text
        except:
            floor = np.nan

        # If floor != number, and floor == parter (= ground floor) set floor = 0
        try:
            floor = int(floor)
        except:
            if floor == "parter":
                floor = 0
            else:
                floor = floor


        # Get year of apartment from website sales announcement
        try:
            year = soup_ob.find("div", {'aria-label' : 'Rok budowy'})
            year = year.find("div", {'class' : 'css-1ytkscc ecjfvbm0'}).text
            year = int(year)
        except:
            year = np.nan

        # Get the address and city from website
        try:
            address = soup_ob.find("a", class_ = "css-xlfzws eom7om61").text
            # Set a city
            city = address.split(",")[0]
            # Set a address
            address = address.split(",", 1)[1:][0].replace(",", "")

            # After split remove white space before name of a city
            if address[0] == " ":
                address = address[1:]
            else:
                address = address
        except:
            address = "None"
            city = "None"

        # Get the latitude and longitude from full address
        lat, lng = getGeo.getGeo(address+", "+city)


        # reset the city
        if lat != None:
            try:
                city = getGeo.resetCity(lat, lng, city)
            except:
                print("Problem with re-setting a city!")
                continue


        # write in csv a row with all information about sale announcement
        f.write(f"{id},{price},{sq},{rooms},{floor},{year},{address},{city},{lat},{lng}\n")

        # print(f"Object {id} completed!")
        id = id+1


    # Set the link to a next page
    next_page = soup.find("li", class_ = "pager-next").a['href']

    # If link is != "" set 'my_url' = link to the next page
    if next_page != "":
        my_url = requests.get(next_page)
    else:
        continue

    print(f"Page {counter} done!")
    counter = counter+1

# close a csv file
f.close()

print("End of while loop")



print("Successful all data collection")
total_time = time.time() - start_time
print(f"Duration {total_time/60} mins.")






#
