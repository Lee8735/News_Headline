from operator import index

from bs4 import  BeautifulSoup
import requests
import re
import pandas as pd
import datetime

from unicodedata import category


#
# url = 'https://news.naver.com/section/100'
#
#
#
# # 주소를 주고 requests하면 html문서를 받아서 반환한다.
# resp = requests.get(url)
#
# print(list(resp))
#
# # html 문서로 파싱해줌.
# soup = BeautifulSoup(resp.text, 'html.parser')
# print(soup)
#
# # sa_text_srtong 클래스를 선택해서
# # 웹 페이지의 그 문자들을 모두 읽어옴
# title_tags = soup.select('.sa_text_strong')
#
# print(len(title_tags))
#
# for title_tags in title_tags:
#     print(title_tags.text)


# 카테고리 라벨을 만듬
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']


# 빈 데이터 프레임을 만듬
df_titles = pd.DataFrame()


# 웹 크롤링
for i in range(0,7):
    # 주소를 기사 카테고리 마다 바꿈.
    url = f'https://news.naver.com/section/10{i}'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sa_text_strong')



    titles = []
    #제목만 뽑아서 리스트를 만듬
    for title_tags in title_tags:

        title = title_tags.text
        # 제목의 문장부호, 한자, 영어, 숫자를 없앰.
        # []안에 공백주지 않으면 다 붙음.
        # [^가-힣 ] 는 한글 처음부터 끝까지 라는 의미.
        # sub는 위의거 이외의 문자는 빼고 ' '(공백)로 채우라는 의미.
        title = re.compile('[^가-힣 ]').sub(' ', title)
        titles.append(title)



    # 빈 데이터 프레임에 추가함.
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)



# 저장된 데이터프레임 확인.
print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

# 파일명에 저장한 시간 추가해서 dataframe을 csv파일로 저장.
# 시간은 나노초 단위까지 구분 가능하다.
df_titles.to_csv(f'../crawling_data/naverNews_headline_Data_{datetime.datetime.now().strftime("%y%m%d")}.csv', index= False)


print('hello')







