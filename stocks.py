# -*- coding: utf-8 -*-
import scrapy


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    allowed_domains = ['baidu.com']
    start_urls = ['https://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            #you can try selecting elements using CSS with the response object
            #提取a标签中的attr属性值
            try:
                stock = re.findall(r"[s][hz]\d6"，href)[0]
                #匹配含有s、h/z、六位数字的代码
                url = 'https://gupiao.baidu.com/stock/' + stock + '.html'
                yield scrapy.Request(url, callback=self.parse_stock)
                #生成器，每次产生一个值，函数被冻结，被唤醒后再产生一个值
                #特别地，冻结之后yield后面的语句不再执行直到下一次唤醒生成器直接执行后续语句
            except:
                continue
    def parseStock(self, response):
        infoDict = {}
        stockInfo = response.css('.stock-bets') #这个点.表示 选择所有class包含stock-bets的节点
        name = stockInfo.css('.bets-name').extract()[0]
        keyList = stockInfo.css('dt').extract()
        valueList = stockInfo.css('dd').extract()
        for i in range(len(keyList):
            key = re.findall(r'>.*</dt>',keyList[i])[0][1:-5]
            try:
                val = re.findall(r'\d+\.?.*</dd>',valueList[i])[0][1:-5]
            except:
                val = '--'
            infoDict[key] = val


