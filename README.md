# Panicbuying

Panicbuying是商城物品抢购脚本,目前支持小米商城.

快速使用
-------

1. 下载panicbuying,不会安装python的查看里面的python安装教程.

2. 安装依赖包

    ```
    D:\Downloads\panicbuying-master> pip install -r requirements.txt
    ```

2. 使用panicbuying,可直接修改start/demo.py里的参数直接运行.


    ```
    >>> from panicbuying.panicbuying.panic import Panic

    >>> xm = Panic(store='小米', driver='chromedriver', account='你的账户', password='你的密码', goods_name='你需要抢购的商品', goods_nth=1, addr_nth=1)

    >>> xm.start() # 启动浏览器

    >>> xm.close() # 关闭浏览器,抢购商品尽量别使用
    ```

3. 传入的参数说明:

    ```
    >>> store = '小米' # 抢购的商城

    >>> driver = 'chromedriver' # 启动浏览器的应用程序

    >>> account = '用户名' # 抢购小米商城则输入你的小米账号

    >>> password = '密码' # 对应账号的密码

    >>> goods_name = '小米手环' # 需要抢购的商品名称

    >>> googs_nth = 1 # 商品在搜索页面的第几个选项上,从1开始
    
    >>> addr_nth = 1 # 如果只有一个收货地址则填1,如果有多个请根据需要选择第几个收货地址
    ```