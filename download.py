# -*- coding:utf-8 -*-

import asyncio, os
from tqdm import tqdm
from utils.utils_download import url2date, get_split_video_url, download_all, merge

def down(url, video_name):    
    # 获取分片
    url = get_split_video_url(url)

    if url:
        asyncio.run(download_all(url)) # 下载分片
        output_file = merge(video_name) # 合并
        return output_file

def check_file(file_path):
    """
    检查给定文件路径是否存在,并判断文件大小是否大于100字节。
    
    参数:
    file_path (str): 文件路径
    
    返回:
    tuple(bool, bool): 第一个元素表示文件是否存在,第二个元素表示文件大小是否大于100字节
    """
    if not file_path:
        return (False, False)
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        return (True, file_size > 10000000)
    else:
        return (False, False)

with open('xwlb_redir_urls.txt', 'r') as f:
    urls = f.readlines()

for url in tqdm(urls, desc='Processing URLs', unit='url'):
    url = url.strip()

    # 获取日期, 作为视频名称
    video_name = url2date(url)

    while(True):
        output_file = down(url, video_name)
        exist, size = check_file(output_file)
        if not exist:
            break
        if size:
            break
    
    
