#coding:utf-8
import requests
import json
class RunMethod:
    def post_main(self,url,data,header=None):
        res = None
        if header !=None:
            res = requests.post(url=url,data=data,headers=header)
        else:
            res = requests.post(url=url,data=data)

        return res.json()

    def get_main(self,url,data=None,header=None):
        res = None



        if header !=None:

            res = requests.get(url=url,data=data,headers=header,verify=False)
            # res = requests.get(url=url, params=data, headers=header, verify=False)
            res=requests.request("GET", url, headers=header, params=data)
        else:
            res = requests.get(url=url,data=data,verify=False)
            # res = requests.get(url=url, params=data, verify=False)
            res = requests.request("GET", url, params=data)
        return res.json()

    def run_main(self,method,url,data=None,header=None):
        res = None
        # 带中文的参数需要编码
        if type(data) == unicode:
            data = data.encode("utf-8")
        if method == 'Post':
            res = self.post_main(url,data,header)
        else:
            res = self.get_main(url,data,header)
        return json.dumps(res,ensure_ascii=False)
    #return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)




