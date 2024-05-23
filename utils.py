import requests, re
from bs4 import BeautifulSoup

def url_match(url):
    """
        根据给定的url进行匹配, 匹配成功返回新闻联播url
        否则返回为空
    """
    url = str(url)
    pattern_2011 = r"https?://news\.cntv\.cn/\d{4}/\d{2}/\d{2}/VIDE([a-zA-Z0-9]+)\.shtml"
    pattern_2024 = r"^https?://tv\.cctv\.com/(\d{4})/(\d{2})/(\d{2})/VIDE([a-zA-Z0-9]+)\.shtml$"
    
    match_2011 = re.match(pattern_2011, url)
    match_2024 = re.match(pattern_2024, url)
    
    if match_2011 or match_2024:
        return url
    else:
        return None

def get_xwlb_url(url, all):
    """
    根据url解析HTML页面, 返回新闻联播url
    all: bool, 如果需要完整的新闻联播视频及其视频分片, all = True
        如果只需要完整的新闻联播视频, all = False
    return: 返回url_list
    """
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    # 解析HTML内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 找到包含标签a的文本
    a_tags = soup.find_all('a')
    
    # 收集超文本链接<a href>
    href_list = []
    for tag in a_tags:
        href = tag.get('href')
        if url_match(href): # 匹配新闻联播url格式, 去除其他url
            href_list.append(href)
            href_list.append('~') # url中不会出现的字符，用于分隔
            if not all:
                return href_list
    return href_list

import datetime
from tqdm import tqdm
def generate_xwlb_url_txt(base_url, start_date, end_date, save_url_file, all=False):
    """
        根据base_url不断调整日期, 范围[start_date, end_date],
        最终生成新闻联播视频url的txt文件
        文件格式：每一行代表一个日期, 如果一行仅有一个url, 代表完整新闻联播视频url
        若一行存在多个url, 代表完整新闻联播视频url及其分片url（使用~分隔）
    """
    total_days = (end_date - start_date).days + 1
    with tqdm(total=total_days, unit="day") as pbar:
        current_date = start_date
        while current_date <= end_date:
            url = base_url.format(date=current_date.strftime("%Y%m%d"))
            url_list = get_xwlb_url(url=url, all=all)
            if url_list:
                save_url_file.writelines(url_list)
                save_url_file.write("\n")
            current_date += datetime.timedelta(days=1)
            pbar.update(1)