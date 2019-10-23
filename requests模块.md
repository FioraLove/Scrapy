### [requests模块](https://www.cnblogs.com/xiugeng/p/9877265.html) [requests模块二](https://blog.csdn.net/qq_36759224/article/details/99747704)<br>
<img src="https://github.com/FioraLove/Tips/blob/Dev-1/%E5%85%B6%E5%AE%83/images/57450b9a295f5.jpg" width=50%>

    常用的就是requests.get()和requests.post()

    requests.get(url, params=None, **kwargs)
    requests.post(url, data=None, json=None, **kwargs)
    requests.put(url, data=None, **kwargs)
    requests.head(url, **kwargs)
    requests.delete(url, **kwargs)
    requests.patch(url, data=None, **kwargs)
    requests.options(url, **kwargs)

    # 以上方法均是在此方法的基础上构建
    requests.request(method, url, **kwargs)
   
#### 1.处理url携带参数的get请求
    import requests

    url = 'https://www.sogou.com/web'

    # 将参数封装到字典中
    params = {
        'query': "周杰伦",
        'ie': 'utf-8'
    }
    response = requests.get(url=url, params=params)
    response.status_code   # 响应状态码：200
    
#### 2.基于requests模块发起的POST请求
    import requests

    # 1.指定post请求的url
    url = "https://accounts.douban.com/login"

    # 封装post请求的参数
    data = {
        "source": "movie",
        "redir": "https://www.douban.com/",
        "form_email": "18907281232",
        "form_password": "uashudh282",
        "login": "登录",
    }

    # 自定义请求头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }

    # 2.发起post请求
    response = requests.post(url=url, data=data, headers=headers)  # 响应对象

    # 3.获取响应对象中的页面数据
    page_text = response.text
#### requests请求的参数：get请求的params、post请求的data、header、上传文件、Cookies、会话Session、SSL 证书验证、代理proxies、超时设置timeout
