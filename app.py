from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create an instance of Flask
app = Flask(__name__)

# use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# route to render index.html template using data from Mongo
@app.route("/")
def home():
    # find one record of data from the mongo database
    mars = mongo.db.marsinfo.find_one()
    
    # return template and data
    return render_template("index.html", mars=mars)

# route to trigger the scrape function
@app.route("/scrape")
def scrape():
    
    # run the scrape function
    mars_data = scrape_mars.scrape()
    print(mars_data)
    
    # update the Mongo database
    mongo.db.marsinfo.update({}, mars_data, upsert=True)

    
    # redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
