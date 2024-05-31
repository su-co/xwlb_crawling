# -*- coding:utf-8 -*-

import asyncio
from utils.utils_download import url2date, get_split_video_url, download_all, merge

# 从文件中获取url
url = "http://tv.cctv.com/2016/01/31/VIDEgJmIyftgT6yETXK8V9ZG160131.shtml"

# 获取日期, 作为视频名称
video_name = url2date(url)

# 获取视频分片url
url = get_split_video_url(url)

# 构建视频分片url模板，异步爬取
if url:
    asyncio.run(download_all(url)) # 下载分片
    merge(video_name) #合并分片到xwlb/$video_name
    
    
