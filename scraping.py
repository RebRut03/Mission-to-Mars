# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_data": hemisphere_data(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Set up Splinter
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)

# Refactor by Defining function; we're telling Python that we'll 
# be using the browser variable we defined outside the function. 
# All of our scraping code utilizes an automated browser, 
# and without this section, our function wouldn't work.
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # Optional delay for loading the page; The optional delay is useful because 
    #sometimes dynamic pages take a little while to load, especially if they are image-heavy.
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
  

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
   
    return img_url


#create a new DataFrame from the HTML table. Pandas function read_html() searches for and returns a list of tables 
#found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, 
#or the first item in the list. Then, it turns the table into a DataFrame.
#df = pd.read_html('https://galaxyfacts-mars.com')[0]
#assign columns to the new DataFrame for additional clarity.
#df.columns=['description', 'Mars', 'Earth']
#By using the .set_index() function, we're turning the Description column into the DataFrame's index. 
#inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
#df.set_index('description', inplace=True)
#df
#Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function.
#df.to_html()

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]


    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

#create function to scrape hemisphere data

def hemisphere_data(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    
    try:
        # 2. Create a list to hold the images and titles.
        hemisphere_image_urls = []


        # Create for loop to iterate through hemisphere images
        for i in range(0, 4):

            hemispheres = {}

            # Click on hemisphere link while navigating to full res image

            hemisphere_page = browser.find_by_css('.thumb')[i]
            hemisphere_page.click()

            # Parse pages
            html = browser.html
            img_soup = soup(html, 'html.parser')

            # 3. Write code to retrieve the image urls and titles for each hemisphere.

            # full res image code

            element1 = img_soup.find('li')
            hreflink = element1.find('a', target='_blank')['href']
            img_url = ('https://marshemispheres.com/'+ hreflink)
            print(hreflink)
            print(img_url)

            # title code
            title = img_soup.find('h2', class_= 'title').text
            print(title)

            hemispheres['img_url'] = img_url
            hemispheres['title'] = title

            hemisphere_image_urls.append(hemispheres)

            browser.back()
    
    except AttributeError:
        return None
    
      
    return hemisphere_image_urls


# end the automatic browser
#browser.quit()

#This last block of code tells Flask that our script is complete 
# and ready for action. The print statement will print 
# out the results of our scraping to our terminal after 
# executing the code.

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())



