# coding:utf-8
import requests, time
from bs4 import BeautifulSoup
import sys
import re
import json

reload(sys)
sys.setdefaultencoding('utf-8')


class music163(object):
    headers = {
        # 'Pragma': 'no-cache',
        # 'DNT': '1',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.30 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection' : 'keep-alive',
        'Origin': 'http://music.163.com',
        'Referer': 'http://music.163.com/weapi/login/?csrf_token=1e64b3f77456a8c20dc50a3c0578ee3b',
        # 删除了此处的host 和上面的两个参数
    }

    def login(self):
        sess = requests.Session()
        # 网易云音乐这部分是由ajax生成的
        # LoginHtml = sess.get('http://www.v2ex.com/signin', headers=self.headers)
        # LoginSoup = BeautifulSoup(LoginHtml.text, 'lxml')
        # usrnamecode = LoginSoup.find('input', {'class': 'sl'})['name']
        # usrpswdcode = LoginSoup.find('input', {'type': 'password'})['name']
        # once = LoginSoup.find('input', {'name': 'once'})['value']
        form_data = {
            'params': 'H1+fyr6kyKKtKq89Kkys/UgSjhfK9dgLlQqiKrlKN//Sbn25x9Gr+vZCgk3rBhy4cdVYdQFKC76gif2Es6+RDPfi9UaBXgsPkn6YAj0un9PcDTNRrg8yODifJXJIItJQ885Kkm0vFPn2/WwsKhOEUcs0Cd+hAgf1+/EASc4dS/c4ygwzzb0F/yop25Ul5/0NbtFvmfDSrbDuV/ANLirBSIDDX6njlX/hKXhkQMhUc9olTiJdGD/oTFU17aOhAUret6S3AzzG5j0mascU8msG/652un8WGvf5ycwYndQsAYY=',
            'encSecKey': '7bc9f3082eb0e361a65581c77274f8633fde36fb70e9065935515e996388872cda9ecca224670cff297a1528c204863345ec9b693ac81852335fdf14ba094e3ce3253300bb1a2c72f55c1728986aaf94cbf6867e19aadad786ab6ced4c147b397b8ed07d3a032f5f6cf1a47e149ecf868cd1a41fd153192e58666ec198b34622',
            }
        rep = sess.post('http://music.163.com/weapi/login/?csrf_token=1e64b3f77456a8c20dc50a3c0578ee3b', form_data, headers=self.headers)
        print rep.text
        resultsJson = json.loads(rep.text)
        status = True if resultsJson['code'] == 200 else False
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
        with open(self.usrname+'music163Log.txt', 'a') as log:
            log.write(time.ctime())
            log.write(des+'\n')
            log.write('*'*30)
            print '写入日志成功...'

    def daily(self, sess):
        RealUrl = 'http://music.163.com/weapi/point/dailyTask?csrf_token=07bb5bae367c1eb46fc1827e8daec904'
        form_data = {
            'params': '8bQOYs8a9P35tD0jGp1AgquvIGsI+ThXPkbOumUU0KdwoWQ1Q6ZFsEBK9pNTSyXz9w0xz5A5urIkW20d2GKvTjx7Ibby2NMryKatJas8K0RjkqoJ4PbuyjPg08VMxODk',
            'encSecKey': 'd2453608fbabc402782b79eaf2a048be7b0c4d18f58d830fdf238433819813ece641628e46367dd77e3e928d0ecb4a253efd02c1125be264f3cb381f38566fd37239bd8f84fdaaaf05abb2bae90b4f916cad284c874e0f2465c8f89424f03c56957abc12c7fb473f1cfffc8a4af2dde752e0d83cdebaa9a25c26511c7a57d0d0',
            }
        rep = sess.post(RealUrl, form_data, headers={'Referer': 'http://music.163.com/weapi/point/dailyTask?csrf_token=07bb5bae367c1eb46fc1827e8daec904'})
        print rep.text
        resultsJson = json.loads(rep.text)
        status = True if resultsJson['code'] == 200 else False
        if status:
            print '已成功领取每日登录奖励...'
            des = '已获得' + resultsJson['point'] + '点'
            self.writelog(des)
        else:
            print resultsJson['msg'] + '已经领取过每日登录奖励...'

if __name__ == '__main__':
    try:
        while True:
            foo = music163()
            sess = foo.login()
            if sess[1] is True:
                foo.daily(sess[0])
            time.sleep(86400)
    except:
        print '登录失败...'
        print sys.exc_info()

# 每个脚本及其建立一个文件夹 日志放在其内
# 搞一个360签到的