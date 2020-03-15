# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:23:31 2019

@author: LeoFishLiao
"""

from flask import Flask,request,jsonify
from flask_mysqldb import MySQL




app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lzy19970217'
app.config['MYSQL_DB'] = 'restful'
mysql = MySQL(app)

@app.route('/info',methods = ['GET','POST'])
def info():
    messages = ""
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute('''SELECT * FROM users ''')
        rv = cur.fetchall()
        messages = rv
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('''SELECT max(id) from users''')
        max_id = cur.fetchone()[0]
        current_id = max_id + 1
        data = request.get_json()
        for i in data:
            cur.execute('''INSERT INTO users (id,name,email,city,phone) VALUES (%s,%s,%s,%s,%s)''',(current_id, i['name'],i['email'],i['city'],i['phone']))
            current_id += 1
        mysql.connection.commit()
    return jsonify(messages)

@app.route('/info/<int:id>',methods = ['PUT'])
def updataData(id):
    cur=mysql.connection.cursor()
    cur.execute('''SELECT id from users''')
    res = cur.fetchall()
    data = request.get_json()
    checklist = []
    for key in data:
        checklist.append(key)
    flag = 0
    messages = ""
    for i in range(len(res)):
        if res[i][0] ==id :
            flag = 1
            break
    if flag == 1:
        data = request.get_json()
        if data:
            if "name" in checklist:
                cur.execute('''UPDATE users SET name = %s where id = %s''',(data['name'],id))
            if "email" in checklist:
                cur.execute('''UPDATE users SET email = %s where id = %s''',(data['email'],id))
            if "city" in checklist:
                cur.execute('''UPDATE users SET city = %s where id = %s''',(data['city'],id))
            if "phone" in checklist:
                cur.execute('''UPDATE users SET phone = %s where id = %s''',(data['phone'],id))

            mysql.connection.commit()
            messages = "data has been updated"
    else:
        messages = "id not found"
    return str(messages)

@app.route('/info/<int:id>',methods = ['DELETE'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE From users where id = %s''',([id]))
    mysql.connection.commit()
    
    return "info has been deleted"




if __name__ == '__main__':
    app.run(debug = True)
