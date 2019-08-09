#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Declare Dependencies 
from bs4 import BeautifulSoup
from selenium import webdriver
from splinter import Browser
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Choose the executable path to driver 
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Nasa URL
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[4]:


# HTML Object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')


# Retrieve the latest element that contains news title and news_paragraph
news_title = soup.find('div', class_='content_title').find('a').text
news_p = soup.find('div', class_='article_teaser_body').text

# Display scrapped data 
print(news_title)
print(news_p)


# In[5]:


# VJPL Mars Space Images - Featured Image
image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(image_url_featured)


# In[6]:


# HTML Object 
html_image = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html_image, 'html.parser')

# Retrieve background-image url from style tag 
featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

# Website Url 
main_url = 'https://www.jpl.nasa.gov'

# Concatenate website url with scrapped route
featured_image_url = main_url + featured_image_url

# Display full link to featured image
featured_image_url


# In[7]:


weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)


# In[8]:


mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(mars_weather_url)
mars_weather_html = browser.html
mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
for tweet in latest_tweets: 
    weather_tweet = tweet.find('p').text
    if 'Sol' and 'pressure' in weather_tweet:
        print(weather_tweet)
        break
    else: 
        pass


# In[9]:


import pandas as pd


# In[10]:


# Visit Mars facts url 
facts_url = 'http://space-facts.com/mars/'

# Use Panda's `read_html` to parse the url
mars_facts_df = pd.read_html(facts_url)

mars_facts_df


# In[11]:


# Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
mars_df = mars_facts_df[0]

mars_df.columns = ['Mars - Earth Comparison','Mars', 'Earth']

# Display mars_df
mars_df


# In[12]:


mars_only = mars_df.drop(columns={'Earth'})
mars_only


# In[13]:


mars_html_table = mars_only.to_html()
mars_html_table


# In[14]:


hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemispheres_url)


# In[15]:


# Creating BeautifulSoup object and parsing with 'html.parser'
html = browser.html
hemisphere_soup = BeautifulSoup(html, 'html.parser')


# In[16]:


items = hemisphere_soup.find_all('div', class_='item')

# Create empty list for hemisphere urls 
new_image_urls = []

# Store the main_ul 
hemispheres_main_url = 'https://astrogeology.usgs.gov'

# loop through items
for i in items: 
    # Store title
    title = i.find('h3').text
    
    #Link to main image site
    partial_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
    soup = BeautifulSoup( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
    new_image_urls.append({"title" : title, "img_url" : img_url})
    

# Display hemisphere_image_urls
new_image_urls

