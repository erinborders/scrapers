import scrapy

class AtlantaRestaurants(scrapy.Spider):
    name = 'atlanta'

    start_urls = [
        'https://www.whereyoucamefrom.biz/restaurants/atlanta'
    ]

    def parse(self, response):
        for post in response.css('.summary-item'):
            business_name = post.css('.summary-title a::text').get()
            if business_name is None:
                business_name = post.css('.title::text').get()
            yield {
                'businessname': business_name,
                'businessaddress': post.css('.summary-address::text').get()
            }

        next_page = response.css('a.item-pagination::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
