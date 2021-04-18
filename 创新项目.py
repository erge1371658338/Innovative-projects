#!/usr/bin/env python
# coding: utf-8

# In[4]:


import fitz  
import re
import os
import sys
import xlwings as xw
from PIL import Image

j = 1
height=0

def get_image(path, pic_path,pdfname):
    doc = fitz.open(path)  #打开PDF
    leng = doc._getXrefLength()  #统计长度
    imgcount = 0
    checkXO = r"/Type(?= */XObject)"#使用了正则表达式
    checkIM = r"/Subtype(?= */Image)"
    print("文件名:{}, 页数: {}, 对象: {}".format(path, len(doc), leng - 1))   #使用格式化函数format
    for i in range(1, leng):
        text = doc._getXrefString(i)   
    
        isXObject = re.search(checkXO, text)    # 查看是否是对象，返回BOOL值
        isImage = re.search(checkIM, text)      # 查看是否是图片,返回BOOL值
    
        if not isXObject or not isImage: # 如果不是对象也不是图片，则continue
            continue
        imgcount +=1   
        try:
            pix = fitz.Pixmap(doc, i)               #提取图片
       
            new_name = pdfname.replace('\\', '_') + "_height{}.png".format(pix.height)
            new_name = new_name.replace(':', '')
            if pix.n < 5:                           # 如果pix.n<5,可以直接存为PNG
                pix.writePNG(os.path.join(pic_path, new_name))  
                print(pix.height)
            pix = None
        except RuntimeError:
            print ("fail to extract image")
            continue
 

def get_excel(p_path,wb):
    
    sht= wb.sheets['Sheet1']
    global j
    
    
    pic_path =p_path    #从文件夹中获取图片地址
    filenames=os.listdir(pic_path)
    for filename in filenames:
    
        
        p=os.path.abspath(pic_path)
        filename1 = os.listdir(p)
        
        path = pic_path+"/"+filename
        try:
            plt = Image.open(path)
            w, h = plt.size
            x_s = 100                    #设定图片的大小
            y_s = h * x_s / w       
    
            sht.pictures.add(path,name=('picture'+format(j)),update = True ,left=sht.range('A'+format(j)).left, top=sht.range('A'+format(j)).top,width=x_s, height=y_s)
            sht.range('B'+format(j)).value="属于"+filename

            height = re.findall( r'(?=height)\w+',filename,re.M)
            height = re.findall( r'\d+',str(height),re.M)
            sht.range('C'+format(j)).value=height
            
            sht.range('A'+format(j)).column_width=x_s/5
            sht.range('A'+format(j)).row_height=y_s+30
            j += 1
        except OSError:
            print ("fail to Add Excel")
            continue
    
        
if __name__=='__main__':                       
    paths=[r"C:\Users\86182\Desktop\12"]
    path1=r"C:\Users\86182"
    
    app=xw.App(visible=True,add_book=False)      #设置Excel表格
    wb=app.books.add()
    wb.save(r'C:\Users\86182\Desktop\test3.xlsx')
    sht= wb.sheets['Sheet1']
    
    
    for path in paths:
        p=os.path.abspath(path)
        filenames=os.listdir(p)
        i = 0
        for filename in filenames:
            im_path=p+'\\'+filename
            pic_path=filename
            i +=1
            print (pic_path)                #PDF文件的名字
            os.mkdir(pic_path)
            get_image(im_path, pic_path,filename)
            sht.range('A'+format(j)).value = pic_path
            j+=1
            get_excel(path1+'/'+pic_path,wb)      #传输绝对路径，以及EXCEL表格
            j+=5
            
    wb.save()   
    wb.close()


# In[17]:



#用于测试

import fitz  
import re
import os
import sys
import xlwings as xw
from PIL import Image

j = 1


def get_image(path, pic_path,pdfname):
    doc = fitz.open(path)  #打开PDF
    leng = doc._getXrefLength()  #统计长度
    imgcount = 0
    checkXO = r"/Type(?= */XObject)"#使用了正则表达式
    checkIM = r"/Subtype(?= */Image)"
    ckeckTI = r"\bFigure\s.+\s+.+\s"
    print("文件名:{}, 页数: {}, 对象: {}".format(path, len(doc), leng - 1))   #使用格式化函数format
    
    app=xw.App(visible=True,add_book=False)      #设置Excel表格
    wb=app.books.add()
    wb.save(r'C:\Users\86182\Desktop\test5.xlsx')
    sht= wb.sheets['Sheet1']
    k=1
    for i in range(1, leng):
        text = doc._getXrefString(i)   
        isXObject = re.search(checkXO, text)    # 查看是否是对象，返回BOOL值
        isImage = re.search(checkIM, text)      # 查看是否是图片,返回BOOL值
        
    
        if not isXObject or not isImage: # 如果不是对象也不是图片，则continue
            continue
        imgcount +=1   
        try:
            pix = fitz.Pixmap(doc,i)               #提取图片
            print (type(pix),pix.type)
            
            title = re.findall( r'\bPixmap.+', pix,re.M)
            sht.range('A'+format(k)).value=pix
            k+=1
            new_name = pdfname.replace('\\', '_') + "_img{}.png".format(imgcount)
            new_name = new_name.replace(':', '')
            if pix.n<5:                           # 如果pix.n<5,可以直接存为PNG
                pix.writePNG(os.path.join(pic_path, new_name))  
            pix = None
        except RuntimeError:
            print ("fail to extract image")
            continue
 


def get_excel(p_path,wb):
    
    sht= wb.sheets['Sheet1']
    global j
    
    
    pic_path =p_path    #从文件夹中获取图片地址
    filenames=os.listdir(pic_path)
    for filename in filenames:
    
        p=os.path.abspath(pic_path)
        filename1 = os.listdir(p)
    
        
        print (pic_path+"/"+filename)
        path = pic_path+"/"+filename
        plt = Image.open(path)
    
        w, h = plt.size
        x_s = 100                    #设定图片的大小
        y_s = h * x_s / w       
    
        sht.pictures.add(path,name=('picture'+format(j)),update = True ,left=sht.range('A'+format(j)).left, top=sht.range('A'+format(j)).top,width=x_s, height=y_s)
        sht.range('B'+format(j)).value="属于"+filename
        height = re.findall( r'(?=height)\w+',filename,re.M)
        height = re.findall( r'\d+',str(height),re.M)
        sht.range('C'+format(j)).value=height
        
        sht.range('A'+format(j)).column_width=x_s/5
        sht.range('A'+format(j)).row_height=y_s+30
         
        j += 1
    
        
if __name__=='__main__':                       
    paths=[r"C:\Users\86182\Desktop\12"]
    path1=r"C:\Users\86182"
    
    app=xw.App(visible=True,add_book=False)      #设置Excel表格
    wb=app.books.add()
    wb.save(r'C:\Users\86182\Desktop\test3.xlsx')
    sht= wb.sheets['Sheet1']
    
    
    for path in paths:
        p=os.path.abspath(path)
        filenames=os.listdir(p)
        i = 0
        for filename in filenames:
            im_path=p+'\\'+filename
            pic_path=filename
            i +=1
            print (pic_path)                #PDF文件的名字
            print ("||||||||||||",im_path,"||||||||||",filename)
            os.mkdir(pic_path)
            get_image(im_path, pic_path,filename)
            sht.range('A'+format(j)).value = pic_path
            j+=1
            
           
            
            get_excel(path1+'/'+pic_path,wb)      #传输绝对路径，以及EXCEL表格
            j+=5
            
    wb.save()   
    wb.close()


# In[7]:


import fitz  
import re
import os
import sys
import xlwings as xw
from PIL import Image
#   用于生成图片对应文本信息的excel
path = r"C:\Users\86182\Desktop\262812-yatskin2012.pdf"
doc = fitz.open(path)  #打开PDF
app=xw.App(visible=True,add_book=False)      #设置Excel表格
wb=app.books.add()
wb.save(r'C:\Users\86182\Desktop\test4.xlsx')
sht= wb.sheets['Sheet1']
k = 2
k1=k
for page in doc:
        # 在页面上列出图像列表
        imageList = page.getImageList()
        #print(imageList)
        # 按页码提取页面文本
        text = page.getText()
        #print(text)
        
        dl = page.getDisplayList() 
        tp = dl.getTextPage() 
        txt  = tp.extractText()

        title = re.findall( r'\bFigure\s.+\s+.+', txt,re.M)
        Doi = re.findall(r'(?=doi).+',txt,re.M|re.I)
        imformation = re.findall( r'(?<=\.\s).+\s.+\s.+(?=Fig\.).{7}', txt,re.M)
        if imformation!=[]:
            sht.range("K"+format(k)).value=imformation
        if Doi!=[]:
            Doi1=Doi
        if imageList!=[]:
            sht.range('A'+format(k)).value=imageList
            print (imageList)
        if title!=[]:
            sht.range('j'+format(k)).value=title
            print (title)
        k+=1
sht.range('A'+format(k1-1)).value=Doi1
wb.save()   
wb.close()


# In[8]:


#用于将图片excel和图片信息excel合并起来
import pandas as pd
import numpy as np
import xlwings as xw
app=xw.App(visible=True,add_book=False)
app.display_alerts=False   
app.screen_updating=False  
text3=pd.read_excel(r"C:\Users\86182\Desktop\test3.xlsx")
text4=pd.read_excel(r"C:\Users\86182\Desktop\test4.xlsx",index_col=1)
wb=app.books.open(r"C:\Users\86182\Desktop\test3.xlsx")
sheet1 = wb.sheets["Sheet1"]
sheet1.range("B"+format(1)).value=list(text4)[0]
for i in range(0,text4.shape[0]): 
    for j in range(0,text3.shape[0]): #对于每一行
        if(text4.iloc[i,2]==text3.iloc[j,2]):
            if (text4.iloc[i,8]!='NaN'):
                sheet1.range('D'+format(j+2)).value=text4.iloc[i,8]
                print(text4.iloc[i,8])
                print('D'+format(j+2))
            break
wb.save()
wb.close()
app.quit()


# In[ ]:


#往下用于测试如何提取人名（利用正则表达式）


# In[12]:


for page in doc:
        # 在页面上列出图像列表
        imageList = page.getImageList()
        #print(imageList)
        # 按页码提取页面文本
        text = page.getText()
        #print(text)
        dl = page.getDisplayList()
        tp = dl.getTextPage() 
        txt  = tp.extractText()
        print(txt)
        imformation = re.findall( r'(?<=\.\s).+\s.+\s.+(?=Fig\.).{7}', txt,re.M)
        if imformation!=[]:
            imformation1=imformation
            
        


# In[11]:


import re
a= "Dq. qqWs. Qaaa. There is no game(Fig. 2). "
imformation = re.findall( r'(?<=\.\s)(?:[A-Z])(?:[^A-Z])+(?=Fig).{7}', a,re.M)
print(imformation)


# In[15]:


path = r"C:\Users\86182\Desktop\193217-Kamali-2015-Pressure-induced-phase-transformati.pdf"
doc = fitz.open(path)  #打开PDF


# In[14]:


for page in doc:
        # 在页面上列出图像列表
        imageList = page.getImageList()
        #print(imageList)
        # 按页码提取页面文本
        text = page.getText()
        #print(text)
        dl = page.getDisplayList()
        tp = dl.getTextPage() 
        txt  = tp.extractText()
        print(txt)
        imformation = re.findall( r'(?<=\.\s).+\s.+\s.+(?=Fig\.).{7}', txt,re.M)
        if imformation!=[]:
            imformation1=imformation
            


# In[16]:


for page in doc:
        # 在页面上列出图像列表
        imageList = page.getImageList()
        #print(imageList)
        # 按页码提取页面文本
        text = page.getText()
        #print(text)
        dl = page.getDisplayList()
        tp = dl.getTextPage() 
        txt  = tp.extractText()
        print(txt)
        imformation = re.findall( r'(?<=\.\s).+\s.+\s.+(?=Fig\.).{7}', txt,re.M)
        if imformation!=[]:
            imformation1=imformation


# In[ ]:




