import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from ibbde.items import Article


class IbbdeSpider(scrapy.Spider):
    name = 'ibbde'
    start_urls = ['https://www.ibb.de/de/ueber-die-ibb/aktuelles/presse/pressemitteilungen/pressemitteilungen.html']

    def parse(self, response):
        links = response.xpath('//h3/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//h3/text()').get()
        if date:
            date = date.split()[0]

        content = response.xpath('//section[@class="col-md-16 mainContent"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
