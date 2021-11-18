import re
import calendar

import scrapy

from amzSpider.items import AmzspiderItem


class amzSpider(scrapy.Spider):
    name = "amz"
    allowed_domains = ["amazon.com"]

    def start_requests(self):
        # ok = set()
        # bad = set()
        # try:
        #     with open('pidok.txt', 'r', encoding='utf-8') as pidok:
        #         for pid in pidok:
        #             ok.add(pid.strip())
        #     with open('pidbad.txt', 'r', encoding='utf-8') as pidbad:
        #         for pid in pidbad:
        #             bad.add(pid.strip())
        # except:
        #     pass
        with open("pid.txt", 'r', encoding='utf-8') as pids:
            for pid in pids:
                pid = pid.strip()
                # if pid in ok or pid in bad:
                #     continue
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
        print("------------------parse start")
        pid = response.meta['pid']
        pi = AmzspiderItem()
        pi['pid'] = pid
        pi['title'] = response.xpath('//meta[@name="title"]/@content').extract()[0]

        try:

            if 'Prime Video' in pi['title']:

                pi['otherFormat'] = []
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

                pi['primeDetail'] = {}
                dts = response.xpath('//*[@id="btf-product-details"]//dl/dt')
                for dt in dts:
                    key = ''.join(dt.xpath('.//text()').extract())
                    value = ''.join(dt.xpath('../dd//text()').extract())
                    pi['primeDetail'][key] = value

                commentList = []
                commentInfos = response.xpath('//*[@id="customer-review-section"]//div[contains(@data-automation-id,"review-item")][position()<=2]')
                for commentInfo in commentInfos:
                    # reviewerId = commentInfo.xpath('./@id').extract()[0]
                    reviewerName = commentInfo.xpath('./div[1]/a/span//text()').extract()[0]
                    overall = commentInfo.xpath('./div[2]/span/span//span//text()').extract()[0][0:3]
                    reviewTime = commentInfo.xpath('./div[1]/span[last()]//text()').extract()[0]
                    reviewTime = reviewTime.split('on')[1][1:]
                    # reviewTime = reviewTime.split(' ')
                    # reviewTime[0] = list(calendar.month_name).index(reviewTime[0])
                    # reviewTime[1] = reviewTime[0]
                    # Time = reviewTime[0]+' '+reviewTime[1]+' '+reviewTime[2]
                    reviewTextSpan = commentInfo.xpath('./div[3]//div[@dir="auto"]')
                    reviewText = reviewTextSpan.xpath('string(.)').extract()[0]
                    summary = commentInfo.xpath('./div[2]/strong//text()').extract()[0]
                    helpfulness = commentInfo.xpath('./span[last()]//text()').extract()[0]

                    item = dict(
                        # reviewerId=reviewerId,
                        reviewerName=reviewerName,
                        overall=overall,
                        reviewTime=reviewTime,
                        reviewText=reviewText,
                        summary=summary,
                        helpfulness=helpfulness
                    )
                    commentList.append(item)
                pi['comment'] = commentList



                item =dict(
                    pid=pi['pid'],
                    title=pi['title'],
                    otherFormat=pi['otherFormat'],  # DVD, VHS Tape, etc.

                    primeMeta=pi['primeMeta'],  # only in prime video
                    primeDetail = pi['primeDetail'],
                    comment = pi['comment']
                )

                yield item


            else:

                print("------------------parse intro")


                pi['format'] = response.xpath('//div[@id="bylineInfo"]/span[last()]/text()').extract()[0]

                print("------------------parse format")

                pi['otherFormat'] = []
                otherFormatHrefs = response.xpath(
                    "//li[contains(@class, 'swatchElement')]//a[@href!='javascript:void(0)']/@href").extract()
                for otherFormatHref in otherFormatHrefs:
                    asin = re.search('/dp/(\w+)/', otherFormatHref).group(1)
                    pi['otherFormat'].append(asin)

                print("------------------parse otherFormat")


                pi['style'] = response.xpath('//*[@id="dp"]/div[3]//li[last()]/span//text()').extract()[0].strip()

                print("------------------parse style")

                mainActors = response.xpath('//*[@id="bylineInfo"]//span[@class="author notFaded"][position()<last()]')
                mainActorsList = []
                for actor in mainActors:
                    mainActor = actor.xpath('./a//text()').extract()[0]
                    mainActorsList.append(mainActor)
                pi['mainActors'] = mainActorsList

                print("------------------parse mainActors")

                pi['additionalOptions'] = []
                additionalOptionHrefs = response.xpath(
                    "//div[contains(@class, 'top-level')]//span/@data-tmm-see-more-editions-click").extract()
                additionalOptionHrefs = list(filter(lambda x: '"metabindingUrl":"#"' not in x, additionalOptionHrefs))
                for additionalOptionHref in additionalOptionHrefs:
                    asin = re.search('/dp/(\w+)/', additionalOptionHref).group(1)
                    pi['additionalOptions'].append(asin)

                print("------------------parse additionalOptions")


                pi['productDetail'] = {}
                detailNames = response.xpath(
                    '//div[@id="detailBullets_feature_div"]/ul[contains(@class, "detail-bullet-list")]//span[@class="a-text-bold"]')
                for detailName in detailNames:
                    key = detailName.xpath('.//text()').extract()[0][:-7]
                    value = detailName.xpath('../span[last()]/text()').extract()[0]
                    pi['productDetail'][key] = value

                print("------------------parse productDetail")


                commentList = []
                commentInfos = response.xpath('//*[@id="cm-cr-dp-review-list"]//div[@data-hook="review"][position()<=2]')
                for commentInfo in commentInfos:
                    reviewerId = commentInfo.xpath('./@id').extract()[0]
                    print("------------------parse reviewerId")
                    reviewerName = commentInfo.xpath('.//span[contains(@class,"a-profile-name")]//text()').extract()[0]
                    print("------------------parse reviewerName")
                    overall = commentInfo.xpath('.//i[@data-hook="review-star-rating"]/span//text()').extract()[0][0:3]
                    print("------------------parse overall")
                    reviewTime = commentInfo.xpath('.//span[@data-hook="review-date"]//text()').extract()[0]
                    reviewTime = reviewTime.split('on')[1][1:]
                    print("------------------parse reviewTime")
                    # reviewTime = reviewTime.split(' ')
                    # reviewTime[0] = list(calendar.month_name).index(reviewTime[0])
                    # reviewTime[1] = reviewTime[0]
                    # Time = reviewTime[0]+' '+reviewTime[1]+' '+reviewTime[2]
                    reviewTextSpan = commentInfo.xpath('.//div[@data-hook="review-collapsed"]/span')
                    reviewText = reviewTextSpan.xpath('string(.)').extract()[0]
                    print("------------------parse reviewText")
                    summary = commentInfo.xpath('.//a[@data-hook="review-title"]/span//text()').extract()[0]
                    print("------------------parse summary")
                    helpfulness = ""
                    helpfulnesses = commentInfo.xpath('.//span[@data-hook="helpful-vote-statement"]')
                    for h in helpfulnesses:
                        helpfulness = h.xpath('.//text()').extract()[0]
                    print("------------------parse helpfulness")

                    # pi['otherFormat'] = []
                    # otherFormatHrefs = response.xpath(
                    #     "//li[contains(@class, 'swatchElement')]//a[@href!='javascript:void(0)']/@href").extract()
                    # for otherFormatHref in otherFormatHrefs:
                    #     asin = re.search('/dp/(\w+)/', otherFormatHref).group(1)
                    #     pi['otherFormat'].append(asin)

                    item = dict(
                        reviewerId=reviewerId,
                        reviewerName=reviewerName,
                        overall=overall,
                        reviewTime=reviewTime,
                        reviewText=reviewText,
                        summary=summary,
                        helpfulness=helpfulness,
                    )
                    commentList.append(item)
                pi['comment'] = commentList

                print("------------------parse comment")

                item = dict(
                    pid=pi['pid'],
                    title=pi['title'],
                    format=pi['format'],
                    otherFormat=pi['otherFormat'],  # DVD, VHS Tape, etc.
                    style = pi['style'],
                    mainActors=pi['mainActors'],
                    additionalOptions=pi['additionalOptions'],  # DVD1, DVD2, etc.
                    productDetail=pi['productDetail'],
                    comment =  pi['comment'],

                    # primeMeta=pi['primeMeta'],  # only in prime video

                )

                print("------------------parse done")

                yield item

        except:
            pass





