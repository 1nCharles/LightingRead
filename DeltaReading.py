import requests
import json
import logger
from jsonpath import jsonpath
from configparser import ConfigParser


headers = {
"Host": "www.ai-reading.com",
"Connection": "keep-alive",
"content-type": "application/x-www-form-urlencoded",
"charset": "utf-8",
"User-Agent": "Mozilla/5.0 (Linux; Android 15; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.120 Mobile Safari/537.36 XWEB/1220099 MMWEBSDK/20240802 MMWEBID/9027 MicroMessenger/8.0.53.2740(0x28003533) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
"Accept-Encoding": "gzip, deflate, br"
}


def get_url(mode):
    url="https://www.ai-reading.com/index.php?c=lm&a="
    if mode == 0:
        url+="getMemberInfo"
    if mode == 1:
        url+="requestPost"
    if mode == 2:
        url+="request"
    if mode == 3:
        url+=""
    if mode == 4:
        url+="requestPost"
    if mode == 5:
        url+="request"
    return url

def get_data(rid=0,readtime=0,Transe={},Select={},mode=0):
    data1="openid="+openid+"&sessionKey="+secretid
    if mode == 0:
        data2="&isGift=1&tokentp=2"
    elif mode == 1:
        data2="&part=1&rId="+str(rid)+"&readTime="+str(readtime)
    elif mode == 2:
        data2="&onOption="+str(Select)+"&part=2&readTime="+str(readtime)+"&challenge=undefined&rId="+str(rid)
    elif mode == 3:
        data2=''
    elif mode == 4:
        data2="&part=4&rId="+str(rid)+"&readTime="+str(readtime)
    elif mode == 5:
        data2="&onOption="+str(Transe)+"&part=5&rId="+str(rid)+"&readTime="+str(readtime)+"&trainType="+'{"1":"1","2":"1"}'
    return data1+data2

def post(url,headers,data):
    res1 = requests.post(url=url,data=data,headers=headers)
    content = res1.json()
    return content

def get_memberInfo():
    json=post(get_url(0),headers,get_data(mode=0))
    return json['data']

def get_Task():
    data="openid="+openid+"&sessionKey="+secretid+"&tokentp=2&type=1&pages=1&new=1"
    url="https://www.ai-reading.com/index.php?c=task&a=myTask"
    json=post(url,headers,data)
    return json['data']

def get_Taskinfo(taskid):
    data="openid="+openid+"&sessionKey="+secretid+"&tokentp=2&task_id="+taskid
    url="https://www.ai-reading.com/index.php?c=task&a=studentTaskInfo"
    json=post(url,headers,data)
    return json['data']

def First(rid,readtime):
    data=get_data(rid=rid,readtime=readtime,mode=1)
    json=post(get_url(1),headers,data)
    if json['error']!='100':
        logger.logging.info("完成阅读失败")
        exit(0)
    logger.logging.info("完成阅读成功！")
    return True

def get_select(answers):
    json={}
    i=1
    for ans in answers:
        json[str(i)]={"0":ans}
        i+=1
    return json

def get_answerls(rid):
    url="https://www.ai-reading.com/index.php?c=lm&a=request"
    data="openid="+openid+"&sessionKey="+secretid+"&part=2&readTime=&rId="+rid+"&review=0"
    json=post(url,headers,data)
    if(json['data']==''):
        logger.logging.info("获取答案失败！！！")
        exit(0)
    return jsonpath(json,("$.data.quiz..right"))

def Second(select,readtime,rid):
    url=get_url(2)
    data=get_data(Select=select,readtime=readtime,rid=rid,mode=2)
    json=post(url,headers,data)
    if json['error']!='100':
        logger.logging.error("答题错误")
        exit(0)
    logger.logging.info("答题成功！！！！")
    return True

def Fourth(rid,readtime):
    url=get_url(4)
    data=get_data(rid=rid,readtime=readtime,mode=4)
    json=post(url,headers,data)
    if json['error']!='100':
        logger.logging.error("答题错误")
        exit(0)
    logger.logging.info("答题成功！！！！")
    return True

def get_answers1(rid):
    url=get_url(2)
    data="openid="+openid+"&sessionKey="+secretid+"&part=5&rId="+rid
    json=post(url,headers,data)
    if json['data']=='':
        logger.logging.error("获取翻译失败")
        exit(0)
    answers=jsonpath(json['data'],"$.train..answer")
    return answers

def Fifth(transe,rid,readtime):
    url=get_url(5)
    data=get_data(Transe=transe,rid=rid,readtime=readtime,mode=5)
    json=post(url,headers,data.encode('utf-8'))
    if json['error']!='100':
        logger.logging.error("答题错误")
        exit(0)
    logger.logging.info("答题成功！！！！")
    return True


def get_Tanse(answer):
    i=1
    json={}
    for ans in answer:
        json[str(i)]=ans
        i+=1
    return json

def main():
    readtime=[420,800,100,300,800]
    json=get_memberInfo()
    logger.logging.info("获取个人信息ing~")
    if(json==''):
        logger.logging.error("获取失败，请检查openid与secretid！！")
        exit(0)
    logger.logging.info("姓名："+json['name'])
    logger.logging.info("学校："+json['school'])
    logger.logging.info("获取作业id列表ing~")
    json1=get_Task()
    if(json1==''):
        logger.logging.error("获取作业失败，请检查openid与secretid！！")
        exit(0)
    Taskidlist=jsonpath(json1,"$..id")
    logger.logging.info(Taskidlist)
    logger.logging.info("获取作业详情ing~")
    input=0
    json2=get_Taskinfo(Taskidlist[input])
    if json2=='':
        logger.logging.error("获取作业详情失败！")
    ridlist=jsonpath(json2,"$.requestList..id")
    #logger.logging.info(ridlist)
    #ridlist=['1154']
    logger.logging.info("开始做题！！")
    i=1
    for rid in ridlist:
        logger.logging.info("进度：第"+str(i)+"题")
        First(rid,readtime[0])
        answers=get_answerls(rid)
        logger.logging.info(answers)
        seclect=get_select(answers)
        logger.logging.info(seclect)
        json3=Second(seclect,readtime[1],rid)
        logger.logging.info("跳过口语题！")
        Fourth(rid,readtime[3])
        answers1=get_answers1(rid)
        logger.logging.info(answers1)
        transe=get_Tanse(answers1)
        logger.logging.info(transe)
        json4=Fifth(transe,rid,readtime[4])
        i+=1
    


if __name__ == '__main__':
    conf = ConfigParser()
    conf.read('./config.ini',encoding='utf-8')
    #conf.read('./LightingRead/config.ini',encoding='utf-8')
    openid=conf['user']['openid']
    secretid=conf["user"]['secretid']
    main()