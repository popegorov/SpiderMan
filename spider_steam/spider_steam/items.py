import scrapy


class SpiderSteamItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    reviews_count = scrapy.Field()
    average_assessment = scrapy.Field()
    release_date = scrapy.Field()
    founder = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    available_platforms = scrapy.Field()
