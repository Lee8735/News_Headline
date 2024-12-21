# ===================================================================================================
# %% 필요 모듈 import
from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import datetime



# ===================================================================================================
# %% 브라우저 열기.
Options = ChromeOptions()

# 브라우저가 요청을 보내면 아래의 user_agent를 보내게 되어 있다.
# 이걸 안주면 차단 당할 수 있다.
user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0')

Options.add_argument('user_agent=' + user_agent)
Options.add_argument('long=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=Options)

# 사용할 타이틀 리스트
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']



# ===================================================================================================
# %% 웹에서 크롤링.
# for k: 뉴스 카테고리 번호.
# for n: 기사제목 더보기 버튼 클릭 횟수
# for i: 한번에 크롤링할 뉴스제목 수
# for j: 한 레이어에 존재하는 뉴스제목 수
for k in range(0, 1):

    # 크롤링 한 데이터가 저장될 데이터 프레임
    df_titles = pd.DataFrame()


    # 크롤링 한 제목들이 저장될 리스트.
    titles = []


    # 웹 페이지 열기
    url = f'https://news.naver.com/section/10{k}'
    driver.get(url)


    # 경제텝의 버튼 주소가 다름.
    if k == 1:
        button_xpath = '//*[@id="newsct"]/div[5]/div/div[2]'
    else:
        button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'


    # 버튼 눌러서 기사 제목 더 띄우기
    for n in range(40):
        time.sleep(0.8)

        # 위에서 정한 XPATH로 Element를 찾아서 클릭함.
        driver.find_element(By.XPATH, button_xpath).click()


    # 크롤링
    for i in range(1, 240):
        for j in range(1, 7):
            # div[1] 부터 div[] 하나에 li가 6개씩 들어감.
            # div[3] 은 제외되어야 함.

            if k == 1:
                title_xpath = ('//*[@id="newsct"]'
                               '/div[5]/div/div[1]'
                               f'/div[{i}]/ul/li[{j}]'
                               '/div/div/div[2]/a/strong')
            else:
                title_xpath = ('//*[@id="newsct"]'
                               '/div[4]/div/div[1]'
                               f'/div[{i}]/ul/li[{j}]'
                               '/div/div/div[2]/a/strong')

            try:
                # 제목 하나를 크롤링해서 가져옴
                title = driver.find_element(By.XPATH, title_xpath).text
                # 가져온 제목에서 한글만 남김
                title = re.compile('[^가-힣 ]').sub('', title)
                # 그걸 리스트에 추가
                titles.append(title)

                # 디버깅용
                # print(title)
            except:
                print(i, j)


    # 위에서 만들어진 리스트를 데이터 프레임으로 저장.
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[k]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)


    # 파일명에 저장한 시간 추가해서 dataframe을 csv파일로 저장.
    date_str = f'{datetime.datetime.now().strftime("%y%m%d")}'
    fileName = f'NaverNews_Headline_Data_{k}_{date_str}'
    df_titles.to_csv(f'./crawling_data/{fileName}.csv', index=False)


    # 저장된 데이터프레임 확인.
    print(df_titles.head())
    df_titles.info()
    print(df_titles['category'].value_counts())


# 30초 뒤 웹페이지 종료
time.sleep(5)
driver.close()



# ===================================================================================================
# %%
# 나눠진 CSV 파일3개를 합쳐서 하나의 CSV로 저장함.
df1 = pd.read_csv('./crawling_data/naver_headline_news_0_1_241219.csv')
df2 = pd.read_csv('./crawling_data/naver_headline_news_2_3_241219.csv')
df3 = pd.read_csv('./crawling_data/naver_headline_news_4_5_241219.csv')

df_titles = pd.concat([df1, df2], axis='rows', ignore_index=True)
df_titles = pd.concat([df_titles, df3], axis='rows', ignore_index=True)

date_str = datetime.datetime.now().strftime("%y%m%d")
df_titles.to_csv(f'./crawling_data/headline_data_{date_str}.csv', index=False)

df_titles.info()
print(df_titles['category'].value_counts())


