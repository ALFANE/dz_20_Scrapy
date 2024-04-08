import scrapy
from scrapy import Request

from scrapy_workua.items import PersonItem


class WorkuaSpider(scrapy.Spider):
    name = "workua"
    allowed_domains = ["work.ua"]
    start_urls = [
        "https://www.work.ua/resumes-kharkiv/"
    ]

    site_url = 'https://work.ua'

    def parse(self, response):

        # print(response.body)
        for person in response.css('div.card.resume-link'):
            name = person.css('p.add-top-xs > span:nth-child(1)::text').get()
            if person.css('p.add-top-xs > span:nth-child(4)::text').get():
                age = person.css('p.add-top-xs > span:nth-child(3)::text').get()
            elif person.css('p.add-top-xs > span:nth-child(3)::text').get():
                age = person.css('p.add-top-xs > span:nth-child(2)::text').get()
            else:
                age = None
            place = person.css('div > h2 > a::text').get()

            people_item = PersonItem()
            people_item['name'] = name.strip()
            people_item['age'] = age.strip() if age else None
            people_item['place'] = place.strip()

            # print(response.css('div.card.resume-link > p.add-top-xs > span:nth-child(2)').getall())

            # yield people_item #yield позволяет парсить в циклеe
            if person.css('div.add-top-sm > h2 > a::attr(href)'):
                detail_page_url = person.css('div.add-top-sm > h2 > a::attr(href)').get()
            else:
                detail_page_url = person.css('div.add-top-exception > h2 > a::attr(href)').get()
            detail_page_url = self.site_url + detail_page_url
            yield Request(detail_page_url, self.parse_detail_page, meta={
                'people_item': people_item,
            })

        next_page_url = response.css('ul.pagination > li.no-style.add-left-default > a::attr(href)').getall()

        if next_page_url:
            next_page_url = self.site_url + next_page_url[-1]
            yield Request(next_page_url)


    def parse_detail_page(self, response):

        detail_info = response.css('p#addInfo::text').getall() #с помощью css
        # detail_info = response.xpath('//*[@id="addInfo"]/text()').getall() # c помощью xpath
        people_item = response.meta['people_item']
        people_item['detail_info'] = detail_info

        yield people_item
