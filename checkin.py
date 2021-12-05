import time
import requests
import os

def getToken():
    CORPID = os.environ["CORPID"]
    CORPSECRET = os.environ["CORPSECRET"]
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid='+CORPID+'&corpsecret='+CORPSECRET
    r = requests.get(url)

    print(getDataAndTimeString() + ' got Token result:')
    # 查看响应结果
    print(r.json())
    
    TOKEN = r.json()['access_token']
    return TOKEN

#普通文本消息发送
def send(info):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+ getToken()
    # 注意这里必须以json字符串构造数据
    # xxx,@all
    data = '''
    {
        "touser" : "@all",
        "msgtype" : "text",
        "agentid" : 1000003,
        "text" : {
              "content" : \"%s\"
         },
         "safe":0
    }    
    ''' % info

    print(getDataAndTimeString() + ' HTTP post \nurl : ' + url + '\n' + data + '\n')

    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=data.encode(), headers=headers)
    print(r.json())

def sendByCard(title,content,jumpUrl,coverUrl):

    data = '''
    {
        "touser" : "@all",
        "msgtype" : "news",
        "agentid" : 1000003,
        "news" : {
            "articles" : [
                {
                    "title" : "%s",
                    "description" : "%s",
                    "url" : "%s",
                    "picurl" : "%s", 
                }
            ]
        },
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    ''' % (title, content ,jumpUrl,coverUrl)
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+ getToken()

    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=data.encode(), headers=headers)
    print(r.json())



def getDataAndTimeString():
    info = time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime(time.time()))
    return info

def getJustTimeString():
    # info = '现在时间 ' + time.strftime('%H:%M:%S', time.localtime(time.time()))
    info = time.strftime('%H:%M:%S', time.localtime(time.time()))
    return info

# 锻炼提醒
def exerciseTimeUp():
    info = '运动时间到了\n\n' + getJustTimeString() 
    print(info)
    send(info)


# 打卡提醒
def CheckIn():
    info = '该打卡了'
    print(info)
    send(info)

if __name__ == "__main__":

    # welecomeInfo = '大家好，我是你们的提醒小助手\n' \
    #     + '本次新增or更新事件 : 修正Token bug ' 
    # send(welecomeInfo)


    sendByCard('Daily打卡提醒','快乐的一天开始了，来打个卡吧！','','https://einkcn.com/zb_users/upload/2020/08/20200808120358159685943870716.png')
    # exerciseTimeUp()
    # CheckIn()
