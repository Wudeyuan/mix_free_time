import itchat
import requests
import re
import time
import random

# 抓取网页上回复内容
def getHtmlText(url): 
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

# 编辑回复内容和时间
@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing', 'Picture'])
def text_reply(msg):
    if msg['FromUserName'] in UserName:
        key='0b986b0f69104275a244e9cddac224e1' # 可以自己去http://www.tuling123.com申请
        url = "http://www.tuling123.com/openapi/api?key="+key+"&info="
        url = url + str(msg['Text'])
        html = getHtmlText(url)
        message = re.findall(r'\"text\"\:\".*?\"', html) # 回复的内容
        reply = eval(message[0].split(':')[1])
        robots = ['.r','.wdy'] #供随机选一个作为回复的结尾
        reply = reply + random.choice(robots)
        time.sleep(1) # 等1秒再回复
        return reply

# 设置回复对象
if __name__ == '__main__':
    itchat.auto_login() # 会弹出微信网页登录的二维码
    myUserName = itchat.get_friends(update=True) # 微信好友名list
    le = len(myUserName)
    k = k0 = 0
    for i in range(0, le):
        if myUserName[i]['RemarkName'] == 'WLL': # 备注是WLL的好友
            k0 = i
    UserName = [itchat.get_friends(update=True)[k0]["UserName"],
                itchat.get_friends(update=True)[k]["UserName"]] # 0表示自己，可以跟自己聊聊
    itchat.run()