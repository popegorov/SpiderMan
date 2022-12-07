import scrapy
from spider_steam.items import SpiderSteamItem


class SteamproductspiderSpider(scrapy.Spider):
    name = 'SteamProductSpider'
    allowed_domains = ['store.steampowered.com']
    start_urls = []

    for category in ['indie', 'strategy', 'minecraft']:
        for i in (1, 3):
            cur_link = "https://store.steampowered.com/search/?g=n&SearchText=" + category + "&page=" + str(i)
            start_urls.append(cur_link)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        games = response.css('a[class = "search_result_row ds_collapse_flag "]::attr(href)').extract()
        for link in games:
            if 'agecheck' in link:
                continue
            yield scrapy.Request(link, callback=self.parse_game)

    def parse_game(self, response):
        cur_game = SpiderSteamItem()

        try:
            cur_game['name'] = response.css('div.blockbg a span::text').get().strip()

            length = len(response.css('span.responsive_hidden::text'))
            cur_game['reviews_count'] = response.css('span.responsive_hidden::text')[length - 2].get().strip()[
                                     1:-1]
            cur_game['average_assessment'] = response.css('span.game_review_summary::text')[1].get().strip()
            cur_game['release_date'] = response.css('div.grid_date::text')[1].get().strip()
            cur_game['founder'] = response.css('div.grid_content a::text')[0].get().strip()
            cur_game['price'] = response.css('div.game_purchase_price::text').get().strip()

            category = ''
            length = len(response.css('div.blockbg a::text'))
            for i in range(1, length):
                category += response.css('div.blockbg a::text')[
                                i].get().strip() + "->"
            cur_game['category'] = category[:len(category) - 3]

            tags = ''
            length = len(response.css('div.popular_tags a::text'))
            for i in range(length):
                tags += response.css('div.popular_tags a::text')[
                            i].get().strip() + ", "
            cur_game['tags'] = tags[:(len(tags) - 3)]

            platforms = set()
            for platform in response.css('div').xpath('@data-os'):
                platforms.add(platform.get().strip())
            cur_game['available_platforms'] = list(platforms)
            if cur_game['release_date'][-4::] > '2000':
                yield cur_game
            else:
                yield
        except:
            yield
