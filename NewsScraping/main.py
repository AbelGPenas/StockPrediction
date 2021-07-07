import scrapy
import imp
from scrapy.crawler import CrawlerProcess
from bloomberg_scraper.get_proxies import get_verify_proxies

from bloomberg_scraper.spiders.mktwatch_spider import marketwatchSpider

# Start sqlite3 fix
# https://stackoverflow.com/questions/52291998/unable-to-get-results-from-scrapy-on-aws-lambda
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
# End sqlite3 fix


if __name__ == "__main__":
    # Step 1: The proxies are obtained online, verified and stored in the proxies_verified.txt file to be used by the spyder
    # get_verify_proxies("https://www.marketwatch.com/markets", 'bloomberg_scraper/proxies_verified.txt')
    # Step 2: launch the spiders from the script
    process = CrawlerProcess()

    process.crawl(marketwatchSpider)
    process.start()
