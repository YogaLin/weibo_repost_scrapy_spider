# -*- coding: utf-8 -*-
import scrapy
import sys
import random
import re
# from lxml import etree
from weibo.items import WeiboItem

reload(sys)
sys.setdefaultencoding('utf-8')

class WeiboSpiderSpider(scrapy.Spider):
    name = "weibo_spider"
    # allowed_domains = ["weibo.cn"]
    start_weibo_id = ['EwqnPi6i6']

    # record all weibo_id had been crawled
    weibo_id_set = set()
    weibo_template = 'https://weibo.cn/repost/%s?page=%d'

    cookies_list = ['_T_WM=f50ba93217f9bbcbdb1256744eb43d50; SUB=_2A250JUQzDeRhGeBM6FsQ8yrOwjqIHXVX5mx7rDV6PUJbkdBeLXWlkW184BIEe2WLlJqDL0rws2g5H1xoFA..; SUHB=0XDlDT3Y876fUm; SCF=AuzgURHxsZcjme35-xeO2R8iCvPvvaOaUPlp6F4D0jD_9D_x4PviVr7StWPETp5H7x5WLOAMFyFtojX2wiMfw2U.', 'M_WEIBOCN_PARAMS=oid%3D4047516368597679%26featurecode%3D20000180%26luicode%3D10000011%26lfid%3D100803; _T_WM=f50ba93217f9bbcbdb1256744eb43d50; SUB=_2A250JUQzDeRhGeBM6FsQ8yrOwjqIHXVX5mx7rDV6PUJbkdBeLXWlkW184BIEe2WLlJqDL0rws2g5H1xoFA..; SUHB=0XDlDT3Y876fUm; SCF=AuzgURHxsZcjme35-xeO2R8iCvPvvaOaUPlp6F4D0jD_9D_x4PviVr7StWPETp5H7x5WLOAMFyFtojX2wiMfw2U.; SSOLoginState=1495348323', '_T_WM=a23f9dd85131ba1658b2b6cb1fff54a6; SUB=_2A250Jh1RDeRhGeBM6FsQ8yjLzTiIHXVX6KMZrDV6PUJbkdBeLUnSkW2bvfN-UHyonVfwwEGUGUlA0cv3wQ..; SUHB=0P1MfGwfqWaSvg; SCF=Asgi69RlGcYMnCCHT_wx8B0VIUpPPThRAO2zZ8iFWGUPEnPaTCdaqPK1cefTl__zOjPBKJadsdDM5hNqWwji1cM.; SSOLoginState=1495428353']

    def get_random_cookies(self):
        cookies = random.choice(self.cookies_list)
        #cookies = self.cookies_list[2]
        rt = {}
        for item in cookies.split(';'):
            key, value = item.split('=')[0].strip(), item.split('=')[1].strip()
            rt[key] = value
        return rt
       

    # 以一个或者多个微博id为根节点微博，开始根据转发关系递归爬取，并传递自己的id给转发结点作为父亲id
    def start_requests(self):
        #cookies = self.cookies_list[2]
        for weibo_id in self.start_weibo_id:
            self.weibo_id_set.add(weibo_id)
            item = WeiboItem()
            item['weibo_id'] = weibo_id
            item['father_weibo_id'] = 'ROOT'
            yield scrapy.Request(url = self.weibo_template % (weibo_id, 1), cookies = self.get_random_cookies(), meta = {'item':item}, callback = self.parse_content)


    # 通过翻页获取所有的转发微博的id，再进行内容爬取
    # 通过 parse_content 获取了信息后再将id放进来爬取repost_id
    # 将 weibo_id 作为 father_weibo_id 传给它的转发微博结点
    # TODO:设置爬取层数
    def get_repost_weibo_id(self, weibo_id, page_size):
        # TODO: 更多热门转发
        print "weibo_id: %s, page_size: %d" % (weibo_id, page_size)
        if weibo_id and page_size:
            print "test*****************************"
            for page in range(1, page_size+1):
                yield scrapy.Request(url = self.weibo_template % (weibo_id, page), cookies = self.get_random_cookies(), meta = {'father_weibo_id': weibo_id}, callback = self.request_content_by_weibo_id)

    # 根据页面上的repost_weibo_id去请求微博内容页面
    def request_content_by_weibo_id(self, response):
        print "test2###################", response.url
        weibo_ids = response.selector.re('/attitude/(\w+)/')
        print weibo_ids
        for weibo_id in weibo_ids:
            # weibo_id_set集合保存已经爬取过的weibo，防止重复内容的爬取
            if weibo_id not in self.weibo_id_set:
                self.weibo_id_set.add(weibo_id)
                item = WeiboItem()
                item['weibo_id'] = weibo_id
                item['father_weibo_user_id'] = response.meta['father_weibo_user_id']
                item['father_weibo_user_name'] = response.meta['father_weibo_user_name']
                item['father_weibo_id'] = response.meta['father_weibo_id']
                yield scrapy.Request(url = self.weibo_template % (weibo_id, 1), cookies = self.get_random_cookies(), meta = {'item':item}, callback = self.parse_content)

    # 解析在 request_content_by_weibo_id 和 start_requests 中请求到的微博内容页面
    def parse_content(self, response):
        item = response.meta['item']
        # 只在根结点保存微博内容
        if item['father_weibo_id'] == 'ROOT':
            content = response.xpath('//*[@id="M_"]/div[1]/span[@class="ctt"]')
            item['content'] = content[0].xpath('string(.)').extract()[0] if content else None
        user_id = response.xpath('//*[@id="M_"]/div[1]/a[1]/@href').extract()
        item['user_id'] = user_id[0][1:] if user_id else None
        if item['user_id'].startswith('u/'):
            item['user_id'] = item['user_id'][2:]
        user_name = response.xpath('//*[@id="M_"]/div[1]/a[1]/text()').extract()
        item['user_name'] = user_name[0] if user_name else None
        pub_time = response.xpath('//*[@id="M_"]/div[1]/span[@class="ct"]/text()|//*[@id="M_"]/div[2]/span[@class="ct"]/text()').extract()
        item['pub_time'] = pub_time[0].strip() if pub_time else None
        repost_num = response.xpath('//*[@id="rt"]/text()').re('\d+')
        item['repost_num'] = repost_num[0] if repost_num else 0
        comment_num = response.xpath('//*[@id="rt"]/following-sibling::span[1]/a/text()').re('\d+')
        item['comment_num'] = comment_num[0] if comment_num else 0
        thumb_num = response.xpath('//*[@id="rt"]/following-sibling::span[2]/a/text()').re('\d+')
        item['thumb_num'] = thumb_num[0] if thumb_num else 0
        repost_reason = response.xpath('//*[@id="M_"]/div[2]')
        item['repost_reason'] = repost_reason[0].xpath('string(.)').extract()[0] if repost_reason else None
        #repost_reason = re.findall(':([\s\S]+?)\s+\d+月', repost_reason) if repost_reason else None
        #item['repost_reason'] = repost_reason[0] if repost_reason else None
        yield item
        page_size = response.xpath('//*[@id="pagelist"]/form[1]/div[1]/input[1]/@value').extract()
        page_size = int(page_size[0]) if page_size else 0
        #print response.url, item, page_size, len(self.weibo_id_set)
        
        if item['weibo_id'] and page_size:
            #print "weibo_id: %s, page_size: %d" % (item['weibo_id'], page_size)
            for page in range(1, page_size+1):
                yield scrapy.Request(url = self.weibo_template % (item['weibo_id'], page), cookies = self.get_random_cookies(), meta = {'father_weibo_id': item['weibo_id'], 'father_weibo_user_id': item['user_id'], 'father_weibo_user_name': item['user_name']}, callback = self.request_content_by_weibo_id)
        







