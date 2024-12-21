#===================================================================================================
#%% 필요 모듈 import
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import pickle
from konlpy.tag import Okt

from keras._tf_keras.keras.models import *
from keras._tf_keras.keras.layers import *
from keras._tf_keras.keras.utils import to_categorical

from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras._tf_keras.keras.preprocessing.sequence import pad_sequences



#===================================================================================================
#%% CSV파일 불러오기

# csv를 데이터 프레임으로 읽음.
csv_dir = './crawling_data/'
csv_name = 'naver_headline_news_241219.csv'
df = pd.read_csv(csv_dir + csv_name)

# CSV파일을 읽어서 확인.
print(df.head())
print(df.info())
print(df.category.value_counts())

# 열을 나눔.
X = df['titles']
Y = df['category']



#===================================================================================================
# 카테고리 열 전처리
#===================================================================================================
#%% 카테고리 더미화.
encoder = LabelEncoder()
# fit_transform은 처음 한번만 해야한다.
labeled_y = encoder.fit_transform(Y)
print(labeled_y[:3])

label = encoder.classes_
print(label)

# Y = pd.get_dummies(Y)
# print(Y.head())


# 더미화 할 때 인코더의 라벨 정보를 파일로 저장.
with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

onehot_Y = to_categorical(labeled_y)
print(onehot_Y)



#===================================================================================================
# 제목 열 전처리
#===================================================================================================
#%% 제목의 형태소 분리

# 한국어는 한글자로 이루어진 단어가 많음 -> 학습이 안됨.
# '와, 그리고, 또는' 같은 접속사는
# 기사제목의 카테고리를 분류하는데 도움이 안됨.
# 대명사, 감탄사 등도 마찬가지 임.
# 이런 불용어(자연어 처리: 학습에 쓸모없는 단어들)는
# 빼줘야 됨.

print(X[0])
okt = Okt()
# okt_x = okt.morphs(X[0])
# print(okt_x)

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)

print(X)



#===================================================================================================
#%% stopwords 제거

# stopwords 목록을 CSV에서 불러옴.
stopwords_dir = './stopwords/stopwords.csv'
stopwords = pd.read_csv(stopwords_dir, index_col=0)
print(stopwords)


# 뉴스 제목들에서 위의 목록에 포함된 것들을 제거.
# for sentence: 하나의 문장을 인덱싱
# for word: 하나의 문장의 한 형태소를 인덱싱
for sentence in range(len(X)):

    words = []

    for word in range(len(X[sentence])):
        if len(X[sentence][word]) > 1:
            if X[sentence][word] not in list(stopwords['stopword']):
                # 글자수가 1보다 크고, stopword 목록에 없으면 리스트에 추가.
                words.append(X[sentence][word])

    # 리스트의 형태소들을 공백하나로 분리하여 하나의 문장으로 합쳐서 다시 저장.
    X[sentence] = ' '.join(words)


print(X[:5])



#===================================================================================================
#%% 문장상태로는 모델에게 주지 못해서 형태소마다 숫자로 라벨링.
# 이 때 숫자는 명목척도 이다.
token = Tokenizer()

token.fit_on_texts(X)

tokened_X = token.texts_to_sequences(X)

# 단어 개수
# 패딩을 하기 위해서 +1로 토큰화된 개수를 늘려줌.
wordsize = len(token.word_index) + 1

print(tokened_X[:5])



#===================================================================================================
#%% 문장들의 길이가 다르므로 앞쪽을 0으로 채움
# 0은 아무런 의미가 없는 형태소라는 의미.
# 0이라서 학습도 안됨.

# 제일 긴 문장을 찾음
max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])

print(max)

# 길이가 max가 되도록 0으로 채워준다.
X_pad = pad_sequences(tokened_X, max)
print(X_pad)



#===================================================================================================
#%% 학습 데이터 저장.
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X_pad, onehot_Y, test_size=0.1)
print(Xtrain.shape, Ytrain.shape)
print(Xtest.shape, Ytest.shape)

np.save(f'./npdata/news_data_X_train_max_{max}_wordsize_{wordsize}', Xtrain)
np.save(f'./npdata/news_data_Y_train_max_{max}_wordsize_{wordsize}', Ytrain)
np.save(f'./npdata/news_data_X_test_max_{max}_wordsize_{wordsize}', Xtest)
np.save(f'./npdata/news_data_Y_test_max_{max}_wordsize_{wordsize}', Ytest)


