import requests
from bs4 import BeautifulSoup

data = open("us_speciality.html","r")
data = data.read()
soup = BeautifulSoup(data, 'html.parser')
options = soup.find_all("option")
f = open("specialities.txt","a")
for item in options:
	f.write( f"{item['value']},{item.text}\n" )