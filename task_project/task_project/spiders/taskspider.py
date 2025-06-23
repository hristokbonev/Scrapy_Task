import scrapy
from scrapy_playwright.page import PageMethod
import json


class PlaywrightSpider(scrapy.Spider):
    name = "task_spider"
    allowed_domains = ["www2.hm.com"]
    intercepted_data = []

    def start_requests(self):
        yield scrapy.Request(
            "https://www2.hm.com/bg_bg/productpage.1274171085.html",
            headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/114.0.0.0 Safari/537.36'},
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("on", "response", self.handle_response),
                    PageMethod("wait_for_selector", "text=КОМЕНТАРИ"),
                    PageMethod("click", "text=КОМЕНТАРИ"),
                    PageMethod("wait_for_timeout", 2000),
                    ]
            },
            callback=self.parse,
        )

    '''
      We're looking for a response which has 'reviews' in the URL
      H&M's website loads reviews data as a separate request
    '''
    async def handle_response(self, response):
        if "reviews?sort" in response.url.lower():
            body = await response.text()
            self.intercepted_data.append({
                'body': body,
            })


    async def parse(self, response):
    
        script_data = response.css('script#__NEXT_DATA__::text').get()
        data = json.loads(script_data)

        product_article_details = data.get('props', {}).get('pageProps', {}).get('productPageProps', {}).get('aemData', {}).get('productArticleDetails', {})
        name = product_article_details.get('productName', 'No name found')
        price = product_article_details.get('variations', {}).get('1274171085', {}).get('whitePriceValue', 'No price found')
        color = product_article_details.get('variations', {}).get('1274171085', {}).get('name', 'No color found')
        variations = product_article_details.get('variations', {})
        available_colors = set()

        for product in variations.values():
            if 'name' in product:
                available_colors.add(product['name'])

        available_colors = sorted(available_colors)
        
        # Reviews data comes from an intercepted response
        reviews_data = self.intercepted_data[0]['body']
        reviews_data = json.loads(reviews_data)
        reviews_count = reviews_data.get('reviews', [])[0].get('catalogItems', [])[0].get('ratingCount', 0)
        reviews_score = reviews_data.get('reviews', [])[0].get('catalogItems', [])[0].get('averageRating', 0)


        yield {
            'name': name,
            'price': price,
            'color': color,
            'available_colors': available_colors,
            'reviews_count': reviews_count,
            'reviews_score': reviews_score
        }