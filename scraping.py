# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page; The optional delay is useful because 
#sometimes dynamic pages take a little while to load, especially if they are image-heavy.
browser.is_element_present_by_css('div.list_text', wait_time=1)



#set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
#Notice how we've assigned slide_elem as the variable to look for the <div /> tag and 
#its descendent (the other tags within the <div /> element)? This is our parent element. 
#This means that this element holds all of the other elements within it, and 
#we'll reference it when we want to filter search results even further. 
#The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag 
#with the class of list_text. CSS works from right to left, such as returning the last item on the list instead of the first.
#Because of this, when using select_one, the first matching element returned will be a <li /> element
#with a class of slide and all nested elements within it.



#In this line of code, we chained .find onto our previously assigned variable, slide_elem. When we do this, 
#we're saying, "This variable holds a ton of information, so look inside of that information to find this specific data.
#" The data we're looking for is the content title, which we've specified by saying, "The specific data is in a <div /> 
#with a class of 'content_title'."
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
#We've added something new to our .find() method here: .get_text(). When this new method is chained onto .find(), 
#only the text of the element is returned. The code above, for example, would return only the title of 
#the news article and not any of the HTML tags or elements.


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p
#.find() is used when we want only the first class and attribute we've specified.


# ### Featured Images



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
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
#An img tag is nested within this HTML, so we've included it.
#.get('src') pulls the link to the image.
#What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image. 
#Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."




# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url
#We're using an f-string for this print statement because it's a cleaner way to create print statements; 
#they're also evaluated at run-time. This means that it, and the variable it holds, doesn't exist until the code
#is executed and the values are not constant. This works well for our scraping app because the data we're scraping
#is live and will be updated frequently.




#create a new DataFrame from the HTML table. Pandas function read_html() searches for and returns a list of tables 
#found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, 
#or the first item in the list. Then, it turns the table into a DataFrame.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
#assign columns to the new DataFrame for additional clarity.
df.columns=['description', 'Mars', 'Earth']
#By using the .set_index() function, we're turning the Description column into the DataFrame's index. 
#inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df.set_index('description', inplace=True)
df



#Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function.
df.to_html()




# end the automatic browser
browser.quit()





