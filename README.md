# python-
scrapy+requests+re(pyquery)=数据就在你手中

# scrapy
# 爬虫框架
- 框架
- 爬虫框架
    - scrapy 
    - pyspider
    - crawley
- scrapy框架介绍
    - https://doc.scrapy.org/en/latest/
    - http://scrapy-chs.readthedocs.io/zh_CN/latest/index.html
    
- 安装
    - 利用pip  
 
- scrapy概述
    - 包含各个部件
        - ScrapyEngine： 神经中枢，大脑，核心、
        - Scheduler调度器：引擎发来的request请求，调度器需要处理，然后交换引擎
        - Downloader下载器：把引擎发来的requests发出请求，得到response
        - Spider爬虫： 负责把下载器得到的网页/结果进行分解，分解成数据+链接
        - ItemPipeline管道： 详细处理Item
        - DownloaderMiddleware下载中间件： 自定义下载的功能扩展组件
        - SpiderMiddleware爬虫中间件：对spider进行功能扩展
        
- 爬虫项目大概流程
    - 新建项目：scrapy startproject xxx
    - 明确需要目标/产出:  编写item.py
    - 制作爬虫 ： 地址 spider/xxspider.py
    -  存储内容： pipelines.py,   
    
- ItemPipeline
    - 对应的是pipelines文件
    - 爬虫提取出数据存入item后，item中保存的数据需要进一步处理，比如清洗，去重，存储等
    - process_item:
        - spider提取出来的item作为参数传入，同时传入的还有spider
        - 此方法必须实现
        - 必须返回一个Item对象，被丢弃的item不会被之后的pipeline处理
    - __init__:构造函数
        - 进行一些必要的参数初始化     
    - open_spider(spider):
        - spider对象被开启的时候调用
    - close_spider(spider):
        - 当spider对象被关闭的时候调用 
- Spider
    - 对应的是文件夹spiders下的文件
    - __init__: 初始化爬虫名称，start_urls列表
    - start_requests:生成Requests对象交给Scrapy下载并返回response
    - parse： 根据返回的response解析出相应的item，item自动进入pipeline； 如果需要，解析出url，url自动交给
    requests模块，一直循环下去
    - start_request: 此方法仅能被调用一次，读取start_urls内容并启动循环过程
    - name:设置爬虫名称
    - start_urls:  设置开始第一批爬取的url
    - allow_domains:spider允许爬去的域名列表
    - start_request(self)： 只被调用一次
    - parse
    - log:日志记录
- 中间件(DownloaderMiddlewares)
    - 中间件是处于引擎和下载器中间的一层组件
    - 可以有很多个，被按顺序加载执行
    - 作用是对发出的请求和返回的结果进行预处理
    - 在middlewares文件中
    - 需要在settings中设置以便生效
    - 一般一个中间件完成一项功能
    - 必须实现以下一个或者多个方法
        - process_request(self, request, spider)
            - 在request通过的时候被调用
            - 必须返回None或Response或Request或raise IgnoreRequest
            - None: scrapy将继续处理该request
            - Request： scrapy会停止调用process_request并冲洗调度返回的reqeust
            - Response： scrapy不会调用其他的process_request或者process_exception，直接讲该response作为结果返回
            同时会调用process_response函数
        - process_response(self, request, response,  spider)
            - 跟process_request大同小异
            - 每次返回结果的时候会自动调用
            - 可以有多个，按顺序调用
        
        
        中间件- 案例代码：
        
          1.中间件处理      
                import random
                import base64
                
                # 从settings设置文件中导入值
                from settings import USER_AGENTS
                from settings import PROXIES
                
                #  随机的 User-Agent
                # 在middlewares.py中单独给UA池封装一个下载中间件的类
                from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
                import random
                
                class RandomUserAgent(object):
                    def process_request(self, request, spider):
                        useragent = random.choice(USER_AGENTS)
                        request.headers.setdefault("User-Agent", useragent)
                        
                class RandomProxy(object):
                    def process_request(self, request, spider):
                        proxy = random.choice(PROXIES)
                        if proxy['user_passwd'] is None:
                            #  没有代理账户验证的代理使用方式
                            request.meta['proxy'] = "http://" + proxy['ip_port']
                        else:
                            #  对账户密码进行 base64 编码转换
                            base64_userpasswd = base64.b64encode(proxy['user_passwd'])
                            #  对应到代理服务器的信令格式里
                            request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd
                            request.meta['proxy'] = "http://" + proxy['ip_port']
        
        - 2.设置settings的相关代码
        
        
                USER_AGENTS = [
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR
                            3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0;
                            SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET
                            CLR 1.1.4322)",
                            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR
                            2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko,
                            Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3)
                            Arora/0.6",
                            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-
                            Ninja/2.1.1",
                            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0
                            Kapiko/3.0",
                            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
                            ]           
   
                PROXIES = [
                        {'ip_port': '111.8.60.9:8123', 'user_passwd': 'user1:pass1'},
                        {'ip_port': '101.71.27.120:80', 'user_passwd': 'user2:pass2'},
                        {'ip_port': '122.96.59.104:80', 'user_passwd': 'user3:pass3'},
                        {'ip_port': '122.224.249.122:8088', 'user_passwd': 'user4:pass4'},
                        ]
                        
        - 3.settings.py中开启ua池、代理池
            DOWNLOADER_MIDDLEWARES = {
                'wangyiPro.middlewares.WangyiproDownloaderMiddleware': 543,
                'wangyiPro.middlewares.RandomUserAgent': 542,
                'wangyiPro.middlewares.Proxy': 541,
            }
                        
- 去重
    - 为了放置爬虫陷入死循环，需要去重
    - 即在spider中的parse函数中，返回Request的时候加上dont_filter=False参数
    
            myspeder(scrapy.Spider):
                def parse(.....):
                
                    ......
                    
                    yield  scrapy.Request(url=url, callback=self.parse, dont_filter=False)                
       
- 如何在scrapy使用selenium
    - 可以放入中间件中的process_request函数中
    - 在函数中调用selenium，完成爬取后返回Response
    
        
            calss MyMiddleWare(object):
                def process_request(.....):
                    
                    driver = webdriver.Chrome()
                    html = driver.page_source
                    driver.quit()
                    
                    return HtmlResponse(url=request.url, encoding='utf-8', body=html, request=request)


###  1.def start_requests()函数
    -该方法必须返回一个可迭代对象(iterable)。该对象包含了spider用于爬取的第一个Request

            
###  2. 选择器(selectors)
    -XPath使用：
        2.1 为了提取真实的原文数据，你需要调用 .extract() 方法如下:
         response.xpath('//title/text()').extract()
        2.2 如果想要提取到第一个匹配到的元素, 必须调用 .extract_first()
    """
        表达式                 描述                    用法              说明
        nodename        选取此节点的所有子节点     xpath(‘span’)      选取span元素的所有子节点
            /               从根节点选取          xpath(‘/div’)       从根节点上选取div节点    
            //      从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置   xpath(‘//div’)   从当前节点选取含有div节点的标签
            .               选取当前节点          xpath(‘./div’)      xpath(‘./div’)   选取当前节点下的div标签
            ..           选取当前节点的父节点        xpath(‘../’)         回到上一级节点
            @               选取属性        xpath(“//div[@id=’1001’]”)      获取div标签中，含有ID属性且值为1001的标签
    """
    
###   3. 直接运行main.py启动爬虫

        另外可以在该爬虫项目的根目录创建一个main.py，然后在pycharm设置下运行路径，那么就不用每次都运行上面那行代码，直接运行main.py就能启动爬虫了 
        输入代码：
        from scrapy import cmdline
        cmdline.execute('scrapy crawl amazon_products -o items.csv -t csv'.split())
        ＃－o 代表输出文件 －t 代表文件格式
        
        
##案例一：以一个具体案例讲解scrapy爬虫框架
   -1.新建项目
   
        scrapy startproject project_name
        cd project_name
        创建爬虫  scrapy genspider spider_name spider_url
        
   -2.编写爬虫文件
   
        # -*- coding: utf-8 -*-
        import scrapy, re
        # 从items.py导入字段类函数
        from ..items import QiushibaikeItem
        # 重点，重点，重点~~~~~~~~~~
        # 通过Settings对象的方法:从scrapy.conf中导入settings.py,并使用其中的设置
        from scrapy.conf import settings
        from scrapy import Request
        
        
        class QiushiSpider(scrapy.Spider):
            # 定义爬虫名字
            name = 'qiushi'
            
        # allowed_domains = ['qiushiom'] # 允许爬取的域名
        # 开始爬取的url
        # start_urls = ['https://www.qiushibaike.com/text/']
        # 可迭代的url，每一次的yield，向回调函数cellback=self.parse传递一个·URL处理
        def start_requests(self):
            # base_url = 'https://www.qiushibaike.com/text/page/{}'
            # 重点，重点，重点~~~~
            # 调用settings自定义的配置一定要self.settings.get('START_PAGE')这样写
            for page in range(self.settings.get('START_PAGE'), self.settings.get('END_PAGE')):
                url = 'https://www.qiushibaike.com/text/page/{}/'.format(page)
                yield Request(url=url, callback=self.parse)
        # 解析函数
        def parse(self, response):
            # 声明并调用items.py中定义的字段
            item = QiushibaikeItem()
            div_list = response.xpath('.//div[@class="col1"]/div')
            # 遍历每一个div_list
            for div in div_list:
                item['author'] = re.sub('\n', '', div.xpath('./div[@class="author clearfix"]/a[2]/h2/text()').extract_first())  # selector对象
    
                item['content'] = re.sub('\n', '', div.xpath('.//div[@class="content" ]/span/text()').extract_first())
                print(item['author'])
                # yield item 将item字段返回给piplines.py文件（用于文件保存）
                yield item
                
   -3 数据存储模板：items.py文件
   
    import scrapy

    class QiushibaikeItem(scrapy.Item):
        # define the fields for your item here like:
        # name = scrapy.Field()
        author = scrapy.Field()
        content = scrapy.Field()
        
   -4 数据持久化处理：piplines.py
   
    class QiushibaikePipeline(object):
        # 定义一个空变量
        f = None
        
        # 在spider开启时自动调用，可以做一些初始化操作：数据库连接，文件打开 
        def open_spider(self, spider):
            print('开始爬虫。。')
            self.f = open('./qiubai.txt', 'a', encoding='utf-8')
            
        # 数据存储，必须存在process_item(self,item,spider)
        def process_item(self, item, spider):
            # 写入文件
            self.f.write('\n' + item['author'] + ':' + item['content'] + '\n')
            return item
            
        # spider的收尾工作
        def close_spider(self, spider):
            self.f.close()
            print('爬取结束')
      
   -5 配置文件：settings.py
   
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' # 伪装请求载体身份

    # Obey robots.txt rules

    ROBOTSTXT_OBEY = False
    
    # Configure item pipelines
    # See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
    ITEM_PIPELINES = {      # 开启管道
        'qiubaiByPages.pipelines.QiubaibypagesPipeline': 300,
    }
    
    # 分页时的起始页
    START_PAGE =1
    # 结束页
    END_PAGE = 4
    
    
   -6.注意
   
    注意：
    　　1）第一页还是使用的起始url列表这个机制来进行请求发送，从第二页开始采用手动请求发送。
    　　2）执行请求手动发送必须结合 yield 和 Request 函数一块来使用。
    　　3）在调用scrapy.Request函数时，有一个参数叫 callback 。这是一个回调函数，会进行递归的调用。为了防止无限循环，需要设置递归终止条件
    
###案例二：如果您需要在启动时以POST登录某个网站，你可以这么写:
    
   -1.1 方法一：重写start_requests方法来发送post请求：
   
    import scrapy

    class PostdemoSpider(scrapy.Spider):
        name = 'postDemo'
        # allowed_domains = ['www.baidu.com']
        start_urls = ['https://fanyi.baidu.com/sug']     # 通过抓包找到post请求地址

        def start_requests(self):
            """重写的父类方法：该方法可以对star_urls列表中的元素进行get请求发送"""
            for url in self.start_urls:
                # Request方法默认发送get请求，配置method参数赋值为'post'
                yield scrapy.Request(url=url, callback=self.parse, method='post')
    
        def parse(self, response):
            pass
              
   -方法二：利用FormRequest方法来发送post请求(推荐)
     
   （1）编写爬虫文件postDemo.py
       
    import scrapy

    class PostdemoSpider(scrapy.Spider):

        name = 'postDemo'
        # allowed_domains = ['www.baidu.com']
        start_urls = ['https://fanyi.baidu.com/sug']    # 通过抓包找到post请求地址
    
        def start_requests(self):
            """重写的父类方法：该方法可以对star_urls列表中的元素进行get请求发送"""
            print("start_requests()被调用")
            data = {
                'kw': 'dog',  # post请求参数
            }
            for url in self.start_urls:
                # FormRequest()可以发送post请求
                # formdata表示请求参数对应的字典
                yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse)
    
        def parse(self, response):
            print(response.text)
            
   （2）编辑settings.py文件
   
    # Crawl responsibly by identifying yourself (and your website) on the user-agent
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' # 伪装请求载体身份
    
    # Obey robots.txt rules
    ROBOTSTXT_OBEY = False    # 不遵从门户网站robots协议，避免某些信息爬取不到       
    
   （3）创建项目、创建应用、执行爬虫
   
    $ scrapy startproject postPro
    $ cd postPro/
    $ scrapy genspider postDemo www.baidu.com
