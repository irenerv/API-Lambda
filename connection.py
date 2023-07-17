import os
import pymysql.cursors

endpoint = os.environ.get('ENDPOINT')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')


def connectDB():
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    return connection