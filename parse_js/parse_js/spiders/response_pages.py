import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class PagesSpider(CrawlSpider):
    name = 'pages'

    page_links = set()

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=(['div.search-pagination ul li:last-child a'])),
             callback='parse_start_url', follow=True),
    )

    def __init__(self, output_filename, query, *args, **kwargs):
        super(PagesSpider, self).__init__(*args, **kwargs)
        self.output_filename = output_filename
        self.query = query

    def start_requests(self):
        url = f'https://searchcode.com/?lan=22&q={self.query}&src=2&src=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse_start_url(self, response):
        links = response.css('div.search-pagination ul li a::attr(href)').extract()[1:]
        for link in links:
            link = response.urljoin(link)
            self.page_links.add(link)

    def closed(self, reason):
        with open(self.output_filename, 'w') as f:
            for link in self.page_links:
                f.write(f'{link}\n')
