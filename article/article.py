# -*-coding:utf-8-*-    #编码，防乱码
#代码仅供学习，不能用于商业等违法用途，否则后果由使用者承担

#from lxml import etree #xpath分析image's url使用，
#获取cv号,以cv号形式保存图片

import requests     #模拟hppts请求
import re           #正则表达式，用于提取image、cv号
import os           #提供文件读写操作
import time         #提供延时函数
import UserAgent

def findCvNumber(list,mid): #根据mid查找cvhao
    page = 1    #预定义page，即从第1页开始查找
    while (1):
        localurl = 'https://api.bilibili.com/x/space/article?mid=' + mid + '&pn=' + str(page)   #合成具有cv号信息的网页A
        headers = UserAgent.get_headers()  # 随机获取一个headers
        res = requests.get(url=localurl, headers=headers)    #请求A
        html = res.text #转换A为文本
        length = len(res.content)   #计算A的文本的长度
        if(length<100): #小于100算作无新的cv号了
            break
        #print('len=' + str(length))    #输出A的文本的长度
        rst = re.findall('{"id":(.*?),".*?":{".*?,".*?",".*?"', html)   #更具正则表达式提取具有cv号的文本
        # list.append(re.findall('[0-9]{7}', str(rst)))   #提取cv号 0后面继续添加
        # rstforprint = re.findall('[0-9]{7}', str(rst))  #用于打印的cv号列表
        print('page=' + str(page))  #打印这是第几页
        # print(rstforprint,"No use")  #打印cv号列表
        print(rst)

        #每个cv号，调用 cv下载img函数
        for i in range(len(rst[0])):
            CvGetImg(rst[i],PATH)
            time.sleep(1)
        page+=1
        time.sleep(0.05)   #休眠1秒
    return list #返回二维cv号列表

def CvGetImg(cv,path):#输入cv号 创建cv号文件夹，其下 下载图片
    headers = UserAgent.get_headers()  # 随机获取一个headers
    html = requests.get(url='https://www.bilibili.com/read/cv'+str(cv), headers=headers)
    html = html.text
    #解析html文本
    title=re.findall('<meta name="name" content="(.*?)">',html)
    print(title)
    if(len(title)==0):
        return
    Imgs=re.findall('<img data-src="(//i0.*?)" .*?>',html,re.S)
    print(Imgs)
    #判断文件夹,存在就跳过这次函数
    if os.path.exists(path+str(title[0])):
        return
    if not os.path.exists(path+str(title[0])):
        os.mkdir(path+str(title[0]))
    for j in range(len(Imgs)):
        pic = requests.get('https:' + Imgs[j], timeout=10)
        fp = open(path+str(title[0])+'/'+ str(j) + '.jpg', 'wb')
        fp.write(pic.content)
        fp.close()



if __name__ == '__main__':
    cv_list =[]   #初始化一个cv_list
    MID='00000000'#修改MID号
    PATH="P:\images/"#修改根目录
    findCvNumber(cv_list,MID)
    print(cv_list)


