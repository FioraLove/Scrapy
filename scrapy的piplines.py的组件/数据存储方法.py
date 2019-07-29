# 将数据分别存储到磁盘、redis、mysql中（管道高级操作）
# 1.修改pei配置管道文件piplines.py文件
# MySQL版本
import pymysql


class QiushibaikePipeline(object):
    # 连接对象声明为全局属性
    conn = None
    # 创建游标对象
    cursor = None

    def open_spider(self, spider):
        print('开始爬虫。。')
        # 连接MySQL数据库
        self.conn = pymysql.connect(host='127.0.0.1', port=3306,
                                    user='root', password='123456', db='qiubai')

    def process_item(self, item, spider):
        """
        编写向数据库中存储数据的相关代码
        :param item:
        :param spider:
        :return:
        """
        # 执行SQL语句
        sql = 'insert into qiubai values ("%s","%s")' % (item['author'], item['content'])
        # 创建游标对象
        self.cursor = self.conn.cursor()
        # 异常处理机制
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        print('爬取结束')
        self.cursor.close()
        self.conn.close()


# redis库版本
"""
启动redis数据库：
1.进入redis文件目录
2.打开redis服务：redis-server
3.键入redis-cli
4.正式开启服务了：set key values
"""
import json, redis


class QiushibaikePipeline(object):
    # 声明全局连接对象
    conn = None

    def open_spider(self, spider):
        print('开始爬虫')
        self.conn = redis.Redis(host='127.0.0.1', port=6379)

    def process_item(self, item, spider):
        # dic中封装item对象中获取的页面数据
        dic = {
            'author': item['author'],
            'content': item['content'],
        }
        # 转为字符串
        dic_str = json.dumps(dic)

        # redis数据库写入
        # lpush：从左往右添加元素。在key对应list的头部添加字符串元素
        self.conn.lpush('data', dic_str)
        return item

# 磁盘文件保存
class QiubaiByFilesPipeline(object):
    """实现将数据值存储到本地磁盘中"""
    fp = None
    def open_spider(self, spider):
        print("开始爬虫")
        # 在该方法中打开文件
        self.fp = open('./qiubai_pipe.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 取出Item对象中存储的数据值
        author = item['author']
        content = item['content']
        # 持久化存储
        self.fp.write(author + ":" + content+ '\n\n\n')  # 写入数据
        return item

    def close_spider(self, spider):
        print("爬虫结束")
        # 关闭文件
        self.fp.close()
