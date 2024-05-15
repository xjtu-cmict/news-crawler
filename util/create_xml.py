import xml.etree.ElementTree as ET
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.split(current_directory)[0]
sys.path.append(root_path)
 
from constant.crawler_constant import CrawlerConstant


def create_news_xml(date, title, content, dir_name, news_path):
    if not os.path.exists(news_path):
        os.makedirs(news_path)
    # 创建根元素
    root = ET.Element(CrawlerConstant.TEXT)

    theme3_tag = ET.SubElement(root, CrawlerConstant.THEME3)
    theme3_tag.text = dir_name

    date_tag = ET.SubElement(root, CrawlerConstant.DATE)
    date_tag.text = date

    title_tag = ET.SubElement(root, CrawlerConstant.TITLE)
    title_tag.text = title

    content_tag = ET.SubElement(root, CrawlerConstant.CONTENT)
    content_tag.text = content
    
    # 创建 XML 对象
    tree = ET.ElementTree(root)

    # 构造文件名
    file_path = os.path.join(news_path, title + '.xml')

    # 保存到文件，指定编码为 UTF-8
    tree.write(file_path, encoding="utf-8")


def create_policy_ckcest_xml(title, content, dir_name, news_path):
    if not os.path.exists(news_path):
        os.makedirs(news_path)
    # 创建根元素
    root = ET.Element(CrawlerConstant.TEXT)

    theme2_tag = ET.SubElement(root, CrawlerConstant.THEME3)
    theme2_tag.text = dir_name

    title_tag = ET.SubElement(root, CrawlerConstant.TITLE)
    title_tag.text = title

    content_tag = ET.SubElement(root, CrawlerConstant.CONTENT)
    content_tag.text = content
    
    # 创建 XML 对象
    tree = ET.ElementTree(root)

    # 构造文件名
    file_path = os.path.join(news_path, title + '.xml')

    # 保存到文件，指定编码为 UTF-8
    tree.write(file_path, encoding="utf-8")