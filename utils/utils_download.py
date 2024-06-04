# -*- coding:utf-8 -*-

import time, re, requests, asyncio, aiohttp, aiofiles, os, shutil
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_hls_url(url):
    """
        监听浏览器访问CCTV视频网址的过程，找到真实m3u8地址
    """
    # 设置 browsermob 代理
    browsermobproxy_client_location = "./browsermob-proxy-2.1.4/bin/browsermob-proxy"
    server = Server(browsermobproxy_client_location)
    server.start()
    proxy = server.create_proxy(params={"trustAllServers": "true"})

    # S设置 Chrome webdriver
    chrome_location = "/usr/bin/google-chrome"
    chromedriver_location = "/usr/bin/chromedriver"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_location
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy)) # Setup proxy to point to our browsermob so that it can track requests
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    s = Service(chromedriver_location)
    browser = webdriver.Chrome(options = chrome_options, service = s)

    # 加载
    proxy.new_har("Example", options={'captureHeaders': True, 'captureContent': True})
    browser.get(url)
    time.sleep(2) # 需要给响应时间

    # 获取监听信息
    result = proxy.har
    result_str = str(result)

    # 反转义字符串
    decoded_str = result_str.encode().decode('unicode_escape')

    # 使用正则表达式匹配 hls_url 后面的 HTTP 网址
    match = re.search(r'"hls_url":"(http://[^"]+)"', decoded_str)

    if match:
        hls_url = match.group(1)
    else:
        hls_url = None

    server.stop()
    browser.quit()
    
    return hls_url

def get_split_video_url(url):
    """
        获取分片video的URL
    """
    hls_url = get_hls_url(url)

    # 获取失败，返回为空（失败的原因，例如视频不存在、响应时间不足等）
    if not hls_url:
        return None
    
    response = requests.get(hls_url)

    for line in response.content.decode().splitlines():
        if not line.startswith("#"):
            mid = line
            break
    
    if not mid:
        return None
        
    combined_url = hls_url.split('/')[0] + '//' + hls_url.split('/')[2] + mid
    
    return combined_url.rsplit('/', 1)[0]

def url2date(url):
    """
        从url中提取日期, 便于后面视频命名
    """
    # 使用更宽松的正则表达式
    date_pattern = r'\d{4}/\d{2}/\d{2}'
    date_match = re.search(date_pattern, url)

    if date_match:
        date = date_match.group().replace('/', '')
        return date
    else:
        return None

##################################
# download
##################################

async def download_one(url,sem):
    try:
        async with sem:
            file_name = url.split("/")[-1]
            async with aiohttp.ClientSession() as session:
                # 发送请求
                async with session.get(url) as res:
                    content = await res.content.read()
                # 异步写入文件
                async with aiofiles.open(f"temp/{file_name}",mode="wb") as f:
                    await f.write(content)
    except Exception as e:
        print(e)
        
async def download_all(url):
    """
        url为真实视频分片地址前缀
    """
    if not url:
        return
        
    # 视频分片的url模板
    url_template = f"{url}/{{}}.ts"
    
    # 信号量
    sem = asyncio.Semaphore(20)
    tasks = []
    for i in range(200): # 新闻联播通常为200个分片
        url = url_template.format(i) # 根据模板创建真实的视频地址
        task = asyncio.create_task(download_one(url,sem))
        tasks.append(task)
    await asyncio.wait(tasks)
    
################################
# 合并ts分片
################################
    
def merge(date):
    # 设置文件所在目录
    directory = './temp'

    # 创建一个新文件用于合并
    output_file = os.path.join('./xwlb', date)

    # 初始化一个空列表保存所有ts文件的内容
    contents = []

    # 遍历目录中所有的ts文件,读取内容并添加到列表中
    for i in range(200):
        file_path = os.path.join(directory, f'{i}.ts')
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                contents.append(file.read())

    # 将列表中的内容写入到合并后的文件中
    with open(output_file, 'wb') as file:
        file.write(b'\n'.join(contents))

   #  print(f'文件已成功合并到 {output_file}')
    
    # temp 文件夹归空
    if os.path.exists(directory):
        shutil.rmtree(directory)
        os.makedirs(directory)
    
    return output_file 
