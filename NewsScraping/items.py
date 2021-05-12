# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from w3lib.html import remove_tags, strip_html5_whitespace
import scrapy
from itemloaders.processors import MapCompose, Join
import re

def process_date(value):
    return re.sub(r'Published:', r'', value)

class BloombergScraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace)
    )
    date = scrapy.Field(
        input_processor=MapCompose(process_date, strip_html5_whitespace)
    )
    body = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_html5_whitespace),
        output_processor=Join()
    )
    first_paragraph = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_html5_whitespace),
        output_processor=Join()
    )