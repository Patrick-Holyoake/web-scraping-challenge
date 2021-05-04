# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# Define function to start browser
def init_browser():
    
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Define scrape function
def scrape():
    browser = init_browser()
    
    #Define Mars data
    mars_data = {}
    
    # Mars News URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    news_soup = bs(html, 'html.parser')
    news = news_soup.find(class_="image_and_description_container")
    f_para = news.find(class_="article_teaser_body").get_text()
    
    #Mars image
    url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    
    browser.links.find_by_partial_text('FULL IMAGE').click()
    
    # Scrape brower and full the image url
    image_html = browser.html

    image_soup = bs(image_html, 'html.parser')
    image_url = image_soup.find("img", class_="fancybox-image")["src"]
    
    #Create full url
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_url
    
    
    # Mars facts
    facts_url = 'https://space-facts.com/mars/'
    df = pd.read_html(facts_url)
    
    # Only want one table
    new_df = df[0]
    
    # Name columns
    new_df.columns = ['Description', 'Value']
    
    # Convert table to html
    html_table = new_df.to_html()
    
    # Clean table
    html_table = html_table.replace('\n', '')
    
    # Mars Hemisphere
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    
    no_clicks = len(browser.find_by_css('div[class="description"] a'))
    
    hemisphere_images = []
    
    for i in range(no_clicks):
    
        links = browser.find_by_css('div[class="description"] a')
    
        links[i].click()
    
        time.sleep(5)
    
        hemisphere_html = browser.html
        hemisphere_soup = bs(hemisphere_html, 'html.parser')

        title = hemisphere_soup.find("h2", class_="title").get_text()
        img_url = hemisphere_soup.find("div", class_="downloads").a['href']
    
        dict = {}
        dict["title"] = title
        dict["img_url"] = img_url
        hemisphere_images.append(dict)
    
    browser.quit()
    
    # add all results to mars_data dictionary
    mars_data["news title"] = news
    mars_data["f_para"] = f_para
    mars_data["featured_image_url"] = featured_image_url
    mars_data["table"] = html_table
    mars_data["hemispheres"] = hemisphere_images
    
    return mars_data
    
    
    
    
    
    
    
    
    
    
    