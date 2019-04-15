import os
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CodeSpider(CrawlSpider):
    name = 'code'

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=(['div.code-result div h5 > a'])),
             callback='parse_item', follow=True),
    )

    def __init__(self, input_filename, output_directory, *args, **kwargs):
        super(CodeSpider, self).__init__(*args, **kwargs)
        self.input_filename = input_filename
        self.output_directory = output_directory

    def start_requests(self):
        self.create_directory(self.output_directory)
        with open(self.input_filename) as articles:
            for link in articles:
                link = link.strip()
                yield scrapy.Request(url=link, callback=self.parse)

    def parse_item(self, response):
        raw_file = response.css('a[rel="nofollow"][href!="#"][href!=""]::attr(href)').extract()[0]
        link = response.urljoin(raw_file)
        name = raw_file.split('/')[-1] + '.js'
        yield scrapy.Request(url=link, callback=self.parse_file, meta={'name': name})

    def parse_file(self, response):
        name = response.meta['name']
        with open(os.path.join(self.output_directory, name), 'w', encoding='utf-8') as f:
            f.write(response.text)

    def create_directory(self, directory_name):
        if not os.path.exists(directory_name):
            os.makedirs(directory_name, exist_ok=True)
