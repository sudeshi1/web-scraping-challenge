# Import Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    mars_dict = {}

### NASA Mars News

    # Scrape news title and news paragraph -> https://redplanetscience.com/
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')

    # Retrieve the latest news title
    news_title = soup.find('div', class_ = 'content_title').text
    # Retrieve the latest news paragraph
    news_para = soup.find('div', class_ = 'article_teaser_body').text
    
# Scrape Mars Image -> https://spaceimages-mars.com/

    jpl_image_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_image_url)
    html = browser.html
    soup = bs(html,"html.parser")
    # Retrieve image
    image_url = soup.find_all("img", class_="headerimage fade-in")['src']
    # Retrieve featured image URL
    featured_image_url = jpl_image_url + image_url
    
#Scrape Mars facts -> https://galaxyfacts-mars.com/
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    mars_fact = tables [1]
    mars_fact = mars_fact.rename(columns={0:"Profile",1:"Value"}, errors="raise")
    mars_fact.set_index("Profile", inplace=True)
    mars_fact
    fact_table = mars_fact.to_html()
    fact_table.replace('\n','')

# Scrape Mars Hemispheres URL -> https://marshemispheres.com/
    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)
    html = browser.html
    soup = bs(html,'html.parser')
    
    def scrape_img(search_url):
        # Retrieve page with the requests module
        response = requests.get(search_url)
        soup = bs(response.text, "html5lib")
        # Store high resolution image URL to create a final hemisphere image URL
        hem_img_url = soup.find('img', class_='wide-image')['src']
        final_img_url = hemisphere_url + hem_img_url
        # Store the image url information into a dictionary
        title_img_dicts['image_url'] = final_img_url
    
        return (title_img_dicts['image_url'])          
            
    def dict_to_list(title_img_dicts):
        new_dict = {}
    
        copy_dict = title_img_dicts.copy()
        new_dict.update(copy_dict)
    
        return (new_dict)

# Use a Python dictionary to store the data using the keys image URL and title

    img_containers = soup.find_all('div', class_='item')

# Empty list to import image reference links
    img_url = []

# Empty dictionary to holds title information and URL of image
    title_img_dicts = {}

# Empty list to hold each dictionary of title and full img url
    hemisphere_img_urls = []

# Extract the title and full image URL
    for img in img_containers:
        title_img_dicts['title'] = img.find('h3').text
        img_link = img.find('a', class_='itemLink product-item')['href']
        img_url.append(img_link)
        img_url_list = [hemisphere_url + url for url in img_url]
    
        for search_url in img_url_list:
            scrape_img(search_url)
    
# Append the empty dictionary with the image URL string and the hemisphere title

        hemisphere_img_urls.append(dict_to_list(title_img_dicts))
    
    mars_dict={
        "news_title":news_title,
        "news_para":news_para,
        "featured_image_url":featured_image_url,
        "fact_table":fact_table,
        "hemisphere_images":hemisphere_img_urls
}

    # quit the browser after scraping
    browser.quit()
    
    # return results
    return mars_dict


    
