#===================================================================================================
#%% 필요 모듈 import
import pandas as pd
import numpy as np

from keras._tf_keras.keras.utils import to_categorical
from keras._tf_keras.keras.preprocessing.sequence import pad_sequences
from keras._tf_keras.keras.models import load_model

import pickle
from konlpy.tag import Okt



#===================================================================================================
#%% CSV파일 불러오기

# csv를 데이터 프레임으로 읽음.
csv_dir = '../crawling_data/'
csv_name = 'NaverNews_Headlne_Data_241223.csv'
df = pd.read_csv(csv_dir + csv_name)

# CSV파일을 읽어서 확인.
print(df.head())
print(df.info())
print(df.category.value_counts())

# 열을 나눔.
X = df['titles']
Y = df['category']



#===================================================================================================
# 카테고리 열 전처리(원 핫 인코딩)
#===================================================================================================
# 저장한 더미화 데이터를 불러와서 더미화.
with open('../models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)

label = encoder.classes_
print(label)

labeled_Y = encoder.transform(Y)
onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)



#===================================================================================================
# 제목 열 전처리
#===================================================================================================
#%% 제목의 형태소 분리
print(X[0])
okt = Okt()

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)

print(X)



#===================================================================================================
#%% stopwords 제거

# stopwords 목록을 CSV에서 불러옴.
stopwords_dir = '../stopwords/stopwords.csv'
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
#%% 제목 문장 라벨링.
# 이전에 모델을 학습할 때 사용했던 것으로 동일하게 해야됨.
# 만약 새로 크롤링한 데이터에 없던 형태소가 있다면 0으로 바꿔줘야 한다.
with open('../models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(X)

# 만약 새로 크롤링한 데이터의 문장길이가 학습할 때 보다 많을경우 자른다.
for i in range(len(tokened_X)):
    if len(tokened_X[i]) > 18:
        tokened_X[i] = tokened_X[i][:18]

X_pad = pad_sequences(tokened_X, 18)

print(tokened_X[:5])



#===================================================================================================
#%% 모델을 불러와서 새로 크롤링한 데이터를 분류 시켜봄.
model = load_model('../models/news_category_classfication_model_0.7324766516685486.h5')
preds = model.predict(X_pad)

predicts = []

for pred in preds:
    most = label[np.argmax(pred)]
    predicts.append(most)

df['predict'] = predicts

print(df.head(30))