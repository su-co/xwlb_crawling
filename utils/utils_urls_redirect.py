def url_redirect(url):
    # 去掉末尾的 ~ 字符 和换行符
    url = url.rstrip('~\n')
    
    # 将https转换为http
    if url.startswith('https://'):
        url = url.replace('https://', 'http://')

    # 判断 URL 是否以 'http://news.cntv.cn' 开头
    if url.startswith('http://news.cntv.cn'):
        new_url = url.replace('http://news.cntv.cn', 'http://tv.cctv.com')
    else:
        # 其他情况,直接返回原始 URL
        new_url = url

    return new_url