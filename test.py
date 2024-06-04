from tqdm import tqdm

# 读取 URL 文件
with open('xwlb_redir_urls.txt', 'r') as f:
    urls = f.readlines()

# 遍历URL并显示进度条
for url in tqdm(urls, desc='Processing URLs', unit='url'):
    url = url.strip()
    # 在这里执行对 URL 的处理操作
    print(url)
