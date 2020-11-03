from flask import Flask, render_template
# Import scrape_mars
import scrape_mars

import pymongo

app = Flask(__name__)

# Creating connection variable
connection = 'mongodb://localhost:27017/mission_to_mars'

client = pymongo.MongoClient(connection)


@app.route("/")
def index():
    mars = client.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape 
@app.route("/scrape")
def scrape():
    mars = client.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data)
    return "Scraped!"

if __name__ == "__main__":
    app.run(debug=True)
