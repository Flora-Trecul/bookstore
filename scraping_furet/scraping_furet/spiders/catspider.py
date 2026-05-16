import scrapy

class CatspiderSpider(scrapy.Spider):
    name = "catspider"
    allowed_domains = ["furet.com"]
    start_urls = ["https://www.furet.com/"]

    def parse(self, response):
        books_cats_url = response.css("li.nav-livres a.level-top::attr(href)").get()
        yield response.follow(books_cats_url, callback=self.parse_books_cats)
    
    def parse_books_cats(self, response):
        pass