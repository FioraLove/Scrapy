"""
start_requests()方法，可以返回一个请求给爬虫的起始网站，这个返回的请求相当于start_urls，start_requests()返回的请求会替代start_urls里的请求

Request()get请求，可以设置，url、cookie、回调函数

FormRequest.from_response()表单post提交，第一个必须参数，上一次响应cookie的response对象，其他参数，cookie、url、表单内容等

yield Request()可以将一个新的请求返回给爬虫执行

在发送请求时cookie的操作， meta={‘cookiejar’:1}表示开启cookie记录，
首次请求时写在Request()里 meta={‘cookiejar’:response.meta[‘cookiejar’]}表示使用上一次response的cookie，
写在FormRequest.from_response()里post授权 meta={‘cookiejar’:True}表示使用授权后的cookie访问需要登录查看的页面
"""
import scrapy
from scrapy.http import HtmlResponse
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

class MyrenrenSpider(CrawlSpider):
    name = 'myrenren2'
    allowed_domains = ['renren.com']
    #个人主页
    start_urls = ['http://www.renren.com/353111356/profile']
    #爬取多个人的主页
    rules = [Rule(LinkExtractor(allow=("(\d+)/profile")),callback="get_parse",follow=True)]

    # 爬虫开启时调用的第一个方法，只调用一次
    def start_requests(self):
        indexURL = "http://www.renren.com"
        # 表单数据提交
        # formdata 表单数据
        # callback 登录后回调
        yield scrapy.FormRequest(url=indexURL,
              # 开启cookie， 用来保存cookie,在setting把COOKIES_ENABLED设为True
                                 meta={"cookiejar":1},
                                 callback=self.login
                                 )
    def login(self,response):
        print('访问主页返回的的url',response.url)
        # 从响应里面获取认证牌
        loginUrl = "http://www.renren.com/PLogin.do"
        yield scrapy.FormRequest.from_response(response,#响应
                                               url=loginUrl,# 登录url
                                               #表单数据
                                               formdata={"email": "你的值",
                                                         "password": "你的密码",},
                                               meta={"cookiejar": response.meta['cookiejar']},  # 传递cookie
                                               callback=self.after_login
                                               )
    #登录后
    def after_login(self,response):
        print('登录后返回的url',response.url)
        for url in self.start_urls:
            yield scrapy.Request(url,meta={"cookiejar": response.meta['cookiejar']})

    # 重写CrawlSpider中_requests_to_follow()方法
    def _requests_to_follow(self, response):
        """重写加入cookiejar的更新"""
        print('跟踪的url',response.url)
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)

                # 更新cookie
                r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])

                yield rule.process_request(r)
    #处理爬取得到的网页函数
    def get_parse(self, response):
        print('追踪后返回的url',response.url)
        print(response.body.decode('utf-8'))
