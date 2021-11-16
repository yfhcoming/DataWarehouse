import re

import scrapy

from amzSpider.items import AmzspiderItem


class amzSpider(scrapy.Spider):
    name = "amz"
    allowed_domains = ["amazon.com"]

    def start_requests(self):
        with open("pid.txt", 'r', encoding='utf-8') as pids:
            for pid in pids:
                pid = pid.strip()
                yield scrapy.Request(url='https://www.amazon.com/dp/' + pid,
                                     callback=self.parse,
                                     meta={'pid': pid,
                                           #    'cookiejar': random.randint(0, 31),
                                           #    'proxy': 'socks5://localhost:7891',
                                           },
                                     headers={
                                         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                         'Accept-Encoding': 'gzip, deflate, br',
                                         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6', })

    def parse(self, response):
        print("------------------parse done")
        pid = response.meta['pid']
        pi = AmzspiderItem()
        pi['pid'] = pid
        pi['otherFormat'] = []

        try:
            pi['title'] = response.xpath('//meta[@name="title"]/@content').extract()[0]

            if 'Prime Video' in pi['title']:

                otherFormatHrefs = response.xpath('//div[@data-automation-id="other-formats"]//a/@href').extract()
                for otherFormatHref in otherFormatHrefs:
                    asin = re.search('/dp/(\w+)/', otherFormatHref).group(1)
                    pi['otherFormat'].append(asin)

                pi['primeMeta'] = {}
                dts = response.xpath('//div[@id="meta-info"]//dl/dt')
                for dt in dts:
                    key = ''.join(dt.xpath('.//text()').extract())
                    value = ''.join(dt.xpath('../dd//text()').extract())
                    pi['primeMeta'][key] = value

                item =dict(
                    pid=pi['pid'],
                    title=pi['title'],
                    otherFormat=pi['otherFormat'],  # DVD, VHS Tape, etc.

                    primeMeta=pi['primeMeta'],  # only in prime video
                )

                yield item


            else:
                pi['productDetail'] = {}
                detailNames = response.xpath(
                    '//div[@id="detailBullets_feature_div"]/ul[contains(@class, "detail-bullet-list")]//span[@class="a-text-bold"]')
                for detailName in detailNames:
                    key = detailName.xpath('.//text()').extract()[0][:-7]
                    value = detailName.xpath('../span[last()]/text()').extract()[0]
                    pi['productDetail'][key] = value

                pi['format'] = response.xpath('//div[@id="bylineInfo"]/span[last()]/text()').extract()[0]

                otherFormatHrefs = response.xpath(
                    "//li[contains(@class, 'swatchElement')]//a[@href!='javascript:void(0)']/@href").extract()
                for otherFormatHref in otherFormatHrefs:
                    asin = re.search('/dp/(\w+)/', otherFormatHref).group(1)
                    pi['otherFormat'].append(asin)

                pi['additionalOptions'] = []
                additionalOptionHrefs = response.xpath(
                    "//div[contains(@class, 'top-level')]//span/@data-tmm-see-more-editions-click").extract()
                additionalOptionHrefs = list(filter(lambda x: '"metabindingUrl":"#"' not in x, additionalOptionHrefs))
                for additionalOptionHref in additionalOptionHrefs:
                    asin = re.search('/dp/(\w+)/', additionalOptionHref).group(1)
                    pi['additionalOptions'].append(asin)

                item = dict(
                    pid=pi['pid'],
                    title=pi['title'],
                    otherFormat=pi['otherFormat'],  # DVD, VHS Tape, etc.
                    #
                    # primeMeta=pi['primeMeta'],  # only in prime video

                    format=pi['format'],
                    productDetail=pi['productDetail'],
                    additionalOptions=pi['additionalOptions'],  # DVD1, DVD2, etc.
                )
                yield item
        except:
            pass

