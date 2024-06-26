# 新闻联播数据集成文档
## 概述

<img src="image/image-20240523104301237.png" alt="image-20240523104301237" style="zoom: 67%;" />

- 为什么不采用OCR
  - 新闻联播没有字幕


## 快速开始
-  安装java8
```shell
apt-get install openjdk-8-jdk
java -version
```
-  安装browsermob-proxy
```shell
pip install browsermob-proxy
```
-  下载java端BrowserMob-Proxy包
```
http://bmp.lightbody.net/
```

## 获取视频下载链接
```python
python get_urls_txt.py
```

## 视频下载链接重定向
```python
python urls_redirect.py
```

## 视频下载
```python
python download.py
```
ps：如果遇到问题，请使用`sh clean.sh`之后，重新运行程序

## 视频格式转换
```python
python convert.py
```

## 新闻联播演讲稿下载
```python
python dowload_xwlb_text.py
```
