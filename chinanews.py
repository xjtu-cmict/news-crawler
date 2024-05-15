import requests
import json
import re
import time
import os
import sys
import yaml
from loguru import logger
from bs4 import BeautifulSoup
from urllib import parse

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

from constant.env_constant import EnvConstant
from constant.crawler_constant import CrawlerConstant
from util.create_xml import create_news_xml


class Chinanews():
    @logger.catch()
    def __init__(self, page_url_base, get_headers):
        self.page_number = 0
        self.page_url_base = page_url_base
        self.dir_name = input("查询主题：")
        self.headers = get_headers

    @logger.catch()
    def get_news_urls(self, page_url):
        response = requests.get(url=page_url, headers=self.headers)
        response.encoding = 'utf-8'
        print(response)
        soup = BeautifulSoup(response.text, CrawlerConstant.HTML_PARSER)
        li_tags = soup.find_all(class_=CrawlerConstant.NEWS_TITLE)
        news_urls = []
        for li_tag in li_tags:
            a_tag = li_tag.find(CrawlerConstant.A)
            news_url = a_tag.get(CrawlerConstant.HREF)
            news_urls.append(news_url)
        return news_urls
    
    @logger.catch()
    def save_news(self, news_url, save_path="./data"):
        response = requests.get(url=news_url, headers=self.headers)
        charset = re.findall('content="text/html; charset=(.*?)"', response.text, re.S)
        if charset == []:
            response.encoding = 'utf-8'
        else:
            response.encoding = 'gb2312'
        soup = BeautifulSoup(response.text, CrawlerConstant.HTML_PARSER)
        content = soup.find(class_=CrawlerConstant.LEFT_ZW).text
        old_title = soup.find(class_=CrawlerConstant.CONTENT_LEFT_TITLE)
        if old_title == None:
            old_title = soup.find(CrawlerConstant.TITLE)
        title = re.sub(r'[\/:*?"<>|\n ]', ' ', old_title.text)
        date = soup.find(id=CrawlerConstant.PUBTIME_BAIDU).text
        news_path = os.path.join(save_path, self.dir_name)
        create_news_xml(date, title, content, self.dir_name, news_path)

    @logger.catch()
    def run(self):
        dir_name_parse = parse.quote(self.dir_name)  # 编码
        for i in range(self.page_number):
            page_url = self.page_url_base.format(dir_name_parse, str(10*i))
            news_urls = self.get_news_urls(page_url)
            for news_url in news_urls:
                self.save_news(news_url)
                time.sleep(0.1)

if __name__ == '__main__':
    # 载入配置文件
    with open(EnvConstant.CONFIG_PATH, 'r', encoding='utf-8') as f:
        config_dict_local = yaml.safe_load(f)

    logger.add(config_dict_local[EnvConstant.LOG][EnvConstant.LOG_PATH] + "/" +
               config_dict_local[EnvConstant.LOG][EnvConstant.LOG_FILE] + "_{time}.log",
               rotation=config_dict_local[EnvConstant.LOG][EnvConstant.LOG_ROTATION],
               retention=config_dict_local[EnvConstant.LOG][EnvConstant.LOG_RETENTION])

    page_url_base = config_dict_local['chinanews']['page_url_base']
    get_headers = config_dict_local['get_headers']
    
    chinanews = Chinanews(page_url_base, get_headers)
    chinanews.page_number = int(input("爬取新闻页数（每页10篇新闻）："))
    chinanews.run()

