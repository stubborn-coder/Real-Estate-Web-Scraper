#import libraries
from bs4 import BeautifulSoup
from numpy import number
import requests
from csv import writer
from selenium.webdriver.common.by import By
from selenium import webdriver
import time	


browser = webdriver.Firefox()
url= "https://www.pararius.com/apartments/nederland?ac=1"
page = browser.get(url)

#wait for page to load
time.sleep(5)

#get source code of the browser
source = browser.page_source

#convert to html
soup = BeautifulSoup(source, 'html.parser')

#divide sections
pages_list = soup.find_all('a',class_="pagination__link")
print(pages_list)
number_of_pages = []

for i in range(len(pages_list)-1):
    b= pages_list[i].text.strip()
    print(b)
    value = b
    value = str(value)
    value = ""+ value
    value = int(value)
    number_of_pages.append(value)

print(number_of_pages)

#accept cookies
browser.find_element(By.ID,'onetrust-accept-btn-handler').click()
time.sleep(1)

#make the csv file
with open('housing.csv', 'w', encoding='utf8', newline='') as f:
    #headers
    thewriter = writer(f)
    header = ['Title', 'Location', 'Price', 'Area','Number of rooms']
    thewriter.writerow(header)

    for a in range(1,number_of_pages[len(number_of_pages)-1]+1):  

        #updating html source code
        if a != 1:
            #url = 'https://www.pararius.com/apartments/nederland/page-' +str(a)
            url = browser.current_url
            page = browser.get(url)
            source = browser.page_source
            soup = BeautifulSoup(source,'html.parser')
        
        print(a)
    
        lists = soup.find_all('section', class_="listing-search-item")
        for list in lists:
            
            title = list.find('a', class_="listing-search-item__link--title").text
            location = list.find('div', class_="listing-search-item__location").text.strip()
            price = list.find('div', class_="listing-search-item__price").text.strip()[:-10]
            area = list.find('li', class_="illustrated-features__item--surface-area").text
            rooms = list.find('li', class_="illustrated-features__item--number-of-rooms").text[:1]
            
            info = [title, location, price, area,rooms]
            thewriter.writerow(info)
        
        #should not click next if it's on the last page
        if a != number_of_pages[len(number_of_pages)-1]:
            browser.find_element(By.CLASS_NAME,'pagination__link--next').click()
            #wait for the browser to load
            time.sleep(3)

#browser.quit()