from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page; tells Flask what to display 
# when we're looking at the home page, index.html 
# (index.html is the default HTML file that we'll use to display
# the content we've scraped). This means that when we visit our 
# web app's HTML page, we will see the home page
@app.route("/")
# create def index function; links our visual representation of 
# our work, our web app, to the code that powers it.
def index():
# uses PyMongo to find the "mars" collection in our database, 
# which we will create when we convert our Jupyter 
# code to Python Script. assign that path to the
# mars variable for use later.
   mars = mongo.db.mars.find_one()
   # tells Flask to return an HTML template using 
   # an index.html file; tells Python to use the "mars" 
   # collection in MongoDB.
   return render_template("index.html", mars=mars)

# next function will set up our scraping route. 
# This route will be the "button" of the web application, 
# the one that will scrape updated data when we tell it to 
# from the homepage of our web app. It'll be tied to a button 
# that will run the code when it's clicked.

#@app.route(“/scrape”) defines the route that Flask will be using. 
# This route, “/scrape”, will run the function that we create
# just beneath it.
@app.route("/scrape")
# The next lines allow us to access the database, scrape new data 
# using our scraping.py script, update the database, 
# & return a message when successful. define it with def scrape(): 
def scrape():
   # assign a new variable that points to our Mongo database 
   mars = mongo.db.mars
   # created a new variable to hold the newly scraped data
   mars_data = scraping.scrape_all()
   # Now that we've gathered new data, we need to update 
   # the database using .update(query_parameter, data, options)
   #We're inserting data, so first we'll need to add an empty 
   # JSON object with {} in place of the query_parameter
   # Next, we'll use the data we have stored in mars_data
   # the option we'll include is upsert=True. This indicates 
   # to Mongo to create a new document if one doesn't already exist, 
   # and new data will always be saved (even if we haven't already 
   # created a document for it).
   mars.update({}, mars_data, upsert=True)
   # Finally, we will add a redirect after successfully scraping 
   # the data: return redirect('/', code=302). This will navigate 
   # our page back to / where we can see the updated content.
   return redirect('/', code=302)

# Tell Flask to run
if __name__ == "__main__":
   app.run()