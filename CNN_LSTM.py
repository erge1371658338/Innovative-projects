# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 15:01:49 2021

@author: 86182
"""
# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from chemdataextractor.nlp.tokenize import ChemWordTokenizer
from sklearn import model_selection
from sklearn import svm
from sklearn import metrics
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
import warnings
warnings.filterwarnings("ignore")   # 忽略掉预测没有标签1的警告
set(stopwords.words('english'))
"""
函数说明：简单分词
Parameters:
     filename:数据文件
Returns:
     list_word_split：分词后的数据集列表
     category_labels: 文本标签列表
""" 
def remove(text):
    remove_chars = '[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    return re.sub(remove_chars, '', text)

def word_split(filename):
    stop_words = set(stopwords.words('english')) # 停用词集合
    fig_words = ["Figure","igure","FIGURE","FIG","Fig","fig"]
    read_data = pd.read_excel(filename)
    list_word_split = []
    category_labels = []
    cwt = ChemWordTokenizer()
    for i in range(len(read_data)):
        row_data = read_data.iloc[i-1, 0]  # 读取单个漏洞描述文本
        list_row_data = list(cwt.tokenize(row_data))  # 对单个漏洞进行分词,化学分词
        #list_row_data = list(nltk.word_tokenize(row_data))  # 对单个漏洞进行分词，NLTK分词
        list_row_data = [remove(x) for x in list_row_data ]  # 去除列表中的标点符号
        list_row_data = [x for x in list_row_data if ((len(x)>3) & (x not in fig_words))]  # 去除列表中的空格字符
        list_row_data = [x for x in list_row_data if x not in stop_words]  # 去除列表中的停用词
        list_word_split.append(list_row_data)

        row_data_label = read_data.iloc[i-1, 1]  # 读取单个漏洞的类别标签
        category_labels.append(row_data_label)  # 将单个漏洞的类别标签加入列表
    return list_word_split, category_labels

#%%

if __name__ == '__main__':
    list_word_split, category_labels = word_split(r"C:\Users\86182\Desktop\all_data.xlsx")  # 获得每条文本的分词列表和标签列表
#%%
'''
created by Yang in 2020.11.1
'''
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
#读取数据集函数
def get_dataset(dataset_path):
    npzfile = pd.read_excel(dataset_path,header=None)
    return npzfile[0] , npzfile[1]

#计算最大文本长度
def get_maxlen(train_texts , test_texts):
    maxlen = 0
    for text in train_texts:
        text = re.findall(r'\b\w+\b' , text)
        if len(text) > maxlen:
            maxlen = len(text)
    for text in test_texts:
        text = re.findall(r'\b\w+\b' , text)
        if len(text) > maxlen:
            maxlen = len(text)
    return maxlen


#文本转换为向量并填充
def texts2vec_padding(train_texts , test_texts ,maxlen):
    tokenizer = Tokenizer(num_words=10604)
    tokenizer.fit_on_texts(train_texts)
    texts_train = tokenizer.texts_to_sequences(train_texts)
    texts_test = tokenizer.texts_to_sequences(test_texts)
    #填充
    texts_train = pad_sequences(texts_train , padding='post' , maxlen=maxlen)
    texts_test = pad_sequences(texts_test , padding='post' , maxlen=maxlen)
    vocab_size = len(tokenizer.word_index)+1
    
    return texts_train , texts_test , vocab_size




train_dataset_path = r"C:\Users\86182\Desktop\train_dataset.xlsx"
test_dataset_path = r"C:\Users\86182\Desktop\text_dataset.xlsx"
#训练集文本与标签
train_x , train_y = get_dataset(train_dataset_path)
test_x , test_y = get_dataset(test_dataset_path)
#获取最大文本长度
maxlen = get_maxlen(train_x , test_x)
train_x , test_x  , vocab_size = texts2vec_padding(train_x , test_x , maxlen)
np.savez(r'C:\Users\86182\Desktop\train_data_vec' , x=train_x , y=train_y)
np.savez(r'C:\Users\86182\Desktop\test_data_vec' , x=test_x , y=test_y)

#%%
'''
    训练模型
'''
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import layers , Sequential , datasets , optimizers,losses 
from tensorflow.keras.layers import LSTM 
import matplotlib.pyplot as plt
import random
#读取数据集函数
def get_dataset(dataset_path):
    npzfile = np.load(dataset_path)
    return npzfile['x'] , npzfile['y']
#画图函数
def draw(epoch_sumloss , epoch_acc):
    x=[i for i in range(len(epoch_sumloss))]
    #左纵坐标
    fig , ax1 = plt.subplots()
    color = 'red'
    ax1.set_xlabel('epoch')
    ax1.set_ylabel('loss' , color=color)
    ax1.plot(x , epoch_sumloss , color=color)
    ax1.tick_params(axis='y', labelcolor= color)

    ax2=ax1.twinx()
    color1='blue'
    ax2.set_ylabel('acc',color=color1)
    ax2.plot(x , epoch_acc , color=color1)
    ax2.tick_params(axis='y' , labelcolor=color1)

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    #读取路径
    train_path = r'C:\Users\86182\Desktop\train_data_vec.npz'
    test_path = r'C:\Users\86182\Desktop\test_data_vec.npz'
    #读取训练集与测试集
    train_x , train_y = get_dataset(train_path)
    test_x , test_y = get_dataset(test_path)
   
    #打乱数据集
    seed = 1234
    random.seed(seed)
    random.shuffle(train_x )
    random.seed(seed)
    random.shuffle(train_y)

    seed = 2143
    random.seed(seed)
    random.shuffle(test_x )
    random.seed(seed)
    random.shuffle(test_y)
    
    
    train_y = tf.one_hot(train_y , depth = 5)
    test_y = tf.one_hot(test_y , depth=5)
    train_y=tf.Session().run(train_y)       #转换数据格式，不转存在报错
    test_y=tf.Session().run(test_y)
    
    #数据集词袋大小
    vocab_size  =10604
    #最长文本
    max_textlen = 123
    #词向量大小
    embedding_dim  =50
    #创建文本分类基础模型
    basic_model = Sequential([
    layers.Embedding(input_dim=vocab_size , 
                    output_dim=embedding_dim,
                    input_length=max_textlen),
    layers.Flatten(),
    # layers.BatchNormalization(),
    layers.Dense(50,activation='relu'),
    # layers.BatchNormalization(),
    layers.Dense(25,activation='relu')  ,
    # layers.BatchNormalization() ,
    layers.Dense(5,activation='sigmoid') ,
    ])

    #lstm模型
    lstm_model = Sequential([
        layers.Embedding(input_dim=vocab_size,
                                    output_dim=embedding_dim,
                                    input_length=max_textlen),
        LSTM(128 , return_sequences=False),
        layers.BatchNormalization() ,
        # layers.Dense(256 ,activation='relu'),
        # layers.Dense(128 ,activation='relu'),
        layers.Dense(16 ,activation='relu'),
        # layers.BatchNormalization(),
        layers.Dense(5,activation='relu')
    ])

    #CNN模型
    CNN_model = Sequential([
        layers.Embedding(input_dim=vocab_size,
                                    output_dim=embedding_dim,
                                    input_length=max_textlen),
        layers.Conv1D(512 ,5, activation='relu'),
        layers.GlobalMaxPooling1D(),
        layers.Dense(64 , activation='relu'),
        layers.BatchNormalization(),
        layers.Dense(32 , activation='relu'),
        layers.Dense(5 , activation='relu')
    ])
#%%  CNN模型
    
    CNN_model.compile(optimizer='adam',loss='binary_crossentropy' , metrics=['accuracy'])
    CNN_model.summary()
    

    history = CNN_model.fit(train_x , train_y , epochs=100 , verbose=False , validation_data=(test_x , test_y),batch_size=118)
    #history = CNN_model.fit(train_x , train_y , epochs=100 ,steps_per_epoch=1)
    loss  , acc =CNN_model.evaluate(train_x , train_y  , verbose=False)
    loss  , acc =CNN_model.evaluate(test_x , test_y  , verbose=False)
    draw(history.history['loss'] , history.history['acc'])

#%%  LSTM模型
    lstm_model.compile(optimizer='adam',loss='binary_crossentropy' , metrics=['accuracy'])
    lstm_model.summary()

    history = lstm_model.fit(train_x , train_y , epochs=100 , verbose=False , validation_data=(test_x , test_y),batch_size=118)
    loss  , acc =lstm_model.evaluate(train_x , train_y  , verbose=False)
    loss  , acc =lstm_model.evaluate(test_x , test_y  , verbose=False)
    draw(history.history['loss'] , history.history['acc'])
    
#%%  basic_model    
    basic_model.compile(optimizer='adam',loss='binary_crossentropy' , metrics=['accuracy'])
    basic_model.summary()

    history = basic_model.fit(train_x , train_y , epochs=100 , verbose=False , validation_data=(test_x , test_y),batch_size=118)
    loss  , acc =basic_model.evaluate(train_x , train_y  , verbose=False)
    loss  , acc =basic_model.evaluate(test_x , test_y  , verbose=False)
    draw(history.history['loss'] , history.history['acc'])