from bs4 import BeautifulSoup
import requests
import csv

print('Up to which page do you want me to scrape to? NOTE: 3,278 is the final page the archives go back to: ')
page_number = int(input())
print('Ok, going to scrape up to that page!')
###### GLOBAL VARIABLES ARE ALL LOCATED HERE ######

website = 'https://www.reuters.com/finance/deals/mergers'
website2 = 'https://www.reuters.com'
source = requests.get(website).text
soup = BeautifulSoup(source, 'lxml') #soup = global variable where P1 is always known
x = 2
int2str = str(x)
link2 = '/news/archive/mergersnews?view=page&page=&'+int2str+'pageSize=10'
next_page = website2 + link2
source2 = requests.get(next_page).text
soup2 = BeautifulSoup(source2, 'lxml')

###### GLOBAL VARIABLES END HERE ######

###### CSV CODE BEGINS HERE ######
with open('ReutersData.csv', 'w', newline='') as csvfile:
    ReutersWriter = csv.writer(csvfile, delimiter=',')
    ReutersWriter.writerow(['Headline']+['Date/Time']+['Summary']+['Link'])
###### CSV CODE ENDS HERE ######

###### FUNCTIONS BEGIN HERE ######

def article_function(soup):
    for article in soup.select('div[class="column1 col col-10"] article'):
        headline = article.div.a.h3.text.strip()
        #threw in strip() to fix the issue of a bunch of space being printed before the headline title.
        date = article.find("span",class_ = 'timestamp').text
        summary = article.find("div", class_="story-content").p.text
        link = article.find('div', class_='story-content').a['href']
        #this bit [href] is the syntax needed for me to pull out the URL from the html code
        origin = "https://www.reuters.com/finance/deals/mergers"
        weblink = origin + link
        with open('ReutersData.csv', 'a', newline='') as csvfile:
            ReutersWriter = csv.writer(csvfile, delimiter=',')
            ReutersWriter.writerow([headline] + [date] + [summary] + [weblink])
    return

def scrape_next_page_function(soup2):
    for article in soup2.select('div[class="column1 col col-10"] article'):
        headline = article.find('h3', class_= 'story-title').text.strip()
        #threw in strip() to fix the issue of a bunch of space being printed before the headline title.
        date = article.find("span",class_ = 'timestamp').text
        summary = article.find("div", class_="story-content").p.text
        link = article.find('div', class_='story-content').a['href']
        #this bit [href] is the syntax needed for me to pull out the URL from the html code
        origin = "https://www.reuters.com/finance/deals/mergers"
        weblink = origin + link2
        with open('ReutersData.csv', 'a', newline='') as csvfile:
            ReutersWriter = csv.writer(csvfile, delimiter=',')
            ReutersWriter.writerow([headline] + [date] + [summary] + [weblink])
    return

###### FUNCTIONS END HERE ######

##page_number = int(input())

article_function(soup)
while x<=page_number: #3278 = max page limit on archives of website
    link2 = '/news/archive/mergersnews?view=page&page='+int2str+'&pageSize=10'
    next_page = website2 + link2
    source2 = requests.get(next_page).text
    soup2 = BeautifulSoup(source2, 'lxml')
    scrape_next_page_function(soup2)
    x = x+1
    int2str = str(x)

print('FINISHED SCRAPING!')
