#!/usr/bin/env python
# coding: utf-8

# In[1]:


# load packages
import requests
from bs4 import BeautifulSoup


# In[2]:


#the URL of the site
base_site = "https://editorial.rottentomatoes.com/guide/140-essential-action-movies-to-watch-now/"


# In[3]:


# sending a request to the webpage
response = requests.get(base_site)
response.status_code


# In[4]:


# get the HTML from the webpage
html = response.content


# In[5]:


# convert the HTML to a BeatifulSoup object
soup = BeautifulSoup(html, 'lxml')


# In[6]:


# Exporting the HTML to a file
with open('Rotten_tomatoes_page_2_LXML_Parser.html', 'wb') as file:
    file.write(soup.prettify('utf-8'))


# ## Finding an element containing all the data

# In[7]:


# Find all div tags on the webpage containing the information we want to scrape
divs = soup.find_all("div", {"class": "col-sm-18 col-full-xs countdown-item-content"})
divs


# # Extracting the title, year and score of each movie

# In[8]:


# The title, year and score of each movie are contained in the 'h2' tags


# In[9]:


# Extracting all 'h2' tags
headings = [div.find("h2") for div in divs]
headings


# In[10]:


# Inspecting the text inside the headings
[heading.text for heading in headings]


# In[11]:


#  notice that:

# The movie title is in the 'a' tag
# The year is in a 'span' with class 'start-year'
# The score is in a 'span' with class 'tMeterScore'


# ## Title

# In[12]:


# Let's check all heading links
[heading.find('a') for heading in headings]


# In[13]:


# Obtaining the movie titles from the links
movie_names = [heading.find('a').string for heading in headings]
movie_names


# ## Year

# In[14]:


# Extracting the year string
years = [heading.find("span", class_ = 'start-year').string for heading in headings]
years


# In[15]:


# Updating years with stripped values
years = [int(year.strip('()')) for year in years]
years


# ## Score

# In[16]:


# HOMEWORK

# Filtering only the spans containing the score
[heading.find("span", class_ = 'tMeterScore') for heading in headings]


# In[17]:


# Extracting the score string
scores = [int(heading.find("span", class_ = 'tMeterScore').string.strip('%')) for heading in headings]
scores


# ## Critics Consensus

# In[18]:


# The critics consensus is located inside a 'div' tag with the class 'info critics-consensus'
# This can be found inside the original 'div's we scraped
divs


# In[19]:


# Getting the 'div' tags containing the critics consensus
consensus = [div.find("div", {"class": "info critics-consensus"}) for div in divs]
consensus


# In[20]:


# Defining the phrase to be removed 
common_phrase = 'Critics Consensus: '


# In[21]:


# Define a variable to store the length
common_len = len(common_phrase)


# In[22]:


# Cleaning the list of the common phrase
consensus_text = [con.text[common_len:] for con in consensus]
consensus_text


# In[23]:


# We can add if-else logic to only truncate the string in case it starts with the common phrase
consensus_text = [con.text[common_len:] if con.text.startswith(common_phrase) else con.text for con in consensus ]
consensus_text


# ## Directors

# In[24]:


# Extracting all director divs
directors = [div.find("div", class_ = 'director') for div in divs]
directors


# In[25]:


# The director's name can be found as the string of a link

# Obtaining all director links
[director.find("a") for director in directors]


# In[26]:


final_directors = [director.find("a").string for director in directors]
final_directors


# ## Cast info

# In[27]:


cast_info = [div.find("div", class_ = 'cast') for div in divs]
cast_info


# In[28]:


# Each cast member's name is the string of a link
# There are multiple cast members for a movie


# In[29]:


# Initialize the list of all cast memners
cast = []
for c in cast_info:
    cast_links = c.find_all('a')
    cast_names = [link.string for link in cast_links]
    
    cast.append(", ".join(cast_names)) 

cast


# ## Synopsis

# In[30]:


# The synopsis is located inside a 'div' tag with the class 'info synopsis'
synopsis = [div.find('div', class_='synopsis') for div in divs]
synopsis


# In[31]:


# Extracting the text
synopsis_text = [syn.contents[1].strip() for syn in synopsis]
synopsis_text


# # Representing the data in structured form

# In[32]:


# load the pandas package
import pandas as pd


# ## Creating a Data Frame

# In[33]:


movies_info = pd.DataFrame()
movies_info["Movie Title"] = movie_names
movies_info["Year"] = years
movies_info["Score"] = scores
movies_info["Director"] = final_directors
movies_info["Synopsis"] = synopsis_text  
movies_info["Cast"] = cast
movies_info["Consensus"] = consensus_text

# Let's see how it looks
movies_info


# In[34]:


# By default pandas abbreviates any text beyond a certain length (as seen in the Cast and Consensus columns)

# We can change that by setting the maximum column width to -1,
# which means the column would be as wide as to display the whole text
pd.set_option('display.max_colwidth', -1)
movies_info


# ## Exporting the data to CSV (comma-separated values) and excel files

# In[35]:


# Write data to excel file
movies_info.to_excel("movies_info.xlsx", index = False, header = True)


# In[36]:


# or write data to CSV file
movies_info.to_csv("movies_info.csv", index = False, header = True)

