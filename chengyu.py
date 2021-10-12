#coding: utf-8
'''
readme
功能：从百度获取所有成语，并对比本地成语库，从而去重筛选出新的成语词汇。

1.从百度获取成语API， 搜索”成语“关键字，百度通过小程序返回成语列表，每页30个成语，大致约26页。通过浏览器开发者工具，查找到成语列表API。注意此API 最后有 ”jQuery110206634179206242571_1634004428665&_=1634004428735“，建议去除。
2.解析并提取成语
3.存储成语到本地文件，等待对比
4.对比去重，挑出没有的成语

'''

import requests
from requests.api import request
import json
import os
import re


headers={'Cookie': 'BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ab_sr=1.0.1_ODhiZmNlZDY0YTA0MTBkYjhiNjE2MmQyYTAwYzc0OTAyYTg0MWMzYzk0ZWY4N2U5YjIyYzZiZmVjMWVlNTZmODMyZjI5OTE5ZjAyNDI5YWZkMjIyMmJkYzIyYTJlYWM4YjNhMzg2ZmNjNWMxM2E3YmIwNzI1YjVlZTgxZDA0NGUyODE3MjFlOTE0MGU5NGI4OGY5NTUzMDA2ZmNkYzY1ZjFlOTZjYWUzZTczYzc5Y2ExNDAxMjY1ZjVmYmI1ZTEz; BA_HECTOR=a1a581a10k2h840gf61gm9rfb0r; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; H_PS_PSSID=34653_34441_34530_34067_31660_34655_34712_34599_34584_34517_34707_34106_34806_34813_26350_34793_34677; PSINO=3; delPer=0; BDSFRCVID=O1tOJeC62lN-w17HDtmDe7F-SeKfg_7TH6bH1z24lxiDOuj92UVDEG0PMU8g0KuMsB3LogKKKgOTHICF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=JbIJVIP-tIvbfP0kMnoHMtK_5p_X5-RLf2b2_p7F54nKDp0Reh78jfkeKHJ-K6blHG7-ahvxfCQxsMT4QfcAyj88Ka7hqUCLQDviXCbN3KJmfMAl-xTIQKuJjxrz2-biW23M2MbdWlOP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe6thj5vbDG0s5JtXKD600PK8Kb7VbPOGyfnkbJkXhPteqpvBJmbpXfnR5C3PKfONyURmejK7QbrH0xRfyNReQIO13hcdSR3o2jOpQT8r5bPD5f6G3Pj3_JTuab3vOpvTXpO1yftzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-Ftqj-tJn-OoDtQb-3bKRvG-trt-J-0qxby26nwa259aJ5y-J7nhInyM6o13RIR3x_f0Drg5m3ibIIKQpbZql5EWxu2bJObbG7wel5MW5KJKl0MLPbrhJo8Lx8VM5KtWxnMBMni52OnapTn3fAKftnOM46JehL3346-35543bRTLnLy5KJYMDFRDTuaj6bbjNRHK430-DT2LTrb2R6DHjrm-tnD-tRH-UnLq5Ov0mOZ0l8KtJRFKt0ljU7U5-uibHJlelJ-WKcMMK3mWIQDOKjuD6OS2-FvXpoBq6jPQen4KKJxBxKWeIJo5fc5L6tThUJiBMnMBan7alOIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbC8RejL-jTvWep5-KPcH5C7JstOVaRoHK4bphP5HhICShUFsW5oJB2Q-5KL-apuVfID6yMOMhf08jPDLQ-Qi5Dvd_MbdJJo1htF4j-vWMf0g5fC8JqQp3gTxoUJzQCnJhhvGXJbIDUAebPRiB-b9QgbA5hQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0M5DK0HPonHj-BDTOX3f; __yjs_duid=1_54997096719af6b5afd7161567626bfc1633684596433; BDUSS=URVSVI1ZGdEVG11TzZtVkRUNThXcHN6eVNTbW42STFqa1hBT2JKeTVlSnJHWFZoSVFBQUFBJCQAAAAAAAAAAAEAAAANlSs3087Lv7rsuuy78Lvwuf4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGuMTWFrjE1hT; BAIDUID=C50163CD850E2144FC4BA49222246371:FG=1; BIDUPSID=C50163CD850E2144D4E54CBE092F6338; PSTM=1632288024',
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Host': 'sp1.baidu.com',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
'Accept-Language': 'zh-cn',
'Referer': 'https://www.baidu.com/s?wd=%E6%88%90%E8%AF%AD&rsv_spt=1&rsv_iqid=0xdea3bf65002f3a41&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=ib&rsv_sug3=8&rsv_sug1=2&rsv_sug7=100',
'Connection': 'keep-alive'}


#逐页遍历
def page(allpage):
    allpage=allpage
    # print(allpage)
    #页面遍历，可以使用从range 从X页到最大页面数
    for i in range(1,allpage):
         get_chengyu(i,headers)
        

#去百度获取成语
def get_chengyu(page,headers):
    #请求URL   参数需要使用format 格式化
    page=page*30
    # 页面要乘以30
    get_response = requests.get('https://sp1.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6848&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=%E6%88%90%E8%AF%AD&sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={pageno}&rn=30'.format(pageno=page), headers=headers)    
    chengyulist=get_response.json()["data"][0]['disp_data']  
    # 提取成语   
    print(page)
    for i in chengyulist:
        #  print(i['ename'])
         save_txt(i['ename'],"baiduchengyu.txt")
        #  print(page)

    #  print(len(chengyulist))   
# 存入txt   
def save(i):
    fo = open("baiduchengyu.txt", "a+")
    fo.write(i+'\n')
    fo.close()

def save_txt(i,url):
    fo = open(url, "a+")
    fo.write(i+'\n')
    fo.close()

#读取txt老成语库
def read_text(url):
    s = []
    f = open(url,'r') 
    for lines in f:
        ls = lines.strip(' ').replace(' ','').replace('、','/').replace('?','').split('/')
        
        for i in ls:
            i=re.sub(r'[0-9]+', '', i).replace(".",'')
            
            s.append(i)
    f.close()
    return s
    # print(s)

# 比较并提取除非重复发成语
def compare():
    huhu=read_text('foo.txt')
    baidu=read_text('baiduchengyu.txt')
    # print(huhu[0])
    # print(baidu[0])
    huhu = [current_name.lower() for current_name in huhu]
    baidu = [new_chengyu.lower() for new_chengyu in baidu]
    for new_chengyu in baidu:
        if new_chengyu not in huhu:           
            print(new_chengyu)
            save_txt(new_chengyu,"new.txt")        
        else:
            print(new_chengyu)
            save_txt(new_chengyu,"chongfu.txt")
        #     print(new_user + " 用户名可以使用")

if __name__=='__main__':
    # get_chengyu(headers)
    # page(27)
    # 从百度获取所有成语
    # read_text('foo.txt')
    # 读取老成语库
    compare()
    #  比较分析去重



