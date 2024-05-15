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

@logger.catch()
def get_response(people_search_url, key_word, page, referer, headers, payloads):
    """获取json格式的响应"""
    headers['Referer'] = referer
    payloads['key'] = key_word
    payloads['page'] = page
    # 发起 post 请求
    response = requests.post(people_search_url, headers=headers, data=json.dumps(payloads))
    return response.json()

@logger.catch()
def get_news_urls(response):
    #解析数据
    records = response[CrawlerConstant.DATA][CrawlerConstant.RECORDS]
    news_urls = []
    for record in records:
        news_url = record[CrawlerConstant.URL]
        news_urls.append(news_url)
    return news_urls

@logger.catch()
def save_news(news_url, dir_name, get_headers, theme1, save_path="./3级分类新闻"):
    """保存新闻"""
    response = requests.get(url=news_url, headers=get_headers, timeout=10)
    charset = re.findall('content="text/html;charset=(.*?)"', response.text, re.S)[0]
    if charset == 'GB2312':
        response.encoding = 'GB2312'
    else:
        response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, CrawlerConstant.HTML_PARSER)
    content = soup.find(class_=CrawlerConstant.RM_TXT_CON_CF).text

    old_title = re.findall('<title>(.*?)</title>', response.text, re.S)[0]
    title = re.sub(r'[\/:*?"<>|\n\t ]', '', old_title)
    date = re.findall('<meta name="publishdate" content="(.*?)"', response.text, re.S)[0]
    
    news_path = os.path.join(save_path, theme1, dir_name)
    create_news_xml(date, title, content, dir_name, news_path)

if __name__ == "__main__":
    # 载入配置文件
    with open(EnvConstant.CONFIG_PATH, 'r', encoding='utf-8') as f:
        config_dict_local = yaml.safe_load(f)

    logger.add(config_dict_local[EnvConstant.LOG][EnvConstant.LOG_PATH] + "/" +
               config_dict_local[EnvConstant.LOG][EnvConstant.LOG_FILE] + "_{time}.log",
               rotation=config_dict_local[EnvConstant.LOG][EnvConstant.LOG_ROTATION],
               retention=config_dict_local[EnvConstant.LOG][EnvConstant.LOG_RETENTION])
    start_page = CrawlerConstant.START_PAGE
    end_page = CrawlerConstant.END_PAGE
    headers = config_dict_local['peplenews']['headers']
    payloads = config_dict_local['peplenews']['payloads']
    get_headers = config_dict_local['get_headers']

    for i in range(0, 8):
        topics = config_dict_local['topics'][i]
        theme1 = config_dict_local['theme1'][i]
        for key_word in topics:
            
            key_word_parse = parse.quote(key_word)
            referer = config_dict_local['peplenews']['referer_base'].format(key_word_parse)
        
            for page in range(start_page, end_page + 1):
                response = get_response(config_dict_local['peplenews']['people_search_url'], 
                                        key_word, page, referer, headers, payloads)
                news_urls = get_news_urls(response)
                for news_url in news_urls:
                    save_news(news_url, key_word, get_headers, theme1)
                    time.sleep(0.1)
    
