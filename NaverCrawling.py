import sys

import numpy as np
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from konlpy.tag import Okt #한국어 형태소 분석기
from collections import Counter, OrderedDict
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image

URL_BEFORE_KEYWORD= "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
UTL_BEFORE_PAGE_NUM =("&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=24&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=")

def get_link(keyword,page_range):
    link = []
    for page in range(page_range):
        current_page = 1+page*10
        crawling_url = URL_BEFORE_KEYWORD + keyword + UTL_BEFORE_PAGE_NUM + str(current_page)

        response=requests.get(crawling_url)
        soup = BeautifulSoup(response.text,"lxml")
        url_tag=soup.select("a.news_tit")

        for url in url_tag:
            link.append(url["href"])


    print(link)
    return link

#신문사 마다 태그가 다른 ->newspaper Article 사용
def get_article(file1,link):
    with open(file1,"w",encoding="utf8") as f:

        for url2 in link:
            article = Article(url2,language="ko")
            try:
                article.download()
                article.parse()
            except:
                continue
            news_title=article.title
            news_content = article.text

            f.write(news_title)
            f.write(news_content)

    f.close()

def wordcount(file1,file2):
    f = open(file1,"r", encoding="utf8")
    g= open(file2,"w", encoding="utf8")

    engine = Okt()
    data= f.read()
    all_nonus = engine.nouns(data)
    nonus = [n for n in all_nonus if len(n) >1 ]
    count = Counter(nonus)

    #Dictionary = {Key:Value} <- t[0], t[1] t[0] <- KEY
    # by_num=OrderedDict(sorted(count.items(),key=lambda t:t[1] ,reverse= True))
    by_num = sorted(count.items(),key=lambda t:(-t[1],t[0]) )
    by_num = dict(by_num)
    # print(by_num)
    # print(dict(by_num))
    word=[i for i in by_num.keys()]
    number = [i for i in by_num.values()]

    for i,j in zip(word,number):
        final = f"{i}   {j}"
        g.write(final+"\n")
    f.close()
    g.close()
    return by_num, count

def top_n(count,file3):
    g = open(file3,"w",encoding="utf8")
    rank=dict(count.most_common(10))
    print(rank)
    word = [i for i in rank.keys()]
    number = [i for i in rank.values()]

    for i, j in zip(word, number):
        final = f"{i}   {j}"
        g.write(final + "\n")

    g.close()
    return rank

def full_vis_var(by_num):
    for w,n in list(by_num.items()):
        if n<=15:
            del by_num[w]
    fig = plt.gcf()
    fig.set_size_inches(20,10) # 1-> 100pixel, 20 ->2000pixel
    matplotlib.rc("font",family="Malgun Gothic",size=10)
    plt.title("기사에 나온 전체 단어 개수", fontsize=30)
    plt.xlabel("기사에 나온 단어",fontsize=20)
    plt.ylabel("기사에 나온 단어 개수",fontsize=20)
    plt.bar(by_num.keys(),by_num.values(),color="#6799FF")
    plt.xticks(rotation=45)
    plt.savefig("all_words.jpg")
    plt.show()


def full_vis_bar(by_num):
    pass

def wordcloud(by_num):
    wc = WordCloud(font_path="malgun", background_color=(168,237,244),width=2500,height=1500)
    cloud=wc.generate_from_frequencies(by_num)# 딕셔너리가 들어가야함
    plt.imshow(cloud,interpolation="bilinear")#interploation 선명도
    plt.axis("off")
    plt.savefig("wordcloud.jpg")
    plt.show()

def wordcloud2(by_num):
    masking_image = np.array(Image.open("alice_mask.png"))
    wc = WordCloud(font_path="malgun", background_color="white",width=2500,height=1500,mask=masking_image)
    cloud=wc.generate_from_frequencies(by_num)# 딕셔너리가 들어가야함
    plt.imshow(cloud,interpolation="bilinear")#interploation 선명도
    plt.axis("off")
    plt.savefig("wordcloud2.jpg")
    plt.show()
def topn_vis_bar(rank):
    topn_data=dict(rank)
    fig = plt.gcf()
    fig.set_size_inches(20, 10)  # 1-> 100pixel, 20 ->2000pixel
    matplotlib.rc("font", family="Malgun Gothic", size=10)
    plt.title("기사에 나온 전체 단어 개수", fontsize=30)
    plt.xlabel("기사에 나온 단어", fontsize=20)
    plt.ylabel("기사에 나온 단어 개수", fontsize=20)
    plt.bar(topn_data.keys(), topn_data.values(), color="red")
    plt.xticks(rotation=45)
    plt.savefig("top_words.jpg")
    plt.show()


#argv 띄어쓰기를 기준으로 값을 받음
def main(argv):
    link=get_link(argv[1], int(argv[2]))
    get_article("수집내용.txt",link)
    by_num,count=wordcount("수집내용.txt","워드카운트.txt")
    full_vis_var(by_num)
    rank=top_n(count,"상위10개.txt")
    topn_vis_bar(rank)
    # wordcloud(by_num)
    wordcloud2(by_num)
if __name__=="__main__":
    main(sys.argv)

