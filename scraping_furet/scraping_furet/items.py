# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CategoryItem(scrapy.Item):
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    category_url = scrapy.Field()
    category_parent = scrapy.Field()
    is_books_list = scrapy.Field()
    books_count = scrapy.Field()
