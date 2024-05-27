import datetime
from utils.utils_get_urls import generate_xwlb_url_txt

base_url_2011_2015 = "https://cctv.cntv.cn/lm/xinwenlianbo/{date}.shtml"
base_url_2016_2024 = "https://tv.cctv.com/lm/xwlb/day/{date}.shtml"

# 设置起始日期
start_date = datetime.date(2015, 1, 1)
# change_date = datetime.date(2015, 1, 5)
change_date = datetime.date(2016, 2, 5)
end_date = datetime.date(2024, 5, 22)

# 设置保存路径
save_url_file = open("xwlb_urls.txt", "w")

# 新闻联播url
generate_xwlb_url_txt(base_url=base_url_2011_2015, start_date=start_date,
                      end_date=change_date, save_url_file=save_url_file, all=False)
generate_xwlb_url_txt(base_url=base_url_2016_2024, start_date=change_date,
                      end_date=end_date, save_url_file=save_url_file, all=False)

save_url_file.close()