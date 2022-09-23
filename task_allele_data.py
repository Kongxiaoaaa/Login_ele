# -*- coding: utf-8 -*-
# Author: kong-an
# Date: 2:49
# FileNames: login_cookie_ele.py
import json
import time
from random import randint
from re import findall

from ddddocr import DdddOcr
from requests import Response, session

from base_sql.save_to_mysql import data_to_mysql

__all__ = 'get_cookies, parser_mian'
session = session()
HOST: str = '' # 在此填入HOST地址(例如: 192.168.13.14)
user: str = '' # 账号
pwd: str = '' # 密码


def get_cookies() -> tuple[str, dict]:
    """
    Login to get cookies
    :return cookie, balance
    """
    # TODO: 验证码
    code_url: str = f'http://{HOST}/zytk35portal/AuthCode.aspx'
    # TODO: 主页面
    main_url: str = f'http://{HOST}/zytk35portal/Cardholder/Cardholder.aspx?sAccNum=30674'
    # TODO: 请求头
    header: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1"
    }  # 构造验证码请求头

    def login_post() -> tuple[dict, Response]:
        # TODO: 1.请求验证码
        img_resp = session.get(code_url, headers=header)
        # TODO: 2.识别验证码
        img_code: str = DdddOcr(show_ad=False).classification(img_resp.content)
        # TODO: 3.存储Cookies
        cook: dict = img_resp.cookies.get_dict()  # 存取cookies
        # TODO: 4.构造登录参数(user, pwd, img_code)
        login_url: str = f'http://{HOST}/zytk35portal/default.aspx'
        data: str = f'__LASTFOCUS=&__EVENTTARGET=UserLogin%24ImageButton1&' \
                    f'__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKMTc0MDQ4ODc3N' \
                    f'w9kFgICAQ9kFhICAw8WAh4HVmlzaWJsZWhkAgUPFgIfAGhkAgcPF' \
                    f'gIfAGhkAgkPPCsACQEADxYEHghEYXRhS2V5cxYAHgtfIUl0ZW1Db' \
                    f'3VudGZkZAIODzwrAAkBAA8WBB8BFgAfAmZkZAIQDzwrAAkBAA8WB' \
                    f'B8BFgAfAmZkZAISDzwrAAkBAA8WBB8BFgAfAmZkZAIUDzwrAAkBA' \
                    f'A8WBB8BFgAfAmZkZAIWDzwrAAkBAA8WBB8BFgAfAmZkZGT7t2PaA' \
                    f'C71nhjomcWWlS2Kl%2FDh6Icnffmmf1QCBjcqOg%3D%3D&__VIEW' \
                    f'STATEGENERATOR=E655DDB2&__EVENTVALIDATION=%2FwEdAAmm' \
                    f'kB23XPRc6QJjrAxJx7jUohjo8sIky4Xs%2BCUBsum%2BnL6pRh%2' \
                    f'FvC3eYiguVzFy%2FtEYvT53BE9ULYNj8jfQiCQeC35ZbbeGbJddo' \
                    f'wj1pY7sNivrI0G85IvfKPX4CghIMZ1NJ4PbCb80KUDHFYYKXgFT9' \
                    f'PjMyUg6NAZP4%2BvrIPkQUuFOdcKl43UA3HbIoQpEPelhEPm0OSq' \
                    f'wYeIaEyD7zfAzjHEWZ1PjzcAqdQtFUyg1jBg%3D%3D&UserLogin' \
                    f'%3AtxtUser={user}&UserLogin%3AtxtPwd={pwd}&Us' \
                    f'erLogin%3AddlPerson=%BF%A8%BB%A7&UserLogin%3AtxtSure='  # 请求页面的参数
        login_resp = session.post(url=login_url, headers=header, data=f"{data}{img_code} ")
        login_resp.encoding = 'gb2312'  # 格式编码
        assert login_resp.status_code == 200, print('状态码出错了')  # 访问失败抛出异常
        assert findall('<span>(.*?)</span>', login_resp.text)[0] != '你好，游客', login_post()  # 多次尝试
        return cook, login_resp  # cookies和返回响应
    
    try:
        cookie: dict = login_post()[0]  # 获取Cookies
        main_page_resp = session.post(url=main_url, headers=header)  # 获取主页面
        balance: list = findall('<span id="lblOne0">(.*?)</span>', main_page_resp.text)  # 获取余额
        if len(balance):
            balance: str = balance[0]
            return balance, cookie  # 金额 和 cookie
        else:
            print(f'金额页面出错: 重试{login_post()}')
    except AssertionError:
        print("访问页面失败,可能无法链接到网页!!!")


def parser_mian(ban_cook=get_cookies()):
    balance: str = ban_cook[0]  # 金额
    lou_head: dict = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Referer': f'http://{HOST}/zytk35portal/Cardholder/Cardholder.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'}
    # TODO: 获取电费主页面(获取楼栋代码)
    lou_resp = session.get(f'http://{HOST}/zytk35portal/Cardholder/SelfHelp.aspx', headers=lou_head, verify=False)
    assert lou_resp.status_code == 200, parser_mian()
    dorm: list = findall('<option value="(\d+)">(.*?)号楼</option>', lou_resp.text)
    assert len(dorm) != 0, parser_mian()
    for dorm_num in dorm:
        try:
            print(dorm_num[0])
            # TODO: 请求楼栋
            lc = session.post(f'http://{HOST}/zytk35portal/ajaxpro/Zytk30Portal.Cardholder.SelfHelp,'
                              'App_Web_selfhelp.aspx.67bdbcc7.ashx',
                              headers={
                                  'X-AjaxPro-Method': 'GetHouseList',
                                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'},
                              data=json.dumps({'AreaId': dorm_num[0]}))
            lc.encoding = 'utf-8'
            data = findall(r'(\["\d+",".*?"])', lc.text)  # TODO: 楼层信息
            if not data:  # 列表没有元素
                raise print('出错了哎!')
            else:  # 列表有元素
                info = {}  # TODO: 收集数据
                house_nums = (findall('\d+', num)[0] for num in data)
                for house in house_nums:
                    house_info = session.post(
                        f'http://{HOST}/zytk35portal/ajaxpro/Zytk30Portal.Cardholder.SelfHelp,'
                        'App_Web_selfhelp.aspx.67bdbcc7.ashx',
                        headers={
                            'X-AjaxPro-Method': 'GetRoomList',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'},
                        data=json.dumps({"areaId": dorm_num[0], "HouseId": house}))
                    house_info.encoding = 'utf-8'
                    for dor in findall(r'(\[\d+,.*,".*",".*"])', house_info.text)[0].replace('][', '').split('],['):
                        dor_list = dor.split(',')
                        info.update(
                            {dor_list[2].replace('"', ''): dor_list[1] + '元'})  # 获取金额并添加当前时间
                    print(f'已经Send All DATA: {dorm_num[0]} <我休息一下>', time.sleep(randint(1, 3)))
                print(f'已经跑完一栋楼了,我休息一下', time.sleep(5))
                data_to_mysql(datas=info)
                del info  # TODO: 清空数据库
        except Exception as e:
            print(e)
    session.close()


if __name__ == '__main__':
    parser_mian()
