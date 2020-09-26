# Import dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import final_scraping

# Set up flask 
app = Flask(__name__)

# Set up Mongo
# Use flask_pymongo to set up mongo connection (app.config tells python that the app will connect to mongoo using URI)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set up app routes

# home page (index.html)
@app.route("/")
def index():

    # use pymongo to find mars collection in db
   mars = mongo.db.mars.find_one()
   # return html template using the index.html file and tell python to use the mars collection in mongo db
   return render_template("index.html", mars=mars)

# scrape route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = final_scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run()