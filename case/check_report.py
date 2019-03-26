#coding:utf-8
import requests
import time
import threading
from create_user import *
from jsondiff import diff
import requests
import datetime
class check_report:

    def __init__(self):
        self.headers=create_user().headers
        self.url="http://admin.iwc678.com/"
        self.file_path = '../dataconfig/report.txt'
    def write_report(self):
        data_list=self.get_report()
        with open(self.file_path, 'a+') as f:
            for i in data_list:
             f.writelines(i+"\n")
    def read_report(self):
        with open(self.file_path) as fp:
            data=fp.readlines()
        #去掉\n
        for  i in range(len(data)):
            data[i] = data[i].rstrip('\n')
        return data

#总公司往下递归，今天报表
    def get_report(self,organization_id=1,time=None,list_report=[]):


        interface = "server/api/manage/statistic/reports"

        querystring = {"report_type": "1",
                       "settlement_status": "1",
                       "search_start_at": self.time_today(time),
                       "search_end_at": self.time_today(time),
                       "organization_id": organization_id,
                       "category": "1"}
        payload = ""
        response = requests.request("GET", self.url+interface, data=payload, headers=self.headers, params=querystring).json()

        for proxy in response["organization_data"]:

            if proxy["name"]==create_user.tag:
                list_report.append(json.dumps(proxy))
                #print proxy
                # self.write_report(proxy)
                # self.read_report(int(proxy["business_id"]))
                if proxy["level_id"]!=5:

                    self.get_report(organization_id=proxy["business_id"], time=time, list_report=list_report)
        # print list_report
        # proxy=json.dumps(proxy)
        #
        return list_report

    def time_today(self,time=None):
        if time == None:
            return datetime.datetime.now().strftime('%Y-%m-%d')
        else:
            return time.strftime('%Y-%m-%d')

    def check_report(self):
        real_reports=self.read_report()
        now_reports=self.get_report()
        print "比对结果如下"
        # if len(real_reports) !=len(now_reports):
        #     print "缺少报表！模板有{}，实际获得{}".format(len(real_reports),len(now_reports))
        #     assert False
        for real in real_reports:
            for now in now_reports:
                if type(real)==str:

                    real=json.loads(real)
                if type(now) == str:
                     now=json.loads(now)
                if real["business_id"]==now["business_id"]:
                    diffjson=   diff(real,now,syntax='symmetric')
                    if diffjson!={}:
                        print "用户{}帐不对，值前后对比:".format(real["master_username"])
                        print diffjson


if __name__ == '__main__':
    #print check_report().write_report()
    check_report().check_report()

