
import scrapy

class DrspiderSpider(scrapy.Spider):
    name = "drspider"
    allowed_domains = ["www.dr.com.tr"]
    start_urls = ["https://www.dr.com.tr/kategori/kitap"]

    def parse(self, response):
        parts = response.css("ul.js-facet-list.js-link-list li")

        for part in parts:
            href = part.css("a::attr(href)").get()
            if href:
                yield response.follow(
                    href,
                    callback=self.parse
                )

        products = response.css("div.prd-wrapper")

        for product in products:

            price = " ".join(
                product.css("div.prd-prices ::text").getall()
            ).strip()


            if not price:
                campaign_prices = product.css(
                    "div.campaign-price span::text"
                ).getall()
                price = campaign_prices[-1].strip() if campaign_prices else None

            yield {
                "name": product.css(
                    "div.prd-infos h3 a::text"
                ).get(default="").strip(),

                "creator": product.css(
                    "div.prd-infos h3 a::text"
                ).getall()[-1].strip(),

                "price": price,

                "url": response.urljoin(
                    product.css("a::attr(href)").get()
                )
            }

