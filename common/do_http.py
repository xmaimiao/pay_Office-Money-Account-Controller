import requests
import json
import re

class Dohttp:
    def __init__(self):
        self.sessions = requests.sessions.Session()

    def dohttp(self,url=None,data=None,method=None,headers=None,json=None):
        method = method.lower()
        headers = eval(headers)
        if method == 'get':
            resp = self.sessions.request(url=url,method=method,params=data,headers=headers)
        elif method =='post':
            if json :
                resp = self.sessions.request(json=eval(json),url=url,method=method,headers=headers)
            else:
                resp = self.sessions.request(data=eval(data),url=url,method=method,headers=headers)
        else:
            resp=None
            print("出錯了！")
        return resp

    def close(self):
        self.sessions.close()

if __name__ == '__main__':
    url ="http://wmpay.doocom.net:8080/office-money-accounts?lang=zh_MO"
    headers = "{'Authorization':'new_592613dc-fcf3-43df-affd-43cc62f5ada4','Content-Type':'application/json'}"
    data ='{"approverList": [61651,61656,61657,61658,61659],"bankAccount": "6228434876637892842","bankAccountName": "澳门科技大学","bankName": "中国建设银行","bankId": 1,"groupId": 618,"makerList": [61651,61656,61657,61658,61659],"name": "澳科大-學費收款7/6-04","use": "收費"}'
    do = Dohttp().dohttp(url=url, json=data, headers=headers, method='post')
    print(do.json()['success'])
    msg = json.loads(do.text)
    print(msg)