import pymysql

pymysql.install_as_MySQLdb()

import MySQLdb

# Si Django 6 te pide por ejemplo mysqlclient 2.3.0, actualiza estos números:
if hasattr(MySQLdb, 'version_info'):
    MySQLdb.version_info = (2, 2, 1, 'final', 0) # <--- Cambia esto si el error lo pide
    MySQLdb.__version__ = '2.2.1'                 # <--- Cambia esto si el error lo pide