#! /usr/bin/env python
# -*- coding: utf-8 -*-
import commands, os, sys

reload(sys)
sys.setdefaultencoding('utf8')


class GitTools(object):

    def reset(self, path, commintId):
        cmd = "cd {path} && git reset --hard {commintId}".format(path=path, commintId=commintId)
        return commands.getstatusoutput(cmd)

    def log(self, path, bName=None, number=None):
        vList = []
        if bName:
            cmd = "cd {path} && git log {bName} --pretty=format:'%h|%s|%cn|%ci|%H' -n {number}".format(path=path,
                                                                                                       bName=bName,
                                                                                                       number=number)
        else:
            cmd = "cd {path} && git log --pretty=format:'%h|%s|%cn|%ci|%H' -n {number}".format(path=path, number=number)
        status, result = commands.getstatusoutput(cmd)
        if status == 0:
            for log in result.split('\n'):
                log = log.split('|')
                data = dict()
                data['ver'] = log[0]
                data['desc'] = log[1]
                data['user'] = log[2]
                data['comid'] = log[4]
                vList.append(data)
        return vList

    def init(self, path):
        cmd = "cd {path} && git init".format(path=path)
        return commands.getstatusoutput(cmd)

    def branch(self, path):
        '''获取分支列表'''
        bList = []
        cmd = "cd {path} && git branch".format(path=path)
        status, result = commands.getstatusoutput(cmd)
        if status == 0:
            for ds in result.split('\n'):
                if len(ds) == 0: continue
                data = dict()
                if ds.find('*') >= 0:
                    data['status'] = 1
                else:
                    data['status'] = 0
                data['name'] = ds.replace('* ', '').strip()
                data['value'] = ds.replace('* ', '').strip()
                bList.append(data)
        return bList

    def createBranch(self, path, branchName):
        cmd = "cd {path} && git checkout -b {branchName} origin/{branchName}".format(path=path, branchName=branchName)
        return commands.getstatusoutput(cmd)

    def delBranch(self, path, branchName):
        cmd = "cd {path} && git branch -d {branchName}".format(path=path, branchName=branchName)
        return commands.getstatusoutput(cmd)

    def tag(self, path):
        tagList = []
        cmd = "cd {path} && git tag".format(path=path)
        status, result = commands.getstatusoutput(cmd)
        if status == 0:
            for ds in result.split('\n'):
                if len(ds) == 0: continue
                data = dict()
                if ds.find('*') >= 0:
                    data['status'] = 1
                else:
                    data['status'] = 0
                data['name'] = ds.replace('* ', '').strip()
                data['value'] = ds.strip()
                tagList.append(data)
        return tagList

    def createTag(self, path, tagName):
        cmd = "cd {path} && git tag {tagName}".format(path=path, tagName=tagName)
        return commands.getstatusoutput(cmd)

    def delTag(self, path, tagName):
        cmd = "cd {path} && git tag -d {tagName}".format(path=path, tagName=tagName)
        return commands.getstatusoutput(cmd)

    def checkOut(self, path, name):
        cmd = "cd {path} && git checkout {name}".format(path=path, name=name)
        return commands.getstatusoutput(cmd)

    def clone(self, url, dir, user=None, passwd=None):
        cmd = "git clone {url} {dir}".format(url=url, dir=dir)
        return commands.getstatusoutput(cmd)

    def pull(self, path):
        cmd = "cd {path} && git pull".format(path=path)
        return commands.getstatusoutput(cmd)

    def mkdir(self, dir):
        if os.path.exists(dir) is False: os.makedirs(dir)

    def show(self, path, branch, cid):
        cmd = "cd {path} && git checkout {branch}".format(path=path, branch=branch)
        result = commands.getstatusoutput(cmd)
        if result[0] == 0 and cid:
            cmd = "cd {path} &&  git show {cid}".format(path=path, cid=cid)
            result = commands.getstatusoutput(cmd)
        return result


class SvnTools(object):

    def reset(self, path, commintId):
        cmd = "cd {path} && svn update -r {commintId}".format(path=path, commintId=commintId)
        return commands.getstatusoutput(cmd)

    def log(self, path, number=None):
        vList = []
        cmd = "cd {path} && svn log -l {number} -q".format(path=path, number=number)
        status, result = commands.getstatusoutput(cmd)
        if status == 0:
            for log in result.split('\n'):
                if log.startswith('---'): continue
                log = log.split('|')
                data = dict()
                data['ver'] = log[0].strip()
                data['user'] = log[1].strip()
                data['comid'] = log[0].strip()
                log = log[2].strip().split(' ', 2)
                ctime = log[0] + ' ' + log[1]
                data['desc'] = ctime
                vList.append(data)
        return vList

    def branch(self, path):
        '''获取分支列表'''
        return []

    def tag(self, path):
        '''获取分支列表'''
        return []

    def checkOut(self, path, name=None):
        cmd = "cd {path} && svn update".format(path=path)
        return commands.getstatusoutput(cmd)

    def clone(self, url, dir, user=None, passwd=None):
        if user and passwd:
            cmd = "svn co {url}  --username {user} --password {passwd} {dir}".format(url=url, user=user, passwd=passwd,
                                                                                     dir=dir)
        else:
            cmd = "svn co {url}  {dir}".format(url=url, dir=dir)
        return commands.getstatusoutput(cmd)

    def pull(self, path):
        cmd = "cd {path} && svn update".format(path=path)
        return commands.getstatusoutput(cmd)

    def show(self, path, cid, branch=None):
        cmd = "cd {path} && svn update && svn diff -r {cid}".format(path=path, cid=cid)
        return commands.getstatusoutput(cmd)

    def mkdir(self, dir):
        if os.path.exists(dir) is False: os.makedirs(dir)


# !/usr/bin/env python
# _#_ coding:utf-8 _*_
'''版本控制方法'''
# import magic
from random import choice
import string, hashlib, calendar
import commands, os, time, smtplib
from datetime import datetime, timedelta, date
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import logging
logger = logging.getLogger('django.base')



def file_iterator(file_name, chunk_size=512):
    f = open(file_name, "rb")
    while True:
        c = f.read(chunk_size)
        if c:
            yield c
        else:
            break
    f.close()


def sendEmail(e_from, e_to, e_host, e_passwd, e_sub="It's a test email.", e_content="test", cc_to=None,
              attachFile=None):
    msg = MIMEMultipart()
    EmailContent = MIMEText(e_content, _subtype='html', _charset='utf-8')
    msg['Subject'] = "%s " % e_sub
    msg['From'] = e_from
    if e_to.find(',') == -1:
        msg['To'] = e_to
    else:
        e_to = e_to.split(',')
        msg['To'] = ';'.join(e_to)
    if cc_to:
        if cc_to.find(',') == -1:
            msg['Cc'] = cc_to
        else:
            cc_to = cc_to.split(',')
            msg['Cc'] = ';'.join(cc_to)
    msg['date'] = time.strftime('%Y %H:%M:%S %z')
    try:
        if attachFile:
            EmailContent = MIMEApplication(open(attachFile, 'rb').read())
            EmailContent["Content-Type"] = 'application/octet-stream'
            fileName = os.path.basename(attachFile)
            EmailContent["Content-Disposition"] = 'attachment; filename="%s"' % fileName
        msg.attach(EmailContent)
        smtp = smtplib.SMTP()
        smtp.connect(e_host)
        smtp.login(e_from, e_passwd)
        smtp.sendmail(e_from, e_to, msg.as_string())
        smtp.quit()
    except Exception, e:
        print e


def radString(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


def rsync(sourceDir, destDir, exclude=None):
    if exclude:
        cmd = "rsync -au --delete {exclude} {sourceDir} {destDir}".format(sourceDir=sourceDir, destDir=destDir,
                                                                          exclude=exclude)
    else:
        cmd = "rsync -au --delete {sourceDir} {destDir}".format(sourceDir=sourceDir, destDir=destDir)
    return commands.getstatusoutput(cmd)


def mkdir(dirPath):
    mkDir = "mkdir -p {dirPath}".format(dirPath=dirPath)
    return commands.getstatusoutput(mkDir)


def cd(localDir):
    os.chdir(localDir)


def pwd():
    return os.getcwd()


def cmds(cmds):
    return commands.getstatusoutput(cmds)


def chown(user, path):
    cmd = "chown -R {user}:{user} {path}".format(user=user, path=path)
    return commands.getstatusoutput(cmd)


def makeToken(strs):
    m = hashlib.md5()
    m.update(strs)
    return m.hexdigest()


def lns(spath, dpath):
    if spath and dpath:
        rmLn = "rm -rf {dpath}".format(dpath=dpath)
        status, result = commands.getstatusoutput(rmLn)
        mkLn = "ln -s {spath} {dpath}".format(spath=spath, dpath=dpath)
        return commands.getstatusoutput(mkLn)
    else:
        return (1, "缺少路径")


def getDaysAgo(num):
    threeDayAgo = (datetime.now() - timedelta(days=num))
    timeStamp = int(time.mktime(threeDayAgo.timetuple()))
    otherStyleTime = threeDayAgo.strftime("%Y%m%d")
    return otherStyleTime


def getSQLAdvisor(host, port, user, passwd, dbname, sql):
    cmd = """/usr/bin/sqladvisor -h {host}  -P {port}  -u {user} -p '{passwd}' -d {dbname} -q '{sql}' -v 1""".format(
        host=host, port=port, user=user, passwd=passwd, dbname=dbname, sql=sql)
    return commands.getstatusoutput(cmd)


def getDayAfter(num, ft=None):
    # 获取今天多少天以后的日期
    if ft:
        return time.strftime(ft, time.localtime(time.time() + (num * 86400)))
    else:
        return time.strftime('%Y-%m-%d', time.localtime(time.time() + (num * 86400)))


def calcDays(startDate, endDate):
    # 对比两个日期的时间差
    startDate = time.strptime(startDate, "%Y-%m-%d %H:%M:%S")
    endDate = time.strptime(endDate, "%Y-%m-%d %H:%M:%S")
    startDate = datetime(startDate[0], startDate[1], startDate[2], startDate[3], startDate[4], startDate[5])
    endDate = datetime(endDate[0], endDate[1], endDate[2], endDate[3], endDate[4], endDate[5])
    return (endDate - startDate).days


def getMonthFirstDayAndLastDay(year=None, month=None):
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year
    if month:
        month = int(month)
    else:
        month = datetime.date.today().month
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)
    firstDay = date(year=year, month=month, day=1)
    lastDay = date(year=year, month=month, day=monthRange)
    return firstDay, lastDay

# def getFileType(filePath):
#     try:
#         files = magic.Magic(uncompress=True,mime=True)
#         file_type = files.from_file(filePath)
#     except Exception,ex:
#         file_type = '未知'
#         logger.error("获取文件类型失败: {ex}".format(ex=ex))
#     return file_type
