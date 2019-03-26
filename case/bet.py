#coding:utf-8
import requests
import time
import threading
import datetime

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
class bet():
    url='http://group.iwc678.com/'
    file_path= '../dataconfig/username.txt'
    password="mkonji123"
    error_path = '../dataconfig/error_bet.txt'
    #彩种ID
    lotterys=[1,2,3,4,5,6,7]
    #下注金额
    num=10
    times=5

    # 获取彩种各注别
    def get_group(self,token,lottery_id):
        data={"lottery_id":lottery_id,
              "token":token
              }
        interface='server/api_game/sporting/query/fast'

        res=requests.get(url=self.url+interface,params=data).json()

        bet_group=[]
        game_group_code=''
        for game_group in res["data"]:
            #小于0是快捷竞猜 我猜
            if game_group["game_group_id"]>0:
                game_group_code=game_group["game_group_code"].encode("UTF-8")+"/"
                for bet_group_names in game_group["details"]:


                    bet_group_name=bet_group_names["bet_group_name"].encode("UTF-8")

                    game_group_code=game_group_code+bet_group_name+"+"


                bet_group.append(game_group_code.decode("UTF-8")[:-1]+"/")
        #print bet_group[0]
        return bet_group

    #下注指定格式 content 注别,times 递归次数
    def bet(self,token,lottery_id,content,times):
        times=times-1
        if times>0:
            data = {"lottery_id": lottery_id,
                    "token": token,
                    "content":content

                    }
            interface = 'server/api_game/sporting/business'

            ress = requests.post(url=self.url + interface, params=data)
            # print "下注彩种：{0} 类别：{1} 次数：{3} 结果:{2}"\
            #             .format(lottery_id,content.encode("utf-8"),ress.text.encode("utf-8"),self.times-times)
            if ress.text.find("We're sorry, but something went wrong (500)")==-1:
                res=ress.json()

                if res["success"]==0:

                    if res["message"]==u"已封盘，停止下单":

                    #     #获取封盘时间
                    #     close_delay=self.get_time( token, lottery_id)
                    #     if close_delay<0:
                    #         print "已封盘，停止下单.等待{4}S彩种：{0} 类别：{1} 次数：{3} 原因:{2}". \
                    #             format(lottery_id, content.encode("utf-8"), res, 5 - times,abs(close_delay))
                    #         time.sleep(abs(close_delay))
                    #     elif close_delay==0:
                    #         print "彩种：{0} 未开盘".format(lottery_id)
                    #         assert False
                    #     else:
                    #         print "彩种：{0} 未知原因{1}".format(lottery_id,close_delay)
                    #
                    #     self.bet(token,lottery_id,content,times)
                    # else:
                    #     print "下注失败彩种：{0} 类别：{1} 次数：{3} 原因:{2}"\
                    #         .format(lottery_id,content.encode("utf-8"),res["message"],self.times-times)
                    #     time.sleep(3)
                    #     self.bet(token,lottery_id,content,times)
                        print "已封盘，停止下单.等待{4}S彩种：{0} 类别：{1} 次数：{3} 原因:{2}". \
                            format(lottery_id, content.encode("utf-8"), res, 5 - times, 13)
                    close_delay = self.get_time(token, lottery_id)
                    while(close_delay<=0):
                        #获取封盘时间，直到>0
                        time.sleep(3)
                        close_delay = self.get_time(token, lottery_id)

                    self.bet(token, lottery_id, content, times)
                else:
                    print "彩种：{0} 类别：{1} 下注成功".format(lottery_id,content.encode("utf-8"))

            else:
                print "下注彩种：{0} 类别：{1} 次数：{3} 结果:{2}" \
                    .format(lottery_id, content.encode("utf-8"), "We're sorry, but something went wrong (500)", self.times - times)
                time.sleep(3)
                self.bet(token, lottery_id, content, times)
        else:

            self.write_error(token+" " +str(lottery_id)+" "+ content.encode("utf-8"))
    # 该彩种全下注
    def bets(self, token, lottery_id, num):

        bet_groups=self.get_group(token, lottery_id)
        for bet_group in bet_groups:
            content= bet_group+str(num)
            self.bet(token,lottery_id,content,self.times)

    def read_data(self):

        with open(self.file_path) as fp:
            data=fp.readlines()
        #去掉\n
        for  i in range(len(data)):
            data[i] = data[i].rstrip('\n')
        return data
    def login(self,username,password):
        interface='/server/api_game/base/session/login/game_member'
        data = {"account": username,
                    "password": password,

                    }
        res = requests.post(url=self.url + interface, params=data).json()
        if res["success"]==1:
            print "{0}登陆成功".format(username)
            return res["data"]["token"]
        else:
            print "{0}登陆失败，原因：{1}".format(username,res["message"].encode("utf-8"))
            assert False

    def bet_full(self):
        usernames=self.read_data()
        for username in usernames:
            token=self.login(username,self.password)
            #彩种遍历
            threads=[]
            for lottery_id in self.lotterys:
                t=threading.Thread(target=self.bets,args=(token,lottery_id,self.num))
                #self.bets(token,lottery_id,self.num)
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
     #获取封盘时间
    def get_time(self,token,lottery_id):
        data={"lottery_id":lottery_id,
              "token":token
              }
        interface='server/api_game/sporting/base/all_lotteries'

        res=requests.get(url=self.url+interface,params=data).json()
        datas = res["data"]
        for data in datas:
            if data["lottery_id"]==lottery_id:
                return int(data["close_delay"])

    def write_error(self,data_list):

        with open(self.error_path, 'a+') as f:

             f.writelines(data_list+"\n")

if __name__ == '__main__':
    bet=bet()
    #bet.get_group("c0e9be7980c2dd8a018473c26e100fc8f1f960772c5e25cfb1911649da04984d",7)
    #bet.bet("c0e9be7980c2dd8a018473c26e100fc8f1f960772c5e25cfb1911649da04984d",2,"1/2/3",5)
    #bet.bets("c0e9be7980c2dd8a018473c26e100fc8f1f960772c5e25cfb1911649da04984d",1,5)
    #print bet.read_data()
    print datetime.datetime.now()
    print bet.bet_full()
    print datetime.datetime.now()

