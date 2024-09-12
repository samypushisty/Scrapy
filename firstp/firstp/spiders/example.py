from pathlib import Path
import scrapy


class ExampleSpider(scrapy.Spider):
    # 145
    count_pages = 145
    href = ""
    name = "example"
    allowed_domains = ["catalog.onliner.by"]
    start_url = "https://catalog.onliner.by/pan"


    def start_requests(self):
        start_url_in = self.start_url
        urls = [start_url_in+"?page="*bool(i)+str(i) for i in range(self.count_pages+1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pans = response.xpath("//a[@class='catalog-form__link "
                              "catalog-form__link_primary-additional "
                              "catalog-form__link_base-additional "
                              "catalog-form__link_font-weight_semibold "
                              "catalog-form__link_nodecor']")
        for pan in pans:
            self.href = pan.xpath(".//@href").get().strip()
            yield response.follow(pan.xpath(".//@href").get().strip(), callback=self.parse_page,
                             cb_kwargs=dict(href=pan.xpath(".//@href").get().strip()))
            # yield {
            # 'title': pan.xpath("text()").get().strip(),
            # 'href': pan.xpath(".//@href").get().strip()
            # }

    def parse_page(self, response,href):
        yield {"title":response.xpath("//h1[@class='catalog-masthead__title js-nav-header']/text()").get().strip(),
               "href":href,
               "price":response.xpath("//a[@class='offers-description__link offers-description__link_nodecor js-description-price-link']/text()").get().strip()[:-3]+"р",
               "discription":response.xpath("//div[@class='offers-description__specs']/p/text()").get().strip()
               }



# scrapy crawl example -o titles.json