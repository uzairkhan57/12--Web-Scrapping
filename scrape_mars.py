# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
from time import sleep

def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # Run the function below:
    news, news_paragraph= mars_news(browser)
    
    # Run the functions below and store into a dictionary
    results = {
        "title": news,
        "paragraph": news_paragraph,
        "image_URL": jpl_image(browser),
        "facts": mars_facts(),
    }

    # Quit the browser and return the scraped results
    browser.quit()
    return results

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape the first article title and teaser paragraph text; return them
    news=soup.find("div", class_="bottom_gradient").get_text()
    news_paragraph = soup.find("div", class_="article_teaser_body").get_text()
    return news, news_paragraph

def jpl_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Go to 'FULL IMAGE', then to 'more info'
    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(1)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape the URL and return
    image_url = soup.find('figure', class_='lede').a['href']
    ful_url_image = f'https://www.jpl.nasa.gov{image_url}'
    return ful_url_image

    
def mars_facts():
    tables = pd.read_html(url)
    facts = tables[0]
    facts.columns = ['Facts', 'Values']
    facts
    # Set index to property in preparation for import into MongoDB
    facts.set_index('Facts', inplace=True)
    
    # Convert to HTML table string and return
    return facts.to_html()

    
