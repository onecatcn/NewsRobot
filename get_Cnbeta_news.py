import requests,os,re,sys
from bs4 import BeautifulSoup
import urllib.parse
import time
from datetime import datetime
import atexit
import signal

HOMEPAGE_URL = 'https://www.cnbeta.com/'
JSON_URL = HOMEPAGE_URL + 'home/more'
AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.99'
HEADERS = {
        'User-Agent' :  AGENT,
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'referer' : HOMEPAGE_URL}

class spider(object):
    def __init__(self):
        print ('开始爬取内容。。。')

        
    def get_resource(self, url, headers):
        try:
            r = requests.get(url, headers = headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
    ##        print('URL: ' + r.url)
        except Exception as e:
            print(e)
            r = None
        finally:
            return r

    def get_csrf(self, res):
        if res is None:
            return None, None
        soup = BeautifulSoup(res.text, 'html.parser')
        #print("soup",soup)
        title = soup.head.find('title').get_text()
        param = soup.head.find(attrs={'name':'csrf-param'})['content']
        token = soup.head.find(attrs={'name':'csrf-token'})['content']
    ##    print('Page Title check: ' + title)
    ##    print('param token check',param + ' = ' + token)
        return {'param' : param, 'token' : token}

    def get_timestamp_ms(self):
        return round(time.time()*1000)

    def get_json_url(self, csrf, page):
        params = {}
        params['type'] = 'all'
        params['page'] = page
        params[csrf['param']] = csrf['token']
        params['_'] = spider.get_timestamp_ms(self)
        params_str = urllib.parse.urlencode(params)
        return JSON_URL + '?&' + params_str

    def get_latest_days_of_year(self, n):
        ticks =  time.time() - n*24*60*60
        return ticks
##        today = datetime.now().timetuple().tm_yday
##        if today >= n:
##            return range(today, today - n, -1)
##        else:
##            return range(today, 0, -1)

    ##def saveinfo2(self, classinfo,keyword,fpath):
    ##    filetitle = keyword+"_cnBeta.txt"
    ##    filename = os.path.join( fpath, filetitle )
    ##        
    ##    f = open(filename, 'a')
    ##    f.writelines('title：' + artical_title + '\r\n')
    ##    f.writelines('time：' + inputtime + '\r\n')
    ##    f.writelines('summ：' + artical_summ + '\r\n')
    ##  ##          f.writelines('*********************************************\n')
    ##    f.writelines('\r\n')
    ##    f.close()

    def print_news(self, news_data, days,keyword_list,fpath):
        ticks = spider.get_latest_days_of_year(self,days)
        if news_data['result'] is None:
            return True
        end = False
        for news in news_data['result']['list']:
            note_time = news['inputtime']
            d = datetime.strptime(note_time,"%Y-%m-%d %H:%M")
            report_time = time.mktime(d.timetuple())
            
            if (report_time < ticks):
                end = True
                break
            #print("{inputtime} {label[name]} {title:<40} \n{url_show} \n{hometext}".format(**news))

            for kword in keyword_list:
                keyword = kword #unicode(kword, "utf8")
                ##print("check keyword",keyword)
                pattern = re.compile(keyword,re.IGNORECASE)
                if(pattern.findall("{hometext}".format(**news))):
                    print("hit it",kword)
                    print("{inputtime} {label[name]} {title:<40} \n{url_show} \n{hometext}".format(**news))
                    filetitle = keyword+"_cnBeta.txt"
                    filename = os.path.join( fpath, filetitle )
            
                    f = open(filename, 'a')
                    f.writelines('title：' + "{title:<40}".format(**news) + '\r\n')
                    f.writelines('time：' + "{inputtime}".format(**news) + '\r\n')
                    f.writelines('summ：' + "{hometext}".format(**news) + '\r\n')
                    f.writelines('\r\n')
                    f.close()        
        return end
            

    def process_cnBeta(self,fpath,days,keyword_list):

        ##    keyword_list = ['AI','自动驾驶']
##         = '/home/kai/05_newsupdate/99_reference/CnbetaNewsSpider-master/99_draft/'
##         = ['AI','人工智能','机器学习','深度学习','自然语言处理','NLP','机器视觉','物联网','NB-IoT','智能硬件','机器人','智能家居','智能音箱','amazon','apple','google','区块链','车联网','自动驾驶','5G','工业互联网','机器智能']
        
        
##        n = 1
        homepage_res =  spider.get_resource(self, HOMEPAGE_URL, HEADERS)
        csrf = spider.get_csrf(self, homepage_res)

        for kword in keyword_list:
            
            filetitle = kword+"_cnBeta.txt"
            filename = os.path.join( fpath, filetitle )
            if(os.path.exists(filename)):
                os.system("rm %s" % filename)
               ## print("remove check point 1")
            f = open(filename, 'a')
     #       f.writelines('*********************************************\n')
            f.writelines('*********************************************\r\n')
            f.writelines('keyword：' + kword + '\r\n')
            f.writelines('*********************************************\r\n')
            f.writelines('\r\n')
     #       f.writelines('*********************************************\n')
            f.close()

##        days = int(days)
        page = 1
        end = False
        while not end:
            json_url = spider.get_json_url(self, csrf, page)
            json_res = spider.get_resource(self, json_url, HEADERS)
            news_data = json_res.json()
     #       print("newss_data check",news_data)
            end = spider.print_news(self, news_data, days,keyword_list,fpath)
            page = page + 1


class cnBeta_Daemon:
    def __init__(self, pidfile='/tmp/daemon-example.pid', stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        if os.path.exists(self.pidfile):
            raise RuntimeError('Already running.')

        # First fork (detaches from parent)
        try:
            if os.fork() > 0:
                raise SystemExit(0)
        except OSError as e:
            raise RuntimeError('fork #1 faild: {0} ({1})\n'.format(e.errno, e.strerror))

##        print("check daemonize 1")

        os.chdir('/')
        os.setsid()
        os.umask(0o22)
##        print("check daemonize 2")
        # Second fork (relinquish session leadership)
        try:
            if os.fork() > 0:
                raise SystemExit(0)
        except OSError as e:
            raise RuntimeError('fork #2 faild: {0} ({1})\n'.format(e.errno, e.strerror))
##        print("check daemonize 3")
        # Flush I/O buffers
        sys.stdout.flush()
        sys.stderr.flush()
##        print("check daemonize 4")
        # Replace file descriptors for stdin, stdout, and stderr
        with open(self.stdin, 'rb', 0) as f:
##            print("check daemonize 4.1")
##            print("check daemonize 4.1:",f.fileno())
##            print("check daemonize 4.1:",sys.stdin.fileno())
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open(self.stdout, 'ab', 0) as f:
##            print("check daemonize 4.2")
##            print("check daemonize 4.2:",f.fileno())
##            print("check daemonize 4.2:",sys.stdout.fileno())
            
            os.dup2(f.fileno(), sys.stdout.fileno())
            
        with open(self.stderr, 'ab', 0) as f:
##            print("check daemonize 4.3")
            os.dup2(f.fileno(), sys.stderr.fileno())
##        print("check daemonize 5")
        # Write the PID file
        with open(self.pidfile, 'w') as f:
            print(os.getpid(), f)
#           print(os.getpid(), file=f)
##        print("check daemonize 6")
        # Arrange to have the PID file removed on exit/signal
        atexit.register(lambda: os.remove(self.pidfile))
##        print("check daemonize 7")
        signal.signal(signal.SIGTERM, self.__sigterm_handler)
##        print("check daemonize 8")
    # Signal handler for termination (required)
    @staticmethod
    def __sigterm_handler(signo, frame):
        raise SystemExit(1)

    def start(self):
        try:
##            print("check daemon start 1")
            self.daemonize()
        except RuntimeError as e:
            print(e, sys.stderr)
#            print(e, file=sys.stderr)
            raise SystemExit(1)

        self.run()

    def stop(self):
        try:
            if os.path.exists(self.pidfile):
                with open(self.pidfile) as f:
                    os.kill(int(f.read()), signal.SIGTERM)
            else:
                print('Not running.', sys.stderr)
#                print('Not running.', file=sys.stderr)
                raise SystemExit(1)
        except OSError as e:
            if 'No such process' in str(e) and os.path.exists(self.pidfile): 
                os.remove(self.pidfile)

    def restart(self):
        self.stop()
        self.start()

    def run(self,n,keyword_list):
        pass

