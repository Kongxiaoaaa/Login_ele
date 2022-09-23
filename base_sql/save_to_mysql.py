# -*- coding: utf-8 -*-
# Author: kong-an
# Date: 15:55
# FileNames: save_to_mysql.py
import pymysql


def get_conn():
    '''启动数据'''
    db = pymysql.connect(
            host='localhost',
            user='root',        # 账号
            password='',        # 密码
            database='',        # 数据库
            charset='utf8'      # 编码
            )
    return db

def data_to_mysql(datas, conn=get_conn()):
    """
    =>写入数据库<=
    | 启动数据库
    | 创建游标
    | 写入数据库
    | 执行操作
    | 关闭游标连接
    """
    def insert(cur, sql, args):
        # 插入数据
        try:
            cur.execute(sql, args)
        except Exception as e:
            print(e)
    
    # TODO: 使用上下文管理器，自动关闭数据库
    with get_conn() as conn:
        with conn.cursor() as cur:
            for k, v in datas.items():
                args = (k, v)
                sql = 'insert into ele_data(house,money) values(%s,%s)'
                insert(cur, sql=sql, args=args)
                conn.commit()
