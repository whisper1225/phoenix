# coding:utf-8

import requests, time
from bs4 import BeautifulSoup
import sys
import json


reload(sys)
sys.setdefaultencoding('utf-8')

class chinaMobileSign(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Origin': 'http://api.ahmobile.cn',
        'Referer': 'http://api.ahmobile.cn:8081/eip?eip_serv_id=app.ssoLogin'
        # 'Host': 'http://api.ahmobile.cn'
    }

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        sess = requests.Session()
        # LoginHtml = sess.get("http://api.ahmobile.cn:8081/eip?eip_serv_id=app.ssoLogin", header = self.header)
        # LoginSoup = BeautifulSoup(LoginHtml.text, 'lxml')
        form_data = {
            'paramType': 1,
            'phone_token': '019d33ea3082300b307130c9383333003632373533',
            'imei': 'FIxnL9/CE4GHCeqA7szFN+/zMDDgSsUlpz2fPKj9ZJgJ9FtzyPo7ksg1cLR1928wZcBkGwh9vs9lUAufWDAQ3d3jWxtN4rsY+PTU3dzjdhqiBsGvLc1SqL7FV8UChBb6yiKJ8Lk9CV2FjgRQtQE6p4V09/Hv2v+zbbKTRoIvglI=',
            'imsi':'TaKGnrNG6VINezhs3IxFLtoqq6ElIvLkUx00pmYlo98YRSRwGJpwo20xi7AxDiSpUP01WuYDxzdozicCUE3jfBp6z41k22oc2F8iBmURqNiOm53i+ubB71/rq+XCtAnYvs05PFN2hzgWh9lISWFSlgfkuqibmGyDeMgAJ58bJGk=',
            'clientVersion': '3.5.4',
            'type': 0,
            'token': '599eba489329e32a7b45dd1a81d95e39',
            'userIn.phone_no': '18788864500',
            'userIn.userPasswd': 'nkQ34k09J7l72EeO6PTrgrkCwKhFAw+PQ8WjoPogRNdDwD33F+lfj/JzB05BOsXsnmb30k/6I/OAUwqPEBU7R91TYrkjxTfkcG8qgRcHQIZ+GpjlVOivK1AoE4KvReUJHt0v7Zle0IJ+13lAcZKHcNKqiSqvbbiviT8wDJamQgc='
        }
        rep = sess.post('http://api.ahmobile.cn:8081/eip?eip_serv_id=app.ssoLogin', form_data, headers=self.headers)
        resultsJson = json.loads(rep.text)
        status = True if resultsJson['result'] else False
        return [sess, status]

    def checkIn(self, sess):
        checkInUrl = 'http://api.ahmobile.cn:8081/eip?eip_serv_id=app.checkInIm'
        form_data = {
            'token': 'b07ece7306ead09f0ef5cd4a74a0d456',
            'ytnb': 'true'
        }
        rep = sess.post(checkInUrl, form_data, headers=self.headers)
        resultsJson = json.loads(rep.text)
        return result


if __name__ == '__main__':
    username = raw_input('username')
    userpswd = raw_input('userpwsd')
    try:
        foo = chinaMobileSign(username, userpswd)
        result = foo.login()
        if result[1] is True:
            checkResult = foo.checkIn(result[0])
            print checkResult
    except:
        print '登陆失败'
        print sys.exc_info()
