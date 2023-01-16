from csv import writer
from bs4 import BeautifulSoup
import requests

page = 1
url = "https://www.autoscout24.com/lst?offer=U&sort=standard&desc=0&atype=C&ustate=N%2CU&powertype=kw&search_id=1mhhc9r9fxb&page={page}"

# Open the file in write mode and write the header
with open('cars.csv', 'w', encoding='utf8', newline='') as file:
    thewriter = writer(file)
    header = ['car_id','model','price','date added','power of engine','used','number of previous owners','transmission type','fuel type','fuel consumption','co2 emissions']
    thewriter.writerow(header)
# Iterate over the pages
for page in range(20):
   req =requests.get(url.format(page=page))

   # Extract the div elements
   soup = BeautifulSoup(req.content, 'html.parser')
   lists= soup.find_all('div', class_="ListItem_wrapper__J_a_C")

   # Open the file in append mode and write the data for each div element
   with open('cars.csv', 'a',encoding='utf8', newline='') as file:
     thewriter=writer(file, delimiter =";")

     for list in lists:
         id=id+1
         h2_element = list.find('h2')
         title=h2_element.text
         price=list.find('div',class_="Price_wrapper__E5C5Y").text
         details=list.find_all('span',class_="VehicleDetailTable_item__koEV4")
         text_list = []
         for detail in details:
             text_list.append(detail.text)

         infos=[id,title,price]
         infos.extend(text_list)
         thewriter.writerow(infos)

    

    

