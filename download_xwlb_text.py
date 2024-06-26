import datetime
from tqdm import tqdm
from utils.utils_download import url2date
from utils.utils_download_text import download_xwlb_txt

# 原始 URL
original_url = 'http://mrxwlb.com/2015/12/22/2015年12月22日新闻联播文字版'

# 结束日期
end_date = datetime.date(2024, 5, 22)

# 计算总天数
total_days = (end_date - datetime.date(2015, 12, 22)).days + 1

# 遍历到结束日期
# current_date = datetime.date(2015, 12, 22)
current_date = datetime.date(2024, 1, 1)
with tqdm(total=total_days, unit="日", desc="遍历进度") as pbar:
    while current_date <= end_date:
        # data for 2024
        url = original_url.replace('2015/12/22', current_date.strftime('%Y/%m/%d'))
        url = url.replace('2015年12月22日', current_date.strftime('%Y年%m月%d日'))
        # data before 2024
        # formatted_date_path = current_date.strftime('%Y/%m/%d')
        # formatted_date_text = f"{current_date.year}年{current_date.month}月{current_date.day}日"
        # url = original_url.replace('2015/12/22', formatted_date_path)
        # url = url.replace('2015年12月22日', formatted_date_text)
        
        print(url)
        text_name = url2date(url)
        download_xwlb_txt(url, text_name)
        current_date += datetime.timedelta(days=1)
        pbar.update(1)