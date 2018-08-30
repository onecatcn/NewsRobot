# -*- coding: utf-8 -*-
import os
import sys
import time
#import datetime
from datetime import datetime,timedelta
from get_Cnbeta_news import *
from auto_email_py2 import *


def sleeptime(starttime,targettime):

    now_time =  datetime.now()
    tomorrow_time = now_time + timedelta(days=+1)
    tomorrow_time_nyr = tomorrow_time.strftime('%Y-%m-%d')
    dateStr = tomorrow_time_nyr+" "+targettime
    start_timestamp = time.mktime(time.strptime(dateStr,'%Y-%m-%d %H:%M:%S'))
    wait_time = start_timestamp-starttime

    return wait_time

class MyTestDaemon(cnBeta_Daemon):
 
        
    def run(self):
##        keyword_list = ['区块链','AI']
        days = 1
        collect_period = 1*24*60*60
##        emaillist =  "kaiwang85@foxmail.com,onecat@163.com,wangkaiwx@chinamobile.com"
        keyword_list = ['\bAI\b','人工智能','机器学习','深度学习','自然语言处理','\bNLP\b','机器视觉','物联网','NB-IoT','智能硬件','机器人','智能家居','智能音箱','\bamazon\b','\bapple\b','google','区块链','车联网','自动驾驶','5G','工业互联网','机器智能','自动驾驶','计算机视觉','高精度地图','\bAR\b','\bSLAM\b','数据分析','数据运营','大数据服务']
        emaillist = "wangkaiwx@chinamobile.com"
        emaillist = "sunlin@chinamobile.com,kaiwang85@foxmail.com,wangkaiwx@chinamobile.com,fanxiaohui@chinamobile.com,luoda@chinamobile.com,pengwei@chinamobile.com,shuchang@chinamobile.com"
        fpath = '/home/kai/05_newsupdate/03_cnbetanewspider/04_20180813_kwordupdate/99_draft/'
        
        sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
        ''''' 
        立即执行一次 
        每天target time执行一次 
        '''
        while True:  
            print(time.strftime('%Y-%m-%d %X',time.localtime()))
            date_local = time.strftime('%Y-%m-%d',time.localtime())
            starttime = time.time()
            targettime = "08:00:00"
            cnbetaspider = spider()
            cnbetaspider.process_cnBeta(fpath,days,keyword_list)
##            process_cnBeta(keyword_list,fpath,collect_period)
            auto_email(emaillist,keyword_list,fpath,date_local)
            sys.stdout.write('Daemon Alive! {}\n'.format(time.ctime()))
            sys.stdout.flush()
            n = sleeptime(starttime,targettime)
            print("we will wait for",n,"seconds to execute next email")
            time.sleep(n)    

if __name__ == '__main__':
    PIDFILE = '/tmp/daemon-example.pid'
    LOG = '/tmp/daemon-example.log'
    
    daemon = MyTestDaemon(pidfile=PIDFILE, stdout=LOG, stderr=LOG)

    if len(sys.argv) != 2:
        print('Usage: {} [start|stop]'.format(sys.argv[0]), sys.stderr)
        raise SystemExit(1)

    if 'start' == sys.argv[1]:
        print("check start 1")
        daemon.start()
        print("check start 2")
    elif 'stop' == sys.argv[1]:
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        daemon.restart()
    else:
        print('Unknown command {!r}'.format(sys.argv[1]), sys.stderr)
        raise SystemExit(1)


