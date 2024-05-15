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
from util.create_xml import create_policy_ckcest_xml

@logger.catch()
def get_response_by_title(people_search_url, key_word, page, referer, 
                          cookie_title, headers, payloads):
    """获取json格式的响应"""
    headers['Cookie'] = cookie_title
    headers['Referer'] = referer
    payloads['page'] = page 
    payloads['secondSearchExpress'] = "TI=" + key_word
    # 发起 post 请求
    response = requests.post(people_search_url, headers=headers, data=json.dumps(payloads))
    return response.json()

@logger.catch()
def get_response_by_text(people_search_url, key_word, page, referer, cookie_text, headers, payloads):
    """获取json格式的响应"""

    headers['Cookie'] = cookie_text
    headers['Referer'] = referer
    payloads['page'] = page
    payloads['text'] = key_word
    # 发起 post 请求
    response = requests.post(people_search_url, headers=headers, data=json.dumps(payloads))
    return response.json()

@logger.catch()
def get_news_urls(response):
    #解析数据
    records = response[CrawlerConstant.DATAS][CrawlerConstant.RECORDS]
    news_urls = []
    for record in records:
        news_url = 'https://policy.ckcest.cn/detail/' + record["dataId"] + '.html'
        news_urls.append(news_url)
    return news_urls

@logger.catch()
def save_news(news_url, dir_name, referer, cookie_get, headers, save_path="./data"):
    headers['Cookie'] = cookie_get
    headers['Referer'] = referer
    response = requests.get(url=news_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, CrawlerConstant.HTML_PARSER)
    old_content = re.findall('<meta name="description" content="(.*?)"', response.text, re.S)[0]
    content = re.sub(r'[\n\t ]', '', old_content)

    old_title = soup.find(class_=CrawlerConstant.KDS_TITLT_L_LF).text
    title = re.sub(r'[\/:*?"<>|\n\t ]', '', old_title)

    policy_path = os.path.join(save_path, dir_name)
    create_policy_ckcest_xml(title, content, dir_name, policy_path)

if __name__ == "__main__":
    # 载入配置文件
    with open(EnvConstant.CONFIG_PATH, 'r', encoding='utf-8') as f:
        config_dict_local = yaml.safe_load(f)

    logger.add(config_dict_local[EnvConstant.LOG][EnvConstant.LOG_PATH] + "/" +
               config_dict_local[EnvConstant.LOG][EnvConstant.LOG_FILE] + "_{time}.log",
               rotation=config_dict_local[EnvConstant.LOG][EnvConstant.LOG_ROTATION],
               retention=config_dict_local[EnvConstant.LOG][EnvConstant.LOG_RETENTION])
    
    headers = config_dict_local['policy_ckcest']['headers']
    payloads = config_dict_local['policy_ckcest']['payloads']
    search_url = config_dict_local['policy_ckcest']['search_url']

    cookie_get = config_dict_local['policy_ckcest']['cookie_get']
	# 起始页，终止页，关键词设置
    start_page = CrawlerConstant.START_PAGE
    end_page = int(input("爬取新闻页数（每页20篇新闻）："))
    key_word = input("查询主题：")
    key_word_parse = parse.quote(key_word)
    
    # 在这里，采用哪种方式搜索就采用相关的数据，并在for循环中调用相应的函数
    referer_base_title = config_dict_local['policy_ckcest']['referer_base_title']
    cookie_title = config_dict_local['policy_ckcest']['cookie_title']
    referer = referer_base_title.format(key_word_parse)
    # referer_base_text = config_dict_local['policy_ckcest']['referer_base_text']
    # cookie_text = config_dict_local['policy_ckcest']['cookie_text']
    # referer = referer_base_text.format(key_word_parse)

    for page in range(start_page, end_page + 1):
        response = get_response_by_title(search_url, key_word, page, referer, cookie_title, 
                                         headers, payloads)
        # response = get_response_by_text(search_url, key_word, page, referer, cookie_text, 
        #                                 headers, payloads)
        news_urls = get_news_urls(response)
        for news_url in news_urls:
            save_news(news_url, key_word, referer, cookie_get, headers)
            time.sleep(1)

