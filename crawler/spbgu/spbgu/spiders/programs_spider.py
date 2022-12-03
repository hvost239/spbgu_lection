import scrapy
import w3lib.html


class ProgramSpider(scrapy.Spider):
    name = "program"

    def start_requests(self):
        start_urls = [
            'https://spbu.ru/postupayushchim/programms/bakalavriat',
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_main)

    def parse_program(self, response):
        title = response.css("title::text")[0].get()
        url = response.url

        print(title)

        content = response.css("main").getall()
        content_without_tags = w3lib.html.remove_tags(str(content))
        words = content_without_tags.split()
        words = set([w.lower() for w in words if w.isalpha()])
        with open("out/{}.dat".format(title), 'w') as f:
            f.write("\n".join(words))

    def parse_main(self, response):
        for page in response.css('a.card-program::attr(href)').getall():
            next_page = response.urljoin(page)
            yield scrapy.Request(next_page, callback=self.parse_program)
