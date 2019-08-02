### 正文

  针对问题：如果想对某一个网站的全站数据进行爬取，该如何处理？
  
      解决方案：

    1.手动请求的发送：基于Scrapy框架中的Spider的递归爬取进行实现（Request模块递归回调parse方法）
    2.CrawlSpider：基于CrawlSpider的自动爬取进行实现（更加简洁和高效）
    
### 一、CrawlSpider介绍

　　-CrawlSpider其实是Spider的一个子类。

    1、CrawlSpider功能
      CrawlSpider功能比Spider更加强大：除了继承到Spider的特性和功能外，还派生除了其自己独有的更加强大的特性和功能。
      其中最显著的功能就是“LinkExtractors链接提取器”和“规则解析器”。

    2、Spider和CrawlSpider应用场景
      Spider是所有爬虫的基类，其设计原则只是为了爬取start_url列表中网页，而从爬取到的网页中提取出的url进行继续的爬取工作使用CrawlSpider更合适。
      

    
### 七、Scrapy框架之CrawlSpider

   二、CrawlSpider使用
   
   -1、创建工程与CrawlSpider爬虫文件
   
    # 创建scrapy工程：
    $ scrapy startproject crawlSpiderPro
    $ cd crawlSpiderPro/
    
    # 创建一个基于CrawlSpider的爬虫文件
    $ scrapy genspider -t crawl chouti dig.chouti.com
    Created spider 'chouti' using template 'crawl' in module:
      crawlSpiderPro.spiders.chouti
    　　注意：创建爬虫的指令对比以前的指令多了 "-t crawl"，表示创建的爬虫文件是基于CrawlSpider这个类的，而不再是Spider这个基类。

  -2、观察分析生成的爬虫文件:chouti.py
  
    # -*- coding: utf-8 -*-
    import scrapy
    from scrapy.linkextractors import LinkExtractor   # 链接提取器对应的类
    from scrapy.spiders import CrawlSpider, Rule   # Rule是规则解析器对应的类
    
    class ChoutiSpider(CrawlSpider):   # 这里继承的父类时CrawlSpider
        name = 'chouti'
        # allowed_domains = ['dig.chouti.com']
        start_urls = ['https://dig.chouti.com/']
    
        rules = (
            # rules中保存的是元组，元组中保存的是Rule规则解析器对象
            # 规划解析器对象第一个参数是：链接提取器对象
            Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        )
    
        def parse_item(self, response):   # 解析方法
            i = {}
            #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
            #i['name'] = response.xpath('//div[@id="name"]').extract()
            #i['description'] = response.xpath('//div[@id="description"]').extract()
            return i
            
  -3、LinkExtractor——链接提取器
  
    链接提取器作用：可以用来提取页面中符合正则表达式要求的相关链接(url)。

    LinkExtractor(
        allow=r'Items/',     # 满足括号中“正则表达式”的值会被提取，如果为空，则全部匹配。
        deny=xxx,            # 满足正则表达式的则不会被提取。
        restrict_xpaths=xxx, # 满足xpath表达式的值会被提取
        restrict_css=xxx,    # 满足css表达式的值会被提取
        deny_domains=xxx,    # 不会被提取的链接的domains。　
    )
    allow参数：赋值一个正则表达式。
    　　allow赋值正则表达式后，链接提取器就可以根据正则表达式在页面中提取指定的链接。提取到的链接会全部交给规则解析器处理。
   -4、Rule——规则解析器
   
    　　规则解析器接受了链接提取器发送的链接后，就会对这些链接发起请求，获取链接对应的页面内容。
    　　获取页面内容后，根据指定的规则将页面内容中的指定数据值进行解析。

    （1）解析器格式
    Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True)
    （2）参数介绍
    　　参数1: 指定链接提取器
    　　参数2:callback 指定规则解析器解析数据的规则（回调函数）
    　　参数3:follow 是否将链接提取器继续作用到链接提取器提取出的链接网页中。
    
    　　当callback为None,参数3的默认值为true。
    　　follow为False时，链接提取器只是提取当前页面显示的所有页码的url
    　　follow为True时会不断往后根据页码提取页面，直到提取所有的页面链接，并自动完成去重操作。

  -5、CrawlSpider整体爬取流程
  
        爬虫文件首先根据起始url，获取该url的网页内容
        链接提取器会根据指定提取规则将步骤a中网页内容中的链接进行提取
        规则解析器会根据指定解析规则将链接提取器中提取到的链接中的网页内容根据指定的规则进行解析
        将解析数据封装到item中，然后提交给管道进行持久化存储
        回到顶部
### 三、抽屉网项目实战

   （1）chouti.py
    
    import scrapy
    from scrapy.linkextractors import LinkExtractor   # 链接提取器对应的类
    from scrapy.spiders import CrawlSpider, Rule   # Rule是规则解析器对应的类
    from ..items import CrawlspiderproItem
    
    class ChoutiSpider(CrawlSpider):
        name = 'chouti'
        # allowed_domains = ['dig.chouti.com']
        start_urls = ['https://dig.chouti.com/']
        # 定义链接提取器，且指定其提取规则(即正则化url，仅对网页URL起作用)
        Link = LinkExtractor(allow=r'/all/hot/recent/\d+')    # 获取的页码的a标签中href值
    
        rules = (
            # 定义规则解析器，且指定解析规则通过callback回调函数
            Rule(Link, callback='parse_item', follow=True),
        )
    
        def parse_item(self, response):   # 解析方法
            """自定义规则解析器的解析规则函数"""
            div_list = response.xpath('//div[@id="content-list"]/div')
    
            for div in div_list:
                # 定义item
                item = CrawlspiderproItem()
                # 根据xpath表达式提取抽屉新闻的内容
                item['content'] = div.xpath('.//div[@class="part1"]/a/text()').extract_first().strip('\n')
                # 根据xpath表达式提取抽屉新闻的作者
                item['author'] = div.xpath('.//div[@class="part2"]/a[4]/b/text()').extract_first().strip('\n')
                yield item  # 将item提交至管道
                
   （2）items.py
    
    import scrapy
    
    class CrawlspiderproItem(scrapy.Item):
        # define the fields for your item here like:
        # name = scrapy.Field()
        author = scrapy.Field()
        content = scrapy.Field()
   （3）pipelines.py
    
    class CrawlspiderproPipeline(object):
        def __init__(self):
            self.fp = None
    
        def open_spider(self, spider):
            print('开始爬虫')
            self.fp = open('./data.txt', 'w')
    
        def process_item(self, item, spider):
            # 将爬虫文件提交的item写入文件进行持久化存储
            self.fp.write(item['author'] + ':' + item['content'] + '\n')
            return item
    
        def close_spider(self, spider):
            print('结束爬虫')
            self.fp.close()
            
   （4）settings.py

    # Crawl responsibly by identifying yourself (and your website) on the user-agent
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' # 伪装请求载体身份
    
    # Obey robots.txt rules
    ROBOTSTXT_OBEY = False   # 不遵从门户网站robots协议，避免某些信息爬取不到
    
    # Configure item pipelines
    # See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
    ITEM_PIPELINES = {
        'crawlSpiderPro.pipelines.CrawlspiderproPipeline': 300,
    }
    
 （5）执行爬虫

    $ scrapy crawl chouti --nolog # --nolog表示无日志输出
    　　可以看到使用CrawlSpider来爬取全站数据，代码简化程度远高于手动请求发送的模式，并且性能也优化非常多。   

    
