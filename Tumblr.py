from selenium import webdriver
import time
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.keys import Keys
#keyword can be modified
search_key = 'atlanta'
driver = webdriver.Firefox()
#specify keyword
driver.get('https://www.tumblr.com/search/' + search_key)
#select data format
driver.find_element_by_xpath("//span[@class='control_text active']").click()
#specify text data
driver.find_element_by_xpath("//div[@class='menu_item post_type post_text_filter']").click()
#scroll down to the bottome of the page
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
       lastCount = lenOfPage
       time.sleep(3)
       lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
       if lastCount==lenOfPage:
           match=True
#get the whole web source
time.sleep(60)
url = driver.page_source
#scrapping
from bs4 import BeautifulSoup as bs
soup = bs(url, 'html.parser')
articles = soup.find_all('article',{'class':'is_regular'})
import json
topics = []
bodys = []
ids = []
blogs = []
descrips = []
for article in articles:
    ids.append(json.loads(article.get('data-json'))['id'])
    blogs.append(json.loads(article.get('data-json'))['tumblelog-data']['title'])
    descrips.append(json.loads(article.get('data-json'))['tumblelog-data']['description'])
    if article.find('div',{'class':'post_title'}) is None:
        topics.append('None')
    else:
        topics.append(article.find('div',{'class':'post_title'}).text.replace('\n',''))
    if article.find('div',{'class':'post_body'}) is None:
        bodys.append('None')
    else:
        bodys.append(article.find('div',{'class':'post_body'}).text.replace('\n',''))
#export data into csv
import csv
out = open('scrape_tumblr.csv', 'a')
rows=zip(topics,bodys,ids,blogs,descrips)
csv = csv.writer(out)
for row in rows:
    values = [(value.encode('utf8') if hasattr(value, 'encode') else value) for value in row]
    csv.writerow(values)