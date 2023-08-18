import time
import pandas as pd
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.by import By

df = pd.DataFrame()
totalDataList = list()

keyword = str(input("수집할 키워드를 입력하세요 : "))
input_page_number = int(input("수집할 페이지 개수를 입력하세요 : "))
page_count = 1

driver = webdriver.Chrome()
driver.maximize_window()
time.sleep(1)

driver.get("https://www.naver.com/")

driver.find_element(By.XPATH, '//*[@id="query"]').send_keys(keyword)
time.sleep(1)

driver.find_element(By.ID, 'search-btn').click()
time.sleep(1)

driver.find_element(By.LINK_TEXT, '뉴스').click()

for page in range(1, input_page_number+1):
    page_xpath = f'//*[@id="main_pack"]/div[2]/div/div/a[{page}]'
    driver.find_element(By.XPATH, page_xpath).click()
    time.sleep(2)

    # news_title = driver.find_elements(By.CSS_SELECTOR, 'a.news_tit')
    news_title = driver.find_elements(By.CLASS_NAME, "news_tit")

    for i in news_title:
        news_href_ = i.get_attribute("href")

        article = Article(news_href_, language='ko')

        try:
            article.download()
            article.parse()
        except:
            continue

        pan_title = article.title
        pan_content = article.text.strip().replace("\n", "")

        engine = Okt()
        all_nouns = engine.nouns(pan_content)
        nouns = [n for n in all_nouns if len(n) > 1]

        count = Counter(nouns)
        by_num = OrderedDict(sorted(count.items(), key=lambda t: t[1], reverse=True))

        word_5 = ",".join(list(by_num)[:5])

        dataList = [str(pan_title), str(pan_content), str(news_href_), str(word_5)]
        totalDataList.append(dataList)
        print(f"{page_count}'s data insert to dataframe complete")
        page_count += 1

df = pd.DataFrame(totalDataList, columns=["제목", "내용", "기사 URL", "단어 5가지"])
print(df)
df.to_csv("selenium_naver_news.csv", encoding="utf-8-sig", index=False)
print("all working's complete.")
driver.close()