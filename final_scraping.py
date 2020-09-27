# Import Splinter and BS
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Define Scrape_All
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    # Set news titles and paragraph variables 
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "image_list": hemisphere_images(browser),
      "last_modified": dt.datetime.now()      
      }
    # Stop webdriver and return data
    browser.quit()
    return data

# Define function to contain the steps of the scraping
def mars_news(browser):
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

    # Error handling for most common type of error AttributeError
    try: 
        # Assign slide_elem as the variable to look for the ul tag and it's "descendent", item_list and the same for li and slide
        # CSS works from right to left, returning the last item instead of the first so the first output will be the li.slide
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # tell slide_elem to find the content title 
        slide_elem.find("div", class_= 'content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    # function return statement
    return news_title, news_p

# ### Featured Images
# Define and declare function
def featured_image(browser):
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

    # Error handling
    try:
        # find the relative image url
        # figure.lede references the figure tag and it's class lede
        # a is the next tag nested inside figure tag
        # img tag is also nested here
        # .get pulls the link to the image
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None

    # add the base URL to create an absolute url
    img_url = f'http://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url 

# ### Mars Facts
def mars_facts():
    try:
        # instead of scraping each row (td) in the table, use pd read_html and store in df
        # read_html searches for and returns a list of tables. By specifying index 0, we are getting the first it encounters
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    # assign columns to the new df
    df.columns=['description','value']

    # assign index
    df.set_index('description', inplace=True)
    
    return df.to_html()

def hemisphere_images(browser):
    # Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Create a list to hold the images and titles.
    hemisphere_images = []
    # Write code to retrieve the image urls and titles for each hemisphere.
    products_list = browser.find_by_css('.description>a')
    size = len(products_list)
    for i in range(size):
        products_list = browser.find_by_css('.description>a')
        item = products_list[i]
        title = item.value
        item.click()
        img_url = browser.links.find_by_partial_href('/download/Mars/Viking')['href']
        hemispheres = {'img_url' : img_url, 'title' : title}
        hemisphere_images.append(hemispheres)
        browser.back()
    #Print the list that holds the dictionary of each image url and title.
    return hemisphere_images


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
