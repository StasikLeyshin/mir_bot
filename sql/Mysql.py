# -*- coding: utf-8 -*-
#import nest_asyncio
#nest_asyncio.apply()
#from vkbottle import Bot, Message, PhotoUploader, DocUploader
#from aiohttp import web

import pymysql
from pymysql.cursors import DictCursor

from flask import Flask
app = Flask(__name__)




def pol_js(u1, u2=0, u3=0, u4=0, f=0):
	connection = pymysql.connect(
				host='127.0.0.1',
				user='ivan',
				password='0351',
				db='test5',
				port=3306)
	cursor = connection.cursor()
	#cursor.execute("SELECT * FROM guide")
	plus = "and campus LIKE 'moscow' and (level LIKE 'bach' or level LIKE 'spec')"
	#cursor.execute(f"SELECT * FROM test5 WHERE {u1} >= 1 and {u2} >= 1 and {u3} >= 1 and (last_year_min LIKE '—' or last_year_min <= {u4}) {plus}")
	cursor.execute(
		f"SELECT * FROM test5 WHERE {u1} >= 1 and {u2} >= 1 and {u3} >= 1 and (last_year_min <= {u4} and last_year_min NOT LIKE '—') {plus}")
	# if u4 != 0:
	# 	cursor.execute(f"SELECT * from test5 where {u1} in (1) and {u2} in (1) and {u3} in (1) and (last_year_min LIKE '—' or last_year_min <= {u4}) and campus LIKE 'moscow' and (level LIKE 'bach' or level LIKE 'spec')")
	# elif u3 != 0:
	# 	cursor.execute(f"SELECT * from test5 where {u1} in (1) and {u2} in (1) and (last_year_min LIKE '—' or last_year_min <= {u3}) and campus LIKE 'moscow' and (level LIKE 'bach' or level LIKE 'spec')")
	# elif u2 != 0:
	# 	cursor.execute(f"SELECT * from test5 where {u1} in (1) and (last_year_min LIKE '—' or last_year_min <= {u2}) and campus LIKE 'moscow' and (level LIKE 'bach' or level LIKE 'spec')")
	# #print(cursor)
	results = cursor.fetchall()
	#print(results)
	g = {}
	#try:
	g["quantity"] = len(results)
	if g["quantity"] == 0:
		cursor.execute(
			f"SELECT * FROM test5 WHERE {u1} >= 1 and {u2} >= 1 and {u3} >= 1 and (last_year_min <= 310 and last_year_min NOT LIKE '—') {plus}")
		results = cursor.fetchall()
		g["quantity"] = -1
	connection.close()
	g["programs"] = []
	if f == 1:
		for i in results:
			if i[10] != '—':
				g["programs"].append({"name": i[1], "code": i[2], "link": i[29], "bal": i[10], "places": i[7]})
			else:
				print({"name": i[1], "code": i[2], "link": i[29], "bal": i[10], "places": i[7]})

	#except Exception as e:
		#print(e)
	#print (result[2])
	#print(connection)
	return g



@app.route("/api/<u>", methods=['GET'])
def index(u):
	spis = u.split("&")
	h = 0
	if len(spis) == 4:
		bal = str(int(spis[3])-10)
		h = pol_js(spis[0], spis[1], spis[2], bal)
	elif len(spis) == 3:
		bal = str(int(spis[2])-10)
		h = pol_js(spis[0], spis[1], bal)
	elif len(spis) == 2:
		bal = str(int(spis[1])-10)
		h = pol_js(spis[0], bal)
	if h != 0 and h != {}:
		return h
	else:
		return "-1"

#if __name__ == "__main__":
	#app.run(host='0.0.0.0')
	#print(pol_js("rus", "info", "math", "230"))

'''async def executor(request: web.Request):
    #event = await request.json()
    print(request)
    return web.Response(text=emulation)

app = web.Application()

app.router.add_route(
    path='/api',
    method='GET',
    handler=executor
)'''
#web.run_app(app=app, host="127.0.0.1", port=8000)

'''app.router.add_route(
    path='/bot',
    method='POST',
    handler=executor1
)'''
#web.run_app(app=app, host="127.0.0.1", port=5000)





'''db = pymysql.connect(host="0.0.0.0",port=3306,user="mysql",passwd="mysql_pass_29")
cursor=db.cursor()
cursor.execute("guide_api")юю
results=cursor.fetchall()
for result in results:
    print (result)'''

'''import mysql.connector
import sshtunnel

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

with sshtunnel.SSHTunnelForwarder(
    ssh_address_or_host = ('212.109.221.219',59288),
    local_bind_address = ('localhost',3306),
    remote_bind_address=('212.109.221.219',3306),
    ssh_username='stas', ssh_password='stasUser51',
) as tunnel:
    connection = mysql.connector.connect(
        user='mysql', password='mysql_pass_29',
        host='127.0.0.1', port=tunnel.local_bind_port,
        database='guide_api',
    )
    # Do stuff
    connection.close()'''

'''import mysql.connector
from mysql.connector import Error

def connect():
   Connect to MySQL database
    try:
        conn = mysql.connector.connect(host='127.0.0.1',
                                       database='guide_api',
                                       user='mysql',
                                       password='mysql_pass_29')
        if conn.is_connected():
            print('Connected to MySQL database') 
            conn.close()

    except Error as e:
        print(e)

    #finally:
        #conn.close()

if __name__ == '__main__':
    connect()'''


'''import pymysql
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser

home = expanduser('~')
mypkey = paramiko.RSAKey.from_private_key_file(home + pkeyfilepath)
# if you want to use ssh password use - ssh_password='your ssh password', bellow

sql_hostname = '212.109.221.219'
sql_username = 'mysql'
sql_password = 'mysql_pass_29'
sql_main_database = 'guide_api'
sql_port = 3306
ssh_host = '212.109.221.219'
ssh_user = 'stas'
ssh_port = 59288
sql_ip = '1.1.1.1.1'
ssh_password = "stasUser51"

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=mypkey,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    conn = pymysql.connect(host='127.0.0.1', user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)
    query = SELECT VERSION();
    data = pd.read_sql_query(query, conn)
    conn.close()'''



'''import mysql.connector
import sshtunnel
import pandas as pd
#import configparser

#config = configparser.ConfigParser()
#config.read('c:/work/tmf/data_model/tools/config.ini')

ssh_host = '212.109.221.219'
ssh_port = 59288
ssh_username = 'stas'
ssh_pkey = "stasUser51"
sql_host = '10.8.0.18'
sql_port = 3306
sql_username = 'mysql'
sql_password = 'mysql_pass_29'

with sshtunnel.SSHTunnelForwarder(
        (ssh_host,ssh_port),
        ssh_username=ssh_username,
        ssh_password='stasUser51',
        remote_bind_address=(sql_host, sql_port)) as tunnel:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        user=sql_username,
        password=sql_password)
    query = 'select version();'
    data = pd.read_sql_query(query, connection)
    print(data)
    connection.close()'''