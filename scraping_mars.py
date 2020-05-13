
# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import time
import pandas as pd
import requests

def scrape():
    mars_results = {}
    mars = []
    # Mars news scraping

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(1)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')

    news_list = nasa_soup.find('ul', class_='item_list')
    first_item = news_list.find('li', class_='slide')
    nasa_title = first_item.find('div', class_='content_title').text
    nasa_paragraph = first_item.find('div', class_='article_teaser_body').text

    print(nasa_title)
    print(nasa_paragraph)

    mars_results["nasa_title"] = nasa_title
    mars_results["nasa_paragraph"] = nasa_paragraph

    # Featured image url scraping

    url_image ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    css = browser.find_by_css('a.fancybox-expand')
    css.click()
    time.sleep(1)

    jpl = browser.html
    jpl_soup = BeautifulSoup(jpl, 'html.parser')

    featured_img_base = "https://www.jpl.nasa.gov"
    featured_img_url_raw = jpl_soup.find("div", class_="carousel_items").find("article")["style"]
    featured_img_url = featured_img_url_raw.split("'")[1]
    featured_img_url = featured_img_base + featured_img_url
    featured_img_url

    mars_results["featured_img_url"] = featured_img_url

    #twitter scraping
    url_twitter = 'https://twitter.com/marswxreport?lang=en'

    response_twitter = requests.get(url_twitter)
    response_twitter

    twitter_soup = BeautifulSoup(response_twitter.text, 'html.parser')
    #twitter_soup.prettify()

    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    twitter_soup = BeautifulSoup(response_twitter.text, 'html.parser')

    twitter_latest= twitter_soup.find('div', class_='js-tweet-text-container').get_text().strip()
    twitter_latest  

    mars_results["twitter_latest"] = twitter_latest  

    #Mars Facts

    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    tables

    df = tables[0]
    df

    df.columns = ["Mars Information","Values"]
    df
    html_mars = df.to_html()
    html_mars
    html_mars = html_mars.replace('\n', '')

    mars_results["html_mars"] = html_mars

    #Mars Hemispheres
    
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    hemisphere_image_urls = []

    for i in range (4):
        images = browser.find_by_css('a.product-item h3')
        images[i].click()
        hemisphere_html = browser.html
        weather_soup = BeautifulSoup(hemisphere_html, 'html.parser')
        partial_url = weather_soup.find("img", class_="wide-image")["src"]
        image_title = weather_soup.find("h2",class_="title").text
        image_url = 'https://astrogeology.usgs.gov'+ partial_url
        image_dict = {"title":image_title,"image_url":image_url}
        hemisphere_image_urls.append(image_dict)
        browser.back()
        
    hemisphere_image_urls

    mars_results["hemisphere_image_urls"] = hemisphere_image_urls
    print(mars_results)
    mars.append(mars_results)
    print(mars)
    
    return mars_results
    
   
scrape()


