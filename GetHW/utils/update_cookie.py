import requests
import hashlib

def get_cookie(student_id):
        BASE_URL = 'http://123.121.147.7:88/ve'
        session = requests.session()
        # 先读一次主页
        session.get(BASE_URL + '/')

        # 获取验证码
        session.get(BASE_URL + '/GetImg')
        resp = session.get(BASE_URL + '/confirmImg')
        passcode = resp.content.decode()

        # 输入学号
        student_id = student_id if student_id is not None else input('请输入学号: ')

        # 输入密码
        password = hashlib.md5(f"Bjtu@{student_id}".encode()).hexdigest()

        # 登录
        resp = session.post(BASE_URL + '/s.shtml', data={
            'login': 'main_2',
            'qxkt_type': '',
            'qxkt_url': '',
            'username': student_id,
            'password': password,
            'passcode': passcode
        }, allow_redirects=True)

        if not 200 <= resp.status_code < 300 or resp.content.decode(resp.encoding or 'utf-8').find('alert(') != -1:
            raise Exception('Failed logging in.')

        return session.cookies.get_dict()['JSESSIONID']