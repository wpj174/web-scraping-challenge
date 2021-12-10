# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
import time


def scrape():
    mars_data = dict()

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #############
    # Mars News #
    #############

    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    #display the current title content
    #slide_elem.find('div', class_='content_title') <- not needed for scrape function

    # Use the parent element to find the first a tag and save it as `news_title`
    # ^ -- This doesn't make any sense.  There is no a tag associated with the article title

    news_title = slide_elem.find('div', class_='content_title').text

    # Use the parent element to find the paragraph text

    news_p = slide_elem.find('div', class_='article_teaser_body').text

    # Add to the mars_data dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

    ##################
    # Featured Image #
    ##################

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    browser.links.find_by_partial_text('FULL').click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find the relative image url
    image = img_soup.find('img', class_='fancybox-image')
    img_url_rel = image['src']

    # Use the base url to create an absolute url
    img_url = url + img_url_rel

    # Add to the mars_data dictionary
    mars_data['feat_img_url'] = img_url

    ##############
    # Mars Facts #
    ##############

    # Visit Galaxy Facts site
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    # Use `pd.read_html` to pull the data from the Mars-Earth Comparison section
    # hint use index 0 to find the table
    tables = pd.read_html(url)
    mf_df = tables[0]
    #mf_df
    #mf_df.to_html()

    # Add to the mars_data dictionary
    mars_data['table_df'] = mf_df

    ####################
    # Mars Hemispheres #
    ####################

    # Visit marshemispheres.com website
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    links = browser.find_by_css('a.product-item img')

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        
        # We have to find the elements on each pass of the loop to avoid a stale element exception
        links = browser.find_by_css('a.product-item img')
        links[i].click()
        
        # Next, we find the Sample image anchor tag and extract the href
        html = browser.html
        hem_soup = soup(html, 'html.parser')
        
        details = hem_soup.find_all('dd')
        hires_link = details[1].a['href']
        
        hem = dict()
        hem['img_url'] = url + hires_link
        
        # Get Hemisphere title
        hem['title'] = hem_soup.find('h2', class_='title').text
        
        # Append hemisphere object to list
        hemisphere_image_urls.append(hem)
        
        
        # Finally, we navigate backwards
        browser.back()

    # Add to mars_data dictionary
    mars_data['hem_imgs'] = hemisphere_image_urls

    ################
    # Done Sraping #
    ################

    # Close browser
    browser.quit()

    # Return the data
    return mars_data
