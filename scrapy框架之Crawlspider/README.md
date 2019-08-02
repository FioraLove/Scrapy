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

    
