from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
class House:
    def __init__(self,price, id, rooms):
        self.price = price
        self.id = id
        self.rooms = rooms
houses = []

#HABITACLIA
#number of the last page
maxrequests = 50
for nreq in range(maxrequests-1):
    req = Request('https://www.habitaclia.com/viviendas-barcelona-'+str(nreq+1)+'.htm')
    mybytes = urlopen(req).read()
    mystr = mybytes.decode("utf8")
    soup = BeautifulSoup(mystr, 'html.parser')
    allarticle = soup.find_all('article')

    for article in allarticle:
        if len(article.find_all(itemprop="price")) != 0 and len(article.find_all(class_="list-item-feature")) !=0:
            htmlprice = article.find_all(itemprop="price")[0]
            htmlprice = htmlprice.get_text()
            htmlprice = htmlprice[:-2]
            htmlprice = htmlprice.replace(".", "")
            htmlrooms = article.find_all(class_="list-item-feature")[0]
            htmlrooms = htmlrooms.get_text()
            iposroom = htmlrooms.find(" habit")
            htmlrooms = htmlrooms[iposroom-1]
            id = article.get("data-id")
            house = House(int(htmlprice), id, int(htmlrooms))
            if not house in houses:
                houses.append(house)
prices = []
rooms = []
for house in houses:
    prices.append(house.price)
    rooms.append(house.rooms)

print(prices)
print(rooms)
mymodel = np.poly1d(np.polyfit(rooms, prices, 3))

myline = np.linspace(1, 7, 100)

plt.scatter(rooms, prices)
plt.plot(myline, mymodel(myline))
plt.show()