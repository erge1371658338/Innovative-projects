# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import model_selection
from sklearn import svm
from sklearn import metrics
import numpy
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
    for i in range(len(read_data)):
        row_data = read_data.iloc[i-1, 0]  # 读取单个漏洞描述文本
        list_row_data = list(nltk.word_tokenize(row_data))  # 对单个漏洞进行分词
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
for i in range(0,len(category_labels)):
    if (i>=len(category_labels)):
        break
    if (type(category_labels[i])!=int):
        category_labels.pop(i)
        list_word_split.pop(i)
        continue
    if (category_labels[i]>3):
        category_labels.pop(i)
        list_word_split.pop(i)
        continue
    print(list_word_split)
    print(category_labels)
    print('分词成功')
split_corpus = []
for c in range(len(list_word_split)):
    s = "".join(list_word_split[c])
    split_corpus.append(s)      # 将多个分词组成一个字符串
print(split_corpus)


# 利用词袋模型提取特征向量
cv = CountVectorizer()
cv_fit = cv.fit_transform(split_corpus)
print(cv.get_feature_names())       # 显示特征列表
print(cv_fit.toarray())             # 显示特征向量


# 利用特征向量训练分类
X = cv_fit.toarray()                            # X：数据数组
y = numpy.zeros(len(category_labels), dtype=int, order='C')     # 
for i in range(0,len(category_labels)):
    y[i] = category_labels[i]-1

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.4, random_state=0)

svm = svm.SVC(kernel='rbf', gamma=0.7)  # 使用rbf核函数，参数设置为：gamma为0.7，一个问题：参数C
svm.fit(X_train, y_train)

# svm分类性能
y_pred_svm = svm.predict(X_test)

print("SVM 准确率为:\n", svm.score(X_test, y_test))
print("SVM report:\n", metrics.classification_report(y_test, y_pred_svm))
print("SVM 混淆矩阵:\n", metrics.confusion_matrix(y_test, y_pred_svm))
