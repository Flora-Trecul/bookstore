import scrapy
import hashlib

class CatspiderSpider(scrapy.Spider):
    name = "catspider"
    allowed_domains = ["furet.com"]
    start_urls = ["https://www.furet.com/"]

    def parse(self, response):
        books_cats_url = response.css("li.nav-livres a.level-top::attr(href)").get()
        yield scrapy.Request(books_cats_url, callback=self.parse_main_cats)
    
    def parse_main_cats(self, response):
        main_cats = response.css("a.navigation-block-container-title")
        for cat in main_cats:
            cat_url = cat.attrib["href"]
            yield response.follow(cat_url, callback=self.parse_all_cats, cb_kwargs={"breadcrumbs": ["Livres"]})
    
    def parse_all_cats(self, response, breadcrumbs):
        cat = response.css(".navigation-block-container--category:not(.navigation-block-container--ahead-category)")[0]
        cat_name = cat.css("h3::text").get().strip()
        cat_split_url = response.url.split("/")
        cat_url_id = f"{cat_split_url[2]}/{cat_split_url[-1]}"
    
        title_section = response.css(".cms-primary-title") or response.css(".nbr_result")
        page_title = title_section.css("span::text").get().strip()
        books_count = 0 if page_title == cat_name else title_section.xpath("text()").getall()[-1].strip()
        books_list = False if page_title == cat_name else True

        forbidden_words = ["réduit", "conteuses"]
        if all(word not in page_title.lower() for word in forbidden_words):
            yield {
                "cat_id": hashlib.md5(cat_url_id.encode("utf-8")).hexdigest(),
                "cat_name": page_title,
                "cat_url": response.url,
                "cat_parent": breadcrumbs[-1],
                "is_books_list": books_list,
                "books_count": books_count,
            }

        if page_title == cat_name:
            subcats = cat.css(".navigation-block-item--list li a")
            for subcat in subcats:
                subcat_url = subcat.attrib["href"]
                yield response.follow(subcat_url, callback=self.parse_all_cats, cb_kwargs={"breadcrumbs": breadcrumbs + [page_title]})