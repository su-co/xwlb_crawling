# -*- coding:utf-8 -*-

from utils.utils_urls_redirect import url_redirect

with open('xwlb_urls.txt', 'r') as f:
    urls = f.readlines()

# URL 重定向
new_urls = []
for url in urls:
    new_url = url_redirect(url) # 包括更换 URL 前缀、去除分隔符~等 
    new_urls.append(new_url)

# 将修改后的 URL 写入新文件
with open('xwlb_redir_urls.txt', 'w') as f:
    for new_url in new_urls:
        f.write(new_url+ '\n')
