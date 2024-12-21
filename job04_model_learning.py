#===================================================================================================
#%% 필요 모듈 임포트
import numpy as np
import matplotlib.pyplot as plt
import glob

from keras._tf_keras.keras.models import *
from keras._tf_keras.keras.layers import *

#===================================================================================================
#%% 학습데이터 불러옴

# 데이터 경로
npdata_dir = './npdata/'

# 와일드카드를 사용해 파일 경로 찾기
X_train_path = glob.glob(npdata_dir + '*X_train*.npy')[0]
X_test_path = glob.glob(npdata_dir + '*X_test*.npy')[0]
Y_train_path = glob.glob(npdata_dir + '*Y_train*.npy')[0]
Y_test_path = glob.glob(npdata_dir + '*Y_test*.npy')[0]

# 파일 로드
X_train = np.load(X_train_path)
X_test = np.load(X_test_path)
Y_train = np.load(Y_train_path)
Y_test = np.load(Y_test_path)

print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)



#===================================================================================================
#%% 모델 생성
model = Sequential()

model.add(Embedding(6607, 300))


model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=1))

model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))

model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))

model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.3))

model.add(Flatten())

model.add(Dense(128,activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(6, activation='softmax'))

#model.build(input_shape=(None, 16))
#print(model.summary())



#===================================================================================================
#%% 모델 학습
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

fit_hist = model.fit(X_train,
                     Y_train,
                     batch_size=128,
                     epochs=10,
                     validation_data=(X_test, Y_test))

print(model.summary())

score = model.evaluate(X_test, Y_test, verbose=0)

print('Final test set accuracy', score[1])

plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.legend()
plt.show()



#%% 모델 저장.
model_dir = './models/'
model_accuracy = fit_hist.history['val_accuracy'][-1]
model_name = f'news_category_classfication_model_{model_accuracy}.h5'

model.save(model_dir + model_name)

