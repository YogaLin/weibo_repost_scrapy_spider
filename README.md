# weibo_repost_scrapy_spider

基于微博转发关系的网络爬虫

## env

python 2.7 | scrapy 1.3

## file descriptions：

weibo/items.py:
config fields you want to crawl

weibo/middlewares.py:
some middlewares like random-user-agent you can use

weibo/settings.py:
settings of this scrapy spider

weibo/spiders/weibo_spider.py:
the crawler itself

weibo/2017_06_06.csv:
a demo crawled result of weibo

## demo result:

a demo result of weibo: https://weibo.cn/comment/EwqnPi6i6

![pic](https://raw.githubusercontent.com/YogaLin/weibo_repost_scrapy_spider/master/demo-result.png)

the result will be saved in csv format with UTF-8 code, you would like to convert it to ANSI code if you open the file in Microsoft Excel and having wrong-encode problem.

## run step:

1. Run: pip install scrapy(only for whom have not installed scrapy yet.)

2. Clone code: git clone git@github.com:YogaLin/weibo_repost_scrapy_spider.git

3. login [weibo.cn](https://weibo.cn) and capture the cookies of login info(software like [fiddler](http://www.telerik.com/fiddler) should be capable for this job)

4. config your cookies info and start_weibo_id in weibo/spider/weibo_spiders.py file(I would suggest you conifg more than one cookies, but one should be fine if you slow your crawl speed.)

5. change your working-dir to /weibo folder

6. run code: scrapy crawl weibo_spider -o YOUR_OUTPUT_FILE.csv(with .csv suffix)

## F&Q

1. Run the code and csv file only have one single data(data from your start_url)

  In this case, it's mostly you a bad cookies that weibo.cn server thinks you are not login yet. Modify your cookies_list with another (or other) cookies should work.

## Other issues

1. make sure it's not problem casued by scrapy, you are welcome to add new issue.
