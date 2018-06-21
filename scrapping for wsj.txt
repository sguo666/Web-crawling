#packages we need
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import csv
import json
import re

#search articles with specified keyword
keyword = 'atlanta'
link = 'https://www.wsj.com/search/term.html?KEYWORDS='+keyword+'&page='
titles = []
descrips = []
links = []

#the search result has 20 pages in total, extract title, description and link
for i in range(1,21):
    r=requests.get(link+str(i)+'&mg=prod/accounts-wsj')
    soup=BeautifulSoup(r.text, 'html.parser')
    scripts=soup.find_all('div',{'class': 'pageFrame'})
    content=BeautifulSoup(str(scripts))
    articles = content.find('ul',{'class':'items'})
    articles = articles.find_all('li')

    for article in articles:
        try:
            prefix = str(article)[:80]
            if 'http://www.w3.org/1999/html' in prefix:
                titles.append(article.h3.text)
                descrips.append(str(article.p).lstrip("<p>").rstrip("</p>"))
                hrefprefix = "https://www.wsj.com"
                if str(article.h3.a["href"]).startswith(hrefprefix):
                    links.append(str(article.h3.a["href"]))
                else:
                    links.append(hrefprefix + str(article.h3.a["href"]))
            else: continue
        except:
            break

#Log in WSJ with subscription
driver = webdriver.Firefox()
driver.get('https://www.wsj.com')
time.sleep(10)
driver.find_element_by_link_text("Sign In").click()
time.sleep(10)
driver.find_element_by_id("username").send_keys('')
driver.find_element_by_id("password").send_keys('')
driver.find_element_by_class_name("sign-in").submit()

times = []
articles = []
authors = []

#Use links to get author, time and article
for i in links:
    driver.get(i)
    url = driver.page_source
    soup = BeautifulSoup(url, 'html.parser')
    script = soup.find('script',{'type':'application/ld+json'}).text
    script = script.encode('utf-8')
    script = json.loads(script)
    if script['author']['name'] is None or ' ':
        authors.append("None")
    else:
        authors.append(script['author']['name'])
    times.append(script['datePublished'])
    paragraphs = driver.find_elements_by_xpath('//*[@id="wsj-article-wrap"]/p')
    text = []
    for t in range(0, len(paragraphs)):
        if ('@wsj.com' not in paragraphs[t].text and 
            'contributed to this article' not in paragraphs[t].text):
            text.append(paragraphs[t].text)
    text = "".join(text)    
    text = re.sub(r'\n', ' ', text)
    text = re.sub("\W", " ", text)
    articles.append(text)


#Write csv to store data
rows = zip(titles,descrips,links,authors,times,articles)
with open('scrape_wsj1.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = ",")
    columns = ['Title','Description','Link','Author','Timestamp','Article']
    writer.writerow(columns)
    for row in rows:
        writer.writerow(row)