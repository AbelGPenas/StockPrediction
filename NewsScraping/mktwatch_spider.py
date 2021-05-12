import scrapy
from ..items import BloombergScraperItem
from scrapy.loader import ItemLoader
from scrapy.http import Request

class bloombergSpider(scrapy.Spider):
    name = "marketwatch"
    start_urls = ['https://www.marketwatch.com/markets?messageNumber=4929&channelId=10ac8992-673b-4dcc-b15d-3a55f1f3d061&position=1.1&partial=true']
    handle_httpstatus_list = [404]

    def parse(self, response):
        newsURLs = response.xpath('.//h3/a[@class="link"]/@href').extract()
        news_ids = response.xpath('.//div[@class="collection__elements j-scrollElement"]/div/@data-msgid').extract()
        for target_url in newsURLs:
            if target_url.find('https') != -1: #Ensure the string is a https url
                try:
                    yield Request(target_url, callback=self.scrape_new, meta={
                        'dont_retry': False,
                        'dont_merge_cookies': True
                        #,'priority': 1
                                  })
                except:
                    pass
        news_ids_int = [int(str_) for str_ in news_ids]
        if min(news_ids_int) > 5:
            next_id = min(news_ids_int)-1
            next_url = 'https://www.marketwatch.com/markets?messageNumber=' + str(next_id) + '&channelId=10ac8992-673b-4dcc-b15d-3a55f1f3d061&position=1.1&partial=true'
            yield response.follow(next_url, callback=self.parse, meta={
                    'dont_retry': False,
                    'dont_merge_cookies': True
                    #,'priority': 1
                              })

    def scrape_new(self, response):
        loader = ItemLoader(item=BloombergScraperItem(), response=response)
        loader.add_xpath('title', '//h1[@class="article__headline"]/text()')
        loader.add_xpath('body', '//div[@id="js-article__body"]/p/text() |//div[@id="js-article__body"]/p/a/text() |////div[@id="js-article__body"]/div/p/text() |//div[@id="js-article__body"]/div/p/a/text()')
        loader.add_xpath('first_paragraph', '//div[@id="js-article__body"]/p[1]/text() |//div[@id="js-article__body"]/p[1]/a/text()')
        loader.add_xpath('date', '//time/text()')
        yield loader.load_item()