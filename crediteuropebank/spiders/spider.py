import scrapy

from scrapy.loader import ItemLoader
from ..items import CrediteuropebankItem
from itemloaders.processors import TakeFirst


class CrediteuropebankSpider(scrapy.Spider):
	name = 'crediteuropebank'
	start_urls = ['https://www.crediteuropebank.com/the-bank.html']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="header"]/h1/text()').get()
		description = response.xpath('//div[@class="content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="news-single-rightbox"]/text()').get()

		item = ItemLoader(item=CrediteuropebankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
