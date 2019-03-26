# coding:utf-8
import sys

import json
import requests


class create_user:
    url = 'http://admin.iwc678.com/'
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    interface = "server/api/base/session/login/manage"
    username = 'zongH01'
    password = 'mkonji123'
    organization_name = 'n6esJxOy'
    # url="http://am.us688us.com/"
    # username = 'n6esJxOy'
    # password = 'vqzF3qkK'
    tag = 'TEST'

    def __init__(self):
        self.token = self.login(self.interface, self.username, self.password)
        self.headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Accept': 'application/json, text/plain, */*',
            'Token': self.token
        }

    def login(self, interface, username, password):
        url = self.url + interface
        # print "{0}\"\" {1}".format(username,password)
        # date="\{\"account\":\"{0}\",\"password\":\"{1}\",\"code\":\"puya\"\}".format(username, password)
        data = '{"account":"' + username + '","password":"' + password + '","code":"puya"}'
        sessions=requests.session()
        res = sessions.post(url=url, data=data, headers=self.headers)

        print url, data, res.text

        if res.text.find('"is_update_password":false')!=-1:
            user_id=res.json()['user_id']
            headers = {
                'Content-Type': "application/json",
                'cache-control': "no-cache",
                'Accept': 'application/json, text/plain, */*',
                'Token': res.json()['token']
            }
            self.updata_password(user_id,headers)
            return self.login(interface, username, password)
        elif res.text.find(u'{"message":"账号或密码错误"}')!=-1:
            if password=="mkonji123":
                password="qwe123"
            else:
                password="mkonji123"

            return  self.login(interface, username, password)
        else:
            tokens= res.json()['token']
            return tokens

    def updata_password(self,user_id,headers):
        url = self.url + 'server/api/base/session/password'
        data='{"user_id":"'+str(user_id)+'","password":"mkonji123"}'
        requests.put(url=url, data=data,headers=headers)

    # 获取代理ID
    # 等级，代理名称
    def get_proxy(self, level_id, master_account):
        interface = "server/api/manage/query/parent_organizations?level_id={0}".format(level_id)
        jsons = requests.get(url=self.url + interface, headers=self.headers).json()
        for i in range(len(jsons)):
            if jsons[i]['master_account'] == master_account:
                return jsons[i]['organization_id']

    # 新增代理
    # organization_id 代理上级ID ，level_id新建层级ID，account 新建层级用户名 retreating_mode_proportion 退水比例，self_proportion 占层比例
    def create_proxy(self, level_id, organization_id, account, retreating_mode_proportion, self_proportion):
        # 额度
        credits = 10000000000 - level_id * 100000
        max_member_count = 99999 - level_id * 10
        data = '{"organization_id":' + str(organization_id) + ',"account":"' + str(
            account) + '","password":"qwe123","name":"'+self.tag+'","credits":' + str(
            credits) + ',"max_member_count":' + str(max_member_count) + ',"retreating_mode_proportion":' + str(
            retreating_mode_proportion) + ',"credit_mode":1,"is_adjustable_replenishment":true,"is_adjustable_odds":true,"handicaps":[1,2,3,4],"is_adjustable_retreating":true,"proportion_details":[{"id":1,"lottery_id":1,"lottery_name":"北京赛车","self_upper_limit":0,"self_lower_limit":0,"interception_category":2,"upper_limit":"1.0","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"is_remain_occupation":true,"invalid":false},{"id":2,"lottery_id":2,"lottery_name":"幸运飞艇","self_upper_limit":0,"self_lower_limit":0,"interception_category":2,"upper_limit":"1.0","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"is_remain_occupation":true,"invalid":false},{"id":3,"lottery_id":3,"lottery_name":"重庆时时彩","self_upper_limit":0,"self_lower_limit":0,"interception_category":2,"upper_limit":"1.0","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"is_remain_occupation":true,"invalid":false},{"id":4,"lottery_id":4,"lottery_name":"广东快乐十分","self_upper_limit":0,"self_lower_limit":0,"interception_category":2,"upper_limit":"1.0","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"is_remain_occupation":true,"invalid":false},{"id":5,"lottery_id":5,"lottery_name":"幸运农场","self_upper_limit":0,"self_lower_limit":0,"interception_category":2,"upper_limit":"1.0","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"is_remain_occupation":true,"invalid":false},{"id":6,"lottery_id":6,"lottery_name":"极速赛车","self_upper_limit":0,"self_lower_limit":0,"interception_category":2,"upper_limit":"1.0","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"is_remain_occupation":true,"invalid":false},{"id":7,"lottery_id":7,"lottery_name":"腾讯分分彩","self_upper_limit":0,"self_lower_limit":0,"interception_category":2,"upper_limit":"1.0","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"is_remain_occupation":true,"invalid":false},{"id":3761,"lottery_id":8,"lottery_name":"幸运赛车","self_upper_limit":0,"self_lower_limit":0,"interception_category":2,"upper_limit":"1.0","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"is_remain_occupation":true,"invalid":false},{"id":2759,"lottery_id":9,"lottery_name":"澳洲十分","self_upper_limit":0,"self_lower_limit":0,"interception_category":2,"upper_limit":"1.0","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"is_remain_occupation":true,"invalid":false}]}'
        interface = 'server/api/manage/base/organization?organization_id={}'.format(level_id)
        res = requests.post(url=self.url + interface, data=data, headers=self.headers).text.encode('UTF-8')
        print res + account

        # if  res.find("message")== -1:
        #   assert '新建代理失败，原因：{0}，用户名：{1}'.format(res,account)

    def create_member(self, level_id, organization_id, account, credits, retreating_mode_proportion, self_proportion):
        data = '{"level_id":' + str(level_id) + ',"organization_id":' + str(organization_id) + ',"account":"' + str(
            account) + '","password":"qwe123","name_remark":"'+self.tag+'","name":"'+self.tag+'","credits":' + str(
            credits) + ',"retreating_mode_proportion":' + str(
            retreating_mode_proportion) + ',"handicap_id":4,"details":[{"id":8,"lottery_id":1,"lottery_name":"北京赛车","self_upper_limit":"0.9","self_lower_limit":"0.0","interception_category":2,"upper_limit":"0.9","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"invalid":false},{"id":9,"lottery_id":2,"lottery_name":"幸运飞艇","self_upper_limit":"0.9","self_lower_limit":"0.0","interception_category":2,"upper_limit":"0.9","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"invalid":false},{"id":10,"lottery_id":3,"lottery_name":"重庆时时彩","self_upper_limit":"0.9","self_lower_limit":"0.0","interception_category":2,"upper_limit":"0.9","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"invalid":false},{"id":11,"lottery_id":4,"lottery_name":"广东快乐十分","self_upper_limit":"0.9","self_lower_limit":"0.0","interception_category":2,"upper_limit":"0.9","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"invalid":false},{"id":12,"lottery_id":5,"lottery_name":"幸运农场","self_upper_limit":"0.9","self_lower_limit":"0.0","interception_category":2,"upper_limit":"0.9","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"invalid":false},{"id":13,"lottery_id":6,"lottery_name":"极速赛车","self_upper_limit":"0.9","self_lower_limit":"0.0","interception_category":2,"upper_limit":"0.9","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"invalid":false},{"id":14,"lottery_id":7,"lottery_name":"腾讯分分彩","self_upper_limit":"0.9","self_lower_limit":"0.0","interception_category":2,"upper_limit":"0.9","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"invalid":false},{"id":3762,"lottery_id":8,"lottery_name":"幸运赛车","self_upper_limit":"0.9","self_lower_limit":"0.0","interception_category":0,"upper_limit":"0.9","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"invalid":false},{"id":2760,"lottery_id":9,"lottery_name":"澳洲十分","self_upper_limit":"0.9","self_lower_limit":"0.0","interception_category":0,"upper_limit":"0.9","self_proportion":' + str(
            self_proportion) + ',"interception_proportion":0,"invalid":false}]}'
        interface = 'server/api/manage/base/member'
        res = requests.post(url=self.url + interface, data=data, headers=self.headers).text.encode('UTF-8')
        print res + account

        #  if res.find("message")== -1:
        #   assert '新建会员失败，原因：{0}，用户名：{1}'.format(res,account)

    # 代理各层级100%
    def create_proxysfull(self):

        for num in range(1, 6):
            organization_name = self.organization_name
            for level_id in range(1, 5):
                organization_id = self.get_proxy(level_id, organization_name)

                retreating_mode_proportion = 0
                if num == level_id:
                    self_proportion = 1
                    account = '{0}L{1}P{2}R0O0N{3}'.format(self.tag, level_id + 1, '100', num)
                else:
                    self_proportion = 0
                    account = '{0}L{1}P{2}R0O0N{3}'.format(self.tag, level_id + 1, '0', num)
                self.create_proxy(level_id, organization_id, account, retreating_mode_proportion, self_proportion)
                organization_name = account
            # 代理新增会员
            level_id = 5
            if num == level_id:
                self_proportion = 1
                account = '{0}L{1}P{2}R0O0N{3}'.format(self.tag, level_id + 1, '100', num)
            else:
                self_proportion = 0
                account = '{0}L{1}P{2}R0O0N{3}'.format(self.tag, level_id + 1, '0', num)
            organization_id = self.get_proxy(level_id, organization_name)
            self.create_member(level_id, organization_id, account=account, credits=9999000000,
                               retreating_mode_proportion=0, self_proportion=self_proportion)

    # 代理赚取固定退水，每个层级0.1
    def create_proxys_retreating(self):
        retreating_mode_proportion = 0.001
        organization_name = self.organization_name
        for level_id in range(1, 5):
            organization_id = self.get_proxy(level_id, organization_name)

            self_proportion = 0.1 + level_id * 0.02
            account = '{0}L{1}P{2}R{3}O0N{4}'.format(self.tag, level_id + 1, str(int(self_proportion * 100)),
                                                     int(retreating_mode_proportion * 1000), 1)
            self.create_proxy(level_id, organization_id, account, retreating_mode_proportion, self_proportion)
            organization_name = account
        # 代理新增会员
        level_id = 5
        self_proportion = 0.1 + level_id * 0.02
        account = '{0}L{1}P{2}R{3}O0N{4}'.format(self.tag, level_id + 1, str(int(self_proportion * 100)),
                                                 int(retreating_mode_proportion * 1000), 1)
        organization_id = self.get_proxy(level_id, organization_name)
        self.create_member(level_id, organization_id, account=account, credits=9999000000,
                           retreating_mode_proportion=retreating_mode_proportion, self_proportion=self_proportion)

    # 代理赚取全部退水
    def create_proxys_retreating_full(self):
        for num in range(1, 6):
            organization_name = self.organization_name
            for level_id in range(1, 5):
                organization_id = self.get_proxy(level_id, organization_name)
                self_proportion = 0.1 + level_id * 0.02
                if num == level_id:
                    retreating_mode_proportion = 1
                    account = '{0}L{1}P{2}R{3}O0N{4}'.format(self.tag, level_id + 1, str(int(self_proportion * 100)),
                                                             int(retreating_mode_proportion * 100), num)
                else:
                    retreating_mode_proportion = 0
                    account = '{0}L{1}P{2}R{3}O0N{4}'.format(self.tag, level_id + 1, str(int(self_proportion * 100)),
                                                             int(retreating_mode_proportion * 100), num)
                self.create_proxy(level_id, organization_id, account, retreating_mode_proportion, self_proportion)
                organization_name = account
            # 代理新增会员
            level_id = 5
            self_proportion = 0.1 + level_id * 0.02
            if num == level_id:
                retreating_mode_proportion = 1
                account = '{0}L{1}P{2}R{3}O0N{4}'.format(self.tag, level_id + 1, str(int(self_proportion * 100)),
                                                         int(retreating_mode_proportion * 100), num)
            else:
                retreating_mode_proportion = 0
                account = '{0}L{1}P{2}R{3}O0N{4}'.format(self.tag, level_id + 1, str(int(self_proportion * 100)),
                                                         int(retreating_mode_proportion * 100), num)
            organization_id = self.get_proxy(level_id, organization_name)
            self.create_member(level_id, organization_id, account=account, credits=9999000000,
                               retreating_mode_proportion=retreating_mode_proportion, self_proportion=self_proportion)

    # 代理赚取赔率，每个层级0.001，没有赚退水,
    def create_proxys_odd(self):
        # 赚水
        retreating_mode_proportion = 0
        odd = 0.001
        organization_name = self.organization_name
        for level_id in range(1, 5):
            organization_id = self.get_proxy(level_id, organization_name)

            self_proportion = 0.1 + level_id * 0.02
            account = '{0}L{1}P{2}R{3}O{5}N{4}'.format(self.tag, level_id + 1, str(int(self_proportion * 100)),
                                                       int(retreating_mode_proportion * 1000), 1, int(odd * 1000))
            self.create_proxy(level_id, organization_id, account, retreating_mode_proportion, self_proportion)
            organization_name = account
        # 代理新增会员
        level_id = 5
        self_proportion = 0.1 + level_id * 0.02

        account = '{0}L{1}P{2}R{3}O{5}N{4}'.format(self.tag, level_id + 1, str(int(self_proportion * 100)),
                                                   int(retreating_mode_proportion * 1000), 1, int(odd * 1000))
        organization_id = self.get_proxy(level_id, organization_name)
        self.create_member(level_id, organization_id, account=account, credits=9999000000,
                           retreating_mode_proportion=retreating_mode_proportion, self_proportion=self_proportion)

    # 修改赔率 row_odds_discrepancy 降赔额度
    def modify_odd(self, username, password, lottery_id, row_odds_discrepancy):
        token = self.login(self.interface, username, password)
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Accept': 'application/json, text/plain, */*',
            'Token': token
        }
        url = self.url + "server/api/manage/middle/odds?lottery_id={}".format(lottery_id)
        group = self.get_odd(token, lottery_id)
        list_lottery = []
        for i in range(len(group)):
            dist_lottery = {}
            dist_lottery['setting_group_id'] = group[i]['setting_group_id']
            dist_lottery['max_row_odds_discrepancy'] = group[i]['max_row_odds_discrepancy']
            dist_lottery['row_odds_discrepancy'] = row_odds_discrepancy
            json.dumps(dist_lottery, ensure_ascii=False)

            list_lottery.append(dist_lottery)
        dist_lottery = {"lottery_id": lottery_id, "details": list_lottery}
        json_lottery = json.dumps(dist_lottery, ensure_ascii=False)

        print json_lottery
        res = requests.put(url=url, data=json_lottery, headers=headers)
        print res.text

        data = '{"lottery_id":1,"details":[]}'
        # requests.put(url=url,data)

    # 查看该彩种赔率分组
    def get_odd(self, token, lottery_id):
        url = self.url + "server/api/manage/middle/odds?lottery_id={}".format(lottery_id)
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Accept': 'application/json, text/plain, */*',
            'Token': token
        }
        res = requests.get(url=url, headers=headers)
        # print res.json()
        return res.json()

    # 修改一条线所有赚取赔率0.001
    def modify_odds(self):
        usernames = {"TESTL2P12R0O1N1", "TESTL3P14R0O1N1", "TESTL4P16R0O1N1", "TESTL5P18R0O1N1"}
        for username in usernames:
                #各个彩种
            for lottery_id in range(1, 10):
                self.modify_odd(username=username, password='qwe123', lottery_id=lottery_id,
                                row_odds_discrepancy=0.001)


if __name__ == '__main__':
    print create_user().create_proxysfull()
    #create_user().create_proxys_retreating()
    #create_user().create_proxys_retreating_full()
    #
    #create_user().create_proxys_odd()
    create_user().modify_odds()
