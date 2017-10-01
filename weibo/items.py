# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    weibo_id = scrapy.Field() # weibo_id
    father_weibo_id = scrapy.Field() # 父 weibo_id
    user_id = scrapy.Field() # 用户id
    user_name = scrapy.Field() # 用户名
    repost_num = scrapy.Field() # 转发数目
    repost_reason = scrapy.Field() # 转发理由，只有转发微博有，root结点微博无
    comment_num = scrapy.Field() # 评论数
    thumb_num = scrapy.Field() # 点赞数
    content = scrapy.Field() # 微博内容，只有root结点微博有，转发微博无
    pub_time = scrapy.Field() # 发布时间
    client_type = scrapy.Field() # 发布客户端
    father_weibo_user_id = scrapy.Field() # 原微博的所属用户id
    father_weibo_user_name = scrapy.Field() # 原微博的所属用户名

# TODO: 评论表
class CommentItem(scrapy.Item):
    pass

# TODO: 转发表
class RepostItem(scrapy.Item):
    pass
