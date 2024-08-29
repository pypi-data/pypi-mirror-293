# -*- coding: UTF-8 –*-
from mdbq.mysql import mysql
from mdbq.config import get_myconf
"""
对指定数据库所有冗余数据进行清理
"""


def op_data(db_name_lists, service_databases=None, days: int = 63):
    """ service_databases 这个参数暂时没有用 """
    # for service_database in service_databases:
    #     for service_name, database in service_database.items():
    #         username, password, host, port = get_myconf.select_config_values(target_service=service_name, database=database)
    #         s = mysql.OptimizeDatas(username=username, password=password, host=host, port=port)
    #         s.db_name_lists = [
    #             '聚合数据',
    #         ]
    #         s.days = days
    #         s.optimize_list()

    if socket.gethostname() == 'xigua_lx' or socket.gethostname() == 'xigua1' or socket.gethostname() == 'Mac2.local':
        # mongodb
        username, password, host, port = get_myconf.select_config_values(
            target_service='home_lx',
            database='mongodb',
        )
        m = mongo.OptimizeDatas(username=username, password=password, host=host, port=port)
        m.db_name_lists = db_name_lists
        m.days = days
        m.optimize_list()
        if m.client:
            m.client.close()
            print(f'已关闭 mongodb 连接')

        if socket.gethostname() == 'xigua_lx':
            restart_mongodb()  # mongodb 太占内存了, 重启服务， 释放内存

        # Mysql
        username, password, host, port = get_myconf.select_config_values(
            target_service='home_lx',
            database='mysql',
        )
        s = mysql.OptimizeDatas(username=username, password=password, host=host, port=port)
        s.db_name_lists = db_name_lists
        s.days = days
        s.optimize_list()

    elif socket.gethostname() == 'company':
        # Mysql
        username, password, host, port = get_myconf.select_config_values(
            target_service='company',
            database='mysql',
        )
        s = mysql.OptimizeDatas(username=username, password=password, host=host, port=port)
        s.db_name_lists = db_name_lists
        s.days = days
        s.optimize_list()


if __name__ == '__main__':
    op_data(service_databases=[{'home_lx': 'mysql'}], days=3650)
