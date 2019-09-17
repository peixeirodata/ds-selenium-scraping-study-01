#importing libs
from bs4 import BeautifulSoup #webscraping
import requests #url requests
import pandas as pd #manipulate data as dataframes
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

#importing excel file with pandas
df = pd.read_excel('teste.xlsx')
site = df['Loja']

#option used by selenium to hide browser window
options = Options()
options.add_argument('--headless')

url_lst = []
access_number = []

#access google and search for all links
for i in range(len(site)):
    driver = webdriver.Firefox(options = options)
    driver.get("https://www.google.com.br")
    elem = driver.find_element_by_xpath("/html/body/div/div[4]/form/div[2]/div[1]/div[1]/div/div[2]/input")
    elem.send_keys(site[i], Keys.RETURN )
    
    time.sleep(5)

    google_url = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div[1]/a")
    url_lst.append(google_url.get_attribute("href"))
    driver.close()

df['Url'] = url_lst

#access all urls and search for visits
for url in df['Url']:
    clean_url = url.replace('https://www.','')
    page = requests.get("https://www.alexa.com/siteinfo/" + clean_url).content
    #driver = webdriver.Firefox()
    
    sp = BeautifulSoup(page, "lxml")
    access_number.append(sp.find(attrs = {'id':'kototalnum'}).text)


df['Acessos'] = access_number

#save to excel file
df.to_excel('novo.xlsx')