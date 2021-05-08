import os
import crochet
crochet.setup()

from flask import Flask , render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time
from ProductReview.spiders.amazon import AmazonSpider
from ProductReview.spiders.flipkart import FlipkartSpider
from ProductReview.spiders.paytmmall import PaytmmallSpider

app = Flask(__name__)

output_data = []
crawl_runner = CrawlerRunner()

@app.route('/')
def index():
    return render_template("index.html")

# After clicking the Submit Button FLASK will come into this
@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        s = request.form['main_url'] # Getting the Input Amazon Product URL
        global baseURL
        baseURL = s
        if 'amazon' in baseURL:
            if os.path.exists("amazon/outputfile.json"): 
                os.remove("amazon/outputfile.json")
        elif 'flipkart' in baseURL:
            if os.path.exists("flipkart/outputfile.json"): 
                os.remove("flipkart/outputfile.json")
        elif 'paytmmall' in baseURL:
            if os.path.exists("paytmmall/outputfile.json"): 
                os.remove("paytmmall/outputfile.json")
        else:
            pass
        return redirect(url_for('scrape')) # Passing to the Scrape function


@app.route("/scrape")
def scrape():
    scrape_with_crochet(baseURL=baseURL) # Passing that URL to our Scraping Function
    time.sleep(20) # Pause the function while the scrapy spider is running    
    return jsonify(output_data) # Returns the scraped data after being running for 20 seconds.

@crochet.run_in_reactor
def scrape_with_crochet(baseURL):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    if 'amazon' in baseURL:
        eventual = crawl_runner.crawl(AmazonSpider, category = baseURL)
    elif 'flipkart' in baseURL:
        eventual = crawl_runner.crawl(FlipkartSpider, category = baseURL)
    elif 'paytmmall' in baseURL:
        eventual = crawl_runner.crawl(PaytmmallSpider, category = baseURL)
    else:
        pass
    return eventual

#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))

if __name__== "__main__":
    app.run(debug=True)