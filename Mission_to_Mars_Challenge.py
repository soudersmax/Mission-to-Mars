
# Import Splinter and BS
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
# searching for elements with a specific combination of tag (ul and li) and attribute (item_list and slide)
# Also telling browser to wait one second before searching for components to ensure all parts are loaded
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Set up HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')

# Assign slide_elem as the variable to look for the ul tag and it's "descendent", item_list and the same for li and slide
# CSS works from right to left, returning the last item instead of the first so the first output will be the li.slide
slide_elem = news_soup.select_one('ul.item_list li.slide')

# tell slide_elem to find the content title 
slide_elem.find("div", class_= 'content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click
#  is element present by text method searches for an element that has the provided text, wait 1s again for loading
# This would return a boolean
browser.is_element_present_by_text('more info', wait_time=1)

# find by partial text methjod takes the string we found and locates the link associated with it 
more_info_elem = browser.links.find_by_partial_text('more info')

# tell splinter to click
more_info_elem.click()

# Now that the page is loaded, parse it 
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
# figure.lede references the figure tag and it's class lede
# a is the next tag nested inside figure tag
# img tag is also nested here
# .get pulls the link to the image
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# add the base URL to create an absolute url
img_url = f'http://www.jpl.nasa.gov{img_url_rel}'
img_url

# ### Mars Facts

# instead of scraping each row (td) in the table, use pd read_html and store in df
# read_html searches for and returns a list of tables. By specifying index 0, we are getting the first it encounters
df = pd.read_html('http://space-facts.com/mars/')[0]

# assign columns to the new df
df.columns=['description','value']

# assign index
df.set_index('description', inplace=True)
df

# convert df back to html with pd.to_html()
facts_html = df.to_html()

# when setting 'description' to index, it introduces an extra cell to the left of value and the right of description. Since
# our html is now in string, I'm going to use regex to remove the characters that add those extra spaces for aesthetic
# purposes
import re
mars_facts = re.sub('(<th></th>\\n\s+<th>value</th>\\n\s+</tr>\\n\s+<tr>\\n)','<th>value</th>',facts_html)

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
products_list = browser.find_by_css('.description>a')
size = len(products_list)

for i in range(size):
    products_list = browser.find_by_css('.description>a')
    item = products_list[i]
    title = item.value
    item.click()
    img_url = browser.links.find_by_partial_href('/download/Mars/Viking')['href']
    hemispheres = {'img_url' : img_url, 'title' : title}
    hemisphere_image_urls.append(hemispheres)
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

