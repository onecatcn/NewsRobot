#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
#python2.7x  
#send_simple_email_by_account.py  @2014-07-30  
#author: orangleliu  
  
''''' 
使用python写邮件 simple 
使用chinamobile 的邮箱服务 
'''  
  
import smtplib  
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
import base64
import time  # 引入time模块
import string
import os
import subprocess

def merge_txt(keyword_list,fpath,date):
    filetitle = 'cnBeta_'+date+'.txt'
    file=open(fpath+filetitle,'w')

    for kword in keyword_list:
        keyword = kword
        s = keyword+'_cnBeta.txt'
        newDir = os.path.join( fpath, s )
        if os.path.isfile(newDir) :         #如果是文件
            if os.path.splitext(newDir)[1]==".txt":  #判断是否是txt
               for line in open(newDir):
                   file.writelines(line)    
                   file.write('\r\n')
    #关闭文件 
    file.close()
    a = "sed -i 's/<[^>]*>//g' "+fpath+filetitle
    os.system(a)
    return filetitle
 

def remove_txt(keyword_list,fpath,date):
    filetitle = 'cnBeta_'+date+'.txt'
    filename = os.path.join( fpath, filetitle )
    ## try to delete file ##
    try:
        os.remove(filename)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename,e.strerror))

    for kword in keyword_list:
        keyword = kword
        filetitle = keyword+'_cnBeta.txt'
        filename = os.path.join( fpath, filetitle )
        print('try to delete',filename)
        ## try to delete file ##
        try:
            os.remove(filename)
        except OSError as e:  ## if failed, report it back to the user ##
            print ("Error: %s - %s." % (e.filename,e.strerror))
    print ("deleted files on disk")

def auto_email(emaillist,keyword_list,fpath,date):
    SMTPserver = 'hqsmtp.chinamobile.com'  
    sender = 'wangkaiwx@chinamobile.com'  
    password = "beijing201807"
##    destination = "kaiwang85@foxmail.com,onecat@163.com,wangkaiwx@chinamobile.com"
##    destination = "kaiwang85@foxmail.com,onecat@163.com,fanxiaohui@chinamobile.com,sunlin@@chinamobile.com"
    destination = str.split(emaillist, ",")

    mailserver = smtplib.SMTP(SMTPserver, 25)  
    mailserver.login(sender, password)

    #创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("NewsRobot", 'utf-8')
    message['To'] =  Header("Clients", 'utf-8')
    subject = 'IoT行业新闻update:'+date
    message['Subject'] = Header(subject, 'utf-8')
     
    #邮件正文内容
    message.attach(MIMEText('这是NewsRobot邮件发送测试……', 'plain', 'utf-8'))
     
    # 构造附件1，传送当前目录下的 test.txt 文件
    # count = 1
    filetitle = merge_txt(keyword_list,fpath,date)
    attachname = os.path.join( fpath, filetitle )

    try:
        attachname = os.path.join( fpath, filetitle )
##                print("check attachname",attachname)
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachname, "rb").read())
        part.add_header('Content-Disposition', 'attachment' ,filename=filetitle)
        encoders.encode_base64(part)
##                print("part check",part)
        message.attach(part)
    except:
        print ("could not attache file")
    
##    att = MIMEBase('application', 'octet-stream')
##    att.set_payload(open(attachname, 'rb').read())
##    att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', attachname) )
##    encoders.encode_base64(att)

##    att = MIMEText(open(attachname, 'rb').read(), 'base64', 'UTF-8')
##    att["Content-Type"] = 'application/octet-stream'
##    att.add_header('Content-Disposition', 'attachment', filename= '=?utf-8?b?' + base64.b64encode(filetitle.encode('UTF-8')) + '?=')
##    message.attach(att)

    sent_note=0
    while(not sent_note):
        try:
            mailserver.sendmail(sender, destination, message.as_string())  
            mailserver.quit()  
            print('send email success')
            remove_txt(keyword_list,fpath,date)
            sent_note = 1
        except:   
        ##except smtplib.SMTPException:
            print("Error: 无法发送邮件")
            time.sleep(10)
            continue

    
