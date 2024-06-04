import requests, os
from bs4 import BeautifulSoup

def download_xwlb_txt(url, text_name):
    """
        爬取新闻联播演讲稿
    """

    # 设置请求头,模拟浏览器行为
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 发送 HTTP 请求并获取响应
    response = requests.get(url, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取所有段落文本
        paragraphs = soup.find_all('p')
        text = '\n'.join([p.get_text() for p in paragraphs])

        # 打印提取的文本
        file_name = os.path.join('./xwlbText', text_name)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(text)
    else:
        print(f'抱歉,无法成功爬取网页内容。响应状态码: {response.status_code}')