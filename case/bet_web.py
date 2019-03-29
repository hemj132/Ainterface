#coding:utf-8
import requests
import time
import threading
import datetime
import json
import sys
import os
reload(sys)

sys.setdefaultencoding('UTF-8')
class bet():
    url='http://member.iwc678.com/'
    #url = 'http://mb.us688us.com/'
    password="qwe123"
    error_path = '../dataconfig/error_bet.txt'
    username_path= '../dataconfig/username.txt'
    #彩种ID
    lotterys=[1,2,3,4,5,6,7,8,9]
    #lotterys = [6, 7]
    #下注金额
    num=10
    times=20
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Accept': 'application/json, text/plain, */*',

    }

    def __init__(self, file_path=None):
        if file_path == None:
            self.file_path= '../dataconfig/bet'
        else:
            self.file_path = file_path
        self.data = self.read_data()
        if os.path.isfile(self.error_path):
            os.remove(self.error_path)

    # 读取json文件
    def read_data(self):
        with open(self.file_path) as fp:
            data = json.load(fp)

            return data

    def read_username(self):


        with open(self.username_path) as fp:
            data = fp.readlines()
        # 去掉\n
        for i in range(len(data)):
            data[i] = data[i].rstrip('\n')
        return data

    def login(self, username,password):
        url = self.url+"server/api/base/session/login/member"
        data='{"account":"'+username+'","password":"'+password+'","code":"puya"}'


        res = requests.post(url=url,data=data,headers=self.headers)
        #print url, data,res.text
        print username+"登陆成功"
        self.write_error(username+"登陆成功")
        return res.json()['token']
    #
    def bet_full(self,username,valid_amount):

            token = self.login(username, self.password)

            headers = {
                'Content-Type': "application/json",
                'cache-control': "no-cache",
                'Accept': 'application/json, text/plain, */*',
                'Token': token
            }
            for lottery_id in self.lotterys:
                for bet_json in self.data["bet"]:
                    if bet_json["lottery_id"]==lottery_id:
                        odds_json=self.get_odds(headers,lottery_id)
                        #替换注额与赔率
                        for bet_games in bet_json["details"]:
                            for odd_games in odds_json:
                                if bet_games["game_id"]==odd_games["game_id"]:
                                    bet_games["execution_odds"]=odd_games["execution_odds"]
                                    bet_games["valid_amount"]=valid_amount
                        print bet_json
                        self.bet(headers,bet_json,self.times)

    def get_odds(self,headers,lottery_id):
        interface="server/api/member/business/odds?lottery_id={}".format(lottery_id)

        res = requests.get(url=self.url + interface,headers=headers).json()
        return res
    def bet(self,headers,bet_json,times):
        starttime=datetime.datetime.now()
        if times>0:

            url = self.url+"server/api/member/business/bet"


            res = requests.post(url=url,data=json.dumps(bet_json).encode("utf-8"),headers=headers).text
            times -= 1
            if res.find("下单成功")==-1:
                print "彩种：{0}  下注失败{1}，等待15S".format(bet_json["lottery_id"],res)

                time.sleep(15)
                self.bet(headers,bet_json,times)

            else:
                print "彩种：{0}  下注成功，消耗时间{1}".format(bet_json["lottery_id"],datetime.datetime.now()-starttime)
                self.write_error("彩种：{0}  下注成功，消耗时间{1}".format(bet_json["lottery_id"],datetime.datetime.now()-starttime))
        else:
            self.write_error(headers["Token"] + " " + str(bet_json["lottery_id"]))


    def bet_alluser(self):

        usernames = self.read_username()
        threads = []
        for username in usernames:
            self.bet_full(username, self.num)



        #     t = threading.Thread(target=self.bet_full, args=(username, self.num))
        #     threads.append(t)
        # for t in threads:
        #     t.start()
        # for t in threads:
        #     t.join()











    def write_error(self,data_list):

        with open(self.error_path, 'a+') as f:

             f.writelines(data_list+"\n")


if __name__ == '__main__':
    bet=bet()
    #print bet.data
    # headers = {
    #     'Content-Type': "application/json;charset=UTF-8",
    #     'Accept': 'application/json, text/plain, */*',
    #     'Token': "c33dcbadfa9a366ea9c558b5a1a49fcc7f233a018c41d1e2a7b6170597208ded"
    # }
    # jsons='{"lottery_id":9,"details":[{"valid_amount":100,"game_id":1771,"name":"大","setting_group_id":315,"execution_odds":"1.94","invalid":false,"result_name":"冠军-大","key":1},{"valid_amount":100,"game_id":1772,"name":"小","setting_group_id":315,"execution_odds":"1.94","invalid":false,"result_name":"冠军-小","key":2}],"game_ids":[1771,1772],"setting_group_ids":[315,315]}'.encode("utf-8")

    print bet.bet_alluser()

