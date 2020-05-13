from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrapping_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
@app.route("/")
def index():
    mars_results = mongo.db.mars_results.find_one()
    print(mars_results)
    return render_template("index.html", mars_results=mars_results)

@app.route("/scrape")
def scraper():
    mars_results = mongo.db.mars_results
    mars_data = scrapping_mars.scrape()
    mars_results.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
