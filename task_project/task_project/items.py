import scrapy


class TaskProjectItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    color = scrapy.Field()
    available_colors = scrapy.Field()
    reviews_count = scrapy.Field()
    reviews_score = scrapy.Field()
    pass
