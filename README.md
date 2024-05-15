# 爬虫代码

## 新闻政策爬虫

.
|-- README.md
|-- config
|-- constant
|-- util
|-- 3级分类新闻
|-- data
|-- log
|-- chinanews.py
|-- peoplenews.py
|-- policy_ckcest.py

其中peoplenews.py用以爬取一定数量所有主题的新闻，chinanews.py，policy_ckcest.py用以输入特定主题补充特定主题的数据。

### TODO

- peoplenews.py：直接运行即可
- chinanews.py：按提示输入主题爬取数量
- policy_ckcest.py：在配置文件config中将cookie_get跟换为自己电脑相关网页的cookie，按提示输入主题爬取数量


### Requirement

pip包：

```shell
loguru==0.7.2
PyYAML==6.0
Requests==2.31.0
beautifulsoup4==4.12.3
```

