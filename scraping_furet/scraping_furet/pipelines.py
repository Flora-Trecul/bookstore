# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CategoriesPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        count_string = adapter.get("books_count")
        if count_string != 0:
            count_value = count_string.split(" ")[0].replace("(", "")
            adapter["books_count"] = int(count_value)
        
        return item