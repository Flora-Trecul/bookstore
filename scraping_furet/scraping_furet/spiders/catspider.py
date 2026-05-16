import scrapy
import hashlib
from scraping_furet.items import CategoryItem

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
        # On récupère la div qui suit le commentaire "START Menu Categorie courante" pour conserver uniquement le menu de la catégorie en cours
        cat = response.xpath("//comment()[contains(., 'START Menu Categorie courante')]/following-sibling::div[1]")
        cat_name = cat.css("h3::text").get().strip()
        cat_split_url = response.url.split("/")
        cat_url_id = f"{cat_split_url[2]}/{cat_split_url[-1]}"
    
        title_section = response.css(".cms-primary-title") or response.css(".nbr_result")
        page_title = title_section.css("span::text").get().strip()
        is_final_subcat = False if page_title == cat_name else True
        books_count = 0 if not is_final_subcat else title_section.xpath("text()").getall()[-1].strip()


        cat_item = CategoryItem()
        cat_item["category_id"] = hashlib.md5(cat_url_id.encode("utf-8")).hexdigest()
        cat_item["category_name"] = page_title
        cat_item["category_url"] = response.url
        cat_item["category_parent"] = breadcrumbs[-1]
        cat_item["is_books_list"] = is_final_subcat
        cat_item["books_count"] = books_count
        yield cat_item


        if not is_final_subcat:
            subcats = cat.css(".navigation-block-item--list li a")
            for subcat in subcats:
                subcat_url = subcat.attrib["href"]
                subcat_name = subcat.css("::text").get()
   
                # On exclut les pages Conteuses (pas des livres) et Livres à prix réduit (pour éviter les doublons)
                forbidden_words = ["réduit", "conteuses"]
                if all(word not in subcat_name.lower() for word in forbidden_words):
                    yield response.follow(subcat_url, callback=self.parse_all_cats, cb_kwargs={"breadcrumbs": breadcrumbs + [page_title]})