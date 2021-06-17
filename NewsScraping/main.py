import scrapy
from scrapy.crawler import CrawlerProcess
from get_proxies import get_verify_proxies

from spiders.mktwatch_spider import marketwatchSpider

# Start sqlite3 fix
# https://stackoverflow.com/questions/52291998/unable-to-get-results-from-scrapy-on-aws-lambda
import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
# End sqlite3 fix

def scraper_run(event):

    spider = event['spider']
    spider_class_name = spider.title()
    scrapy_class = globals()[spider]

    # Key parameter: Storage URI. An S3 link can be also created https://docs.scrapy.org/en/latest/topics/feed-exports.html#s3
    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_URI': '/tmp/result_crawling.json',
    })

    process.crawl(scrapy_class)
    process.start()

if __name__ == "__main__":
    # Step 1: The proxies are obtained online, verified and stored in the proxies_verified.txt file to be used by the spyder
    get_verify_proxies("https://www.marketwatch.com/markets", 'bloomberg_scraper/proxies_verified.txt')
    # Step 2: launch the spiders from the script
    event = {
        'spider': 'marketwatchSpider'
    }
    scraper_run(event)
