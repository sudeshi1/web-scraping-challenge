from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
mars_db = mongo.db.mars

@app.route("/")
def home():
    scraped_data = mars_db.find_one()
    #print(scraped_data["hemisphere_images"])
    return render_template("index.html", mars = scraped_data)

@app.route("/scrape")
def scrape_all():
    mars_dict = scrape.scrape_all()
    ##mars_dict.insert_one(mars_data)
    mars_db.update_one({}, {"$set": mars_dict}, upsert=True)
    return redirect("/", code = 302)


if __name__ == "__main__":
    app.run()



