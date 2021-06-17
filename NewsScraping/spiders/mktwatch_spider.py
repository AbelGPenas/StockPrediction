import scrapy
from ..items import MarketwatchScraperItem
from scrapy.loader import ItemLoader
from scrapy.http import Request
from w3lib.html import remove_tags, strip_html5_whitespace
import datetime, re

class marketwatchSpider(scrapy.Spider):
    name = "Marketwatch"
    start_urls = ['https://www.marketwatch.com/markets?messageNumber=20000&channelId=10ac8992-673b-4dcc-b15d-3a55f1f3d061&position=1.1&partial=true']
    handle_httpstatus_list = [404]

    def parse(self, response):
        newsURLs = response.xpath('.//h3/a[@class="link"]/@href').extract()
        news_ids = response.xpath('.//div[@class="collection__elements j-scrollElement"]/div/@data-msgid').extract()
        for target_url in newsURLs:
            if target_url.find('https') != -1: #Ensure the string is a https url
                try:
                    yield Request(target_url, callback=self.scrape_new, meta={
                        'dont_retry': False,
                        'dont_merge_cookies': True,
                        'priority': 1
                                  })
                except:
                    pass
        news_ids_int = [int(str_) for str_ in news_ids]
        if news_ids_int:
            if min(news_ids_int) > 5:
                next_id = min(news_ids_int)-1
                next_url = 'https://www.marketwatch.com/markets?messageNumber=' + str(next_id) + '&channelId=10ac8992-673b-4dcc-b15d-3a55f1f3d061&position=1.1&partial=true'
                yield response.follow(next_url, callback=self.parse, meta={
                        'dont_retry': False,
                        'dont_merge_cookies': True,
                        'priority': 2
                                  })

    def scrape_new(self, response):

        # Check the date of the new
        str_date = strip_html5_whitespace(remove_tags(response.xpath('//time/text()').extract()[0]))
        # Select the second group in the regex, this will return a string i.e. "March 19"
        str_date = re.search(r'd: (.*?), 2021', str_date)[0]
        formatted_date = datetime.datetime.strptime(str_date, 'd: %B %d, %Y')
        # Check how long ago was the new published
        new_lag = datetime.datetime.today() - formatted_date
        # Close the spider if the scraped news are older than one week
        if new_lag > datetime.timedelta(days=7):
            raise scrapy.exceptions.CloseSpider()
        else:
            # Load the items thorugh the class created in items.py (handling the processing)
            loader = ItemLoader(item= MarketwatchScraperItem(), response=response)
            loader.add_xpath('title', '//h1[@class="article__headline"]/text()')
            loader.add_xpath('body', '//div[@id="js-article__body"]/p/text() |//div[@id="js-article__body"]/p/a/text() |////div[@id="js-article__body"]/div/p/text() |//div[@id="js-article__body"]/div/p/a/text()')
            loader.add_xpath('first_paragraph', '//div[@id="js-article__body"]/p[1]/text() |//div[@id="js-article__body"]/p[1]/a/text()')
            loader.add_xpath('date', '//time/text()')
            yield loader.load_item()
