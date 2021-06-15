# Description
Spyder developed in scrapy to crawl news from marketwatch.com
# Relevant contents
## get_proxies.py
In the beginning of the scraping process https proxies are gathered from open source online, checked against the url targetted and stored if the responsiveness is satisfactory.
## mktwatch_spyder.py
Heart of the spyder, this script builds up the class with the custom methods to navigate through the resources online and scrape the desired pieces of information
## items.py
Defines the postprocessing steps for the information gathered before storing it.
