# coding:utf-8
import requests, time
from bs4 import BeautifulSoup
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


class v2ex(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Origin': 'http://www.v2ex.com',
        'Referer': 'http://www.v2ex.com/signin',
        'Host': 'www.v2ex.com'
    }

    def __init__(self, usrname, usrpswd):
        self.usrname = usrname
        self.usrpswd = usrpswd

    def login(self):
        sess = requests.Session()
        LoginHtml = sess.get('http://www.v2ex.com/signin', headers=self.headers)
        LoginSoup = BeautifulSoup(LoginHtml.text, 'lxml')
        usrnamecode = LoginSoup.find('input', {'class': 'sl'})['name']
        usrpswdcode = LoginSoup.find('input', {'type': 'password'})['name']
        once = LoginSoup.find('input', {'name': 'once'})['value']
        form_data = {
            usrnamecode: self.usrname,
            usrpswdcode: self.usrpswd,
            'once': once,
            'next': '/'
            }
        sess.post('http://www.v2ex.com/signin', form_data, headers=self.headers)
        sethtml = sess.get('http://www.v2ex.com/settings', headers=self.headers)
        soup = BeautifulSoup(sethtml.text, 'lxml')
        email = soup.find('input', {'type': 'email'})['value']
        status = True if email else False
        print '登录成功！' if status else '登录失败！'
        return [sess, status]

    def balance(self, sess):
        '''
        :param sess: 登录状态
        :return: 获取签到奖励和余额
        '''
        BalanceHtml = sess.get('http://www.v2ex.com/balance',headers={'Referer': 'http://www.v2ex.com/balance'}).text
        dailygold = re.findall(u'>(\d+.+的每日.+)</span', BalanceHtml)[0]
        return dailygold

    def writelog(self, des):
        with open(self.usrname+'v2exLog.txt', 'a') as log:
            log.write(time.ctime())
            log.write(des+'\n')
            log.write('*'*30)
            print '写入日志成功...'

    def daily(self, sess):
        DailyUrl = 'http://www.v2ex.com/mission/daily'
        html = sess.get(DailyUrl, headers=self.headers)
        MSoup = BeautifulSoup(html.text, 'lxml')
        u = MSoup.find('input', {"type": 'button'})['onclick'].split('\'')[1]
        RealUrl = 'http://www.v2ex.com' + u
        res = sess.get(RealUrl, headers={'Referer': 'http://www.v2ex.com/mission/daily'})
        des = self.balance(sess)
        print des
        if res.text.find(u'已成功领取每日登录奖励') > 0:
            print '已成功领取每日登录奖励...'
            self.writelog(des)
        else:
            print '已经领取过每日登录奖励...'

if __name__ == '__main__':
    usrname = raw_input('用户名: ')
    usrpswd = raw_input('密码: ')
    try:
        foo = v2ex(usrname, usrpswd)
        foo.writelog('des')
        sess = foo.login()
        if sess[1] is True:
            foo.daily(sess[0])
    except:
        print '登录失败...'
        print sys.exc_info()
