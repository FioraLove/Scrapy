import scrapy


class MyrenrenSpider(scrapy.Spider):
    name = 'myrenren'
    allowed_domains = ['renren.com']

    # start_urls = ['http://renren.com/']
    # 重写start_requests()方法，爬虫首先调用这个方法，
    # 程序不再调用start_urls里的url
    def start_requests(self):
        loginUrl = "http://www.renren.com/PLogin.do"
        # 表单数据提交
        # formdata 表单数据
        # callback 登录后回调
        yield scrapy.FormRequest(url=loginUrl,
                                 formdata={"email": "你的账号",
                                           "password": "你的密码"},
                                 callback=self.parse
                                 )

    def parse(self, response):
        print('*******', response.url)
        print(response.body.decode('utf-8'))
