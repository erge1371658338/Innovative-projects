#%%    乌鸦网站post请求format中输入doi，使用浏览器为谷歌浏览器
import requests
from lxml import etree     ##爬虫，爬取内容
import re
url = "https://sci-hub.se/"

payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"request\"\r\n\r\n"+format("10.1016/0025-5408(76)90073-8 ")+"\r\n-----011000010111000001101001--"
headers = {
    'content-type': "multipart/form-data; boundary=---011000010111000001101001",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'cookie': "__ddg1=eBta35OBcKJuSyuQZzAJ; session=49ad08798c561be8e2db56b49c975a31; refresh=1624260971.2539; __ddgid=HwJTXTQEwecV3LKR; __ddgmark=Yxndk6IfPUctk17r; _ym_uid=1624260984450422206; _ym_d=1624260984; __ddg2=YfoGjNCBPzXVtma9; _ym_isad=2",
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': "?0",
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "none",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    'cache-control': "no-cache",
    ##'postman-token': "b46313b7-7c95-f246-1a12-67bb11b4d7c5"
    }

response = requests.request("POST", url, data=payload, headers=headers)

contents=response.content.decode("utf8")
html = etree.HTML(contents)  #此处生成了一个HTML格式的文件，无法直接打印
result = etree.tostring(html,encoding="utf8").decode("utf-8") #用于显示html文件，没有额外的作用

author_data=(html.xpath('//div[@id="citation"]/text()'))[0] #作者
author=(re.findall("\D+(?=[.])",author_data))[0]

year=(re.findall("['(']+\d+[')']",author_data))[0] #年份

doi=(html.xpath('//div[@id="citation"]/text()'))[1]    #DOI

title_data=(html.xpath('//div[@id="citation"]/*/text()'))[0] #文章标题
title=title_data

journal=(re.findall("[?<=.]+.*",title_data))[0] #期刊名字
#%%   百度学术进行爬取,获取百度学术的URL,使用谷歌浏览器，输入为文献的名字

url = "https://xueshu.baidu.com/s"

querystring = {"wd":title,"rsv_bp":"0","tn":"SE_baiduxueshu_c1gjeupa","rsv_spt":"3","ie":"utf-8","f":"3","rsv_sug2":"1","sc_f_para":"sc_tasktype%3D%7BfirstSimpleSearch%7D","rsp":"2"}
#修改上述参数为文献名字
payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"paperid\"\r\n\r\nc7f412ba629ed9b1e831b6673593ab00\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"site\"\r\n\r\nxueshu_se\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"hitarticle\"\r\n\r\n1\r\n-----011000010111000001101001--"
headers = {
    'content-type': "multipart/form-data; boundary=---011000010111000001101001",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'connection': "keep-alive",
    'cookie': "BIDUPSID=4DBD301333ADDD88594FCBEBF85E97EF; PSTM=1620200350; BAIDUID=4DBD301333ADDD883E7EBE3D5BC32D21FG=1; __yjs_duid=1_4485edf5ffcf5583a1e79031f1d28a491620312424006; BD_HOME=0; COOKIE_KEY_INDEX_BANNER=; Hm_lvt_43115ae30293b511088d3cbe41ec099c=1624339706; Hm_lvt_f28578486a5410f35e6fbd0da5361e5f=1624339706; BD_CK_SAM=1; antispam_key_id=45; antispam_site=ae_xueshu_paper; BDSFRCVID=YHKOJexroG384qTeFqQFo4OuxeKK0gOTDYLtOwXPsp3LGJLVgadsEG0PtOUBxFP-oxShogKK0eOTHk8F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRk8oIL2fIvDqTrP-trf5DCShUFsXxviB2Q-XPoO3K8WM-j2bfja0fKej-nthPQiWbRM2MbgylRM8P3y0bb2DUA1y4vpK-ob-2TxoUJ2BM5IJhQMqtnW0PkebPRiJPQ9QgbWVpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0HPonHjL-j5jP; BDSFRCVID_BFESS=YHKOJexroG384qTeFqQFo4OuxeKK0gOTDYLtOwXPsp3LGJLVgadsEG0PtOUBxFP-oxShogKK0eOTHk8F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tRk8oIL2fIvDqTrP-trf5DCShUFsXxviB2Q-XPoO3K8WM-j2bfja0fKej-nthPQiWbRM2MbgylRM8P3y0bb2DUA1y4vpK-ob-2TxoUJ2BM5IJhQMqtnW0PkebPRiJPQ9QgbWVpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0HPonHjL-j5jP; delPer=0; BDRCVFR[EiXQVvOKA3D]=mk3SLVN4HKm; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=01808k200l2l0480jn1gd3cp20q; H_PS_PSSID=; ab_sr=1.0.1_ZjAyMDJlM2M5YWY2ZTkwZDkyNDg5MGMzZGQ3YmRjMGQwNjg0NTBkMjY1Y2VlYzc5ZDY2MDEyM2E0OGI5NDBjM2VkNjBmOGQxNWMyOWQ3MmNiODkzYmZhMTM1ZjRmOTZiNzFjMDUxMWViMjkxMDQxMzlkNTI5NDllYzMyMjNlMzMwOWZjNTQ5YWU0ZGRiZWUxYmM5ZDEwZmI5NTdjY2JjYQ==; antispam_data=9408fc7da3a1d912a77bb5869ebcb62f370e80b1749a20f447d413ed419f2d448863203f60211a4de85287cd6a8277c14a748e844fca84caabb1e92633415933a2ff68ae10cdf04d7d7ec0d2f37e9b2df4c0532a918820f63cc2a3953fb84eb0; antispam_sign=ca2ab019; PSINO=1; BDRCVFR[w2jhEs_Zudc]=mk3SLVN4HKm; BDSVRTM=14; Hm_lpvt_43115ae30293b511088d3cbe41ec099c=1624357841; Hm_lpvt_f28578486a5410f35e6fbd0da5361e5f=1624357841",
    'host': "xueshu.baidu.com",
    'referer': "https//xueshu.baidu.com/?tn=SE_baiduxueshu_c1gjeupa&sc_as_para=&sc_from=",
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': "?0",
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "same-origin",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    'cache-control': "no-cache",
    #'postman-token': "4524317a-390b-f284-9762-15d2bcbc8d39"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
contents=response.content.decode("utf8")
html=etree.HTML(contents)
print(response.text)
url2=(html.xpath("//span[@class='detail_article_hint']/a/@href"))[0]  #后续连接
#%%  百度学术
url2="https://xueshu.baidu.com"+format(url2)
headers={
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
    }
response = requests.get(url2,headers=headers)   ##返回了一个对象
contents=response.content.decode("utf8")
html=etree.HTML(contents)
result=etree.tostring(html,encoding="utf8").decode("utf-8")
print(result)
url3=(html.xpath("//div[@id='content_leftrs']//div[@id='1']//h3//a/@href"))[0]
#%%  百度学术
url3="https:"+format(url3)
headers={
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
    }
response = requests.get(url3,headers=headers)   ##返回了一个对象
contents=response.content.decode("utf8")
html=etree.HTML(contents)
result=etree.tostring(html,encoding="utf8").decode("utf-8")
abstract=(html.xpath("//div[@class='abstract_wr']//p[@class='abstract']/text()"))[0]  #文章摘要，太多了显示不全
keyword=html.xpath("//div[@class='kw_wr']//p[@class='kw_main']//span/a/text()")   #文章关键词
for i in range(0,len(keyword)):
    print (keyword[i])
