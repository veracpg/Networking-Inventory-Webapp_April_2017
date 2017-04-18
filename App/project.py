
import psycopg2

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)


def connect():
    try:
        conn_string = "host='localhost' dbname='hosts' user='postgres' password='secret'"
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        return db, cursor
    except:
        print('<error message>')

@app.route('/host')
def showHome():
    return render_template('home.html')


@app.route('/host/add', methods=['GET', 'POST'])
def newHost():
    return render_template('newhost.html')
    if request.method == 'POST':
        db, cursor = connect()
        query = 'INSERT INTO host (hostname, ipv4) VALUES (%s,%s);'
        params = (hostname,ipv4,)
        cursor.execute(query,params)
        if request.form ['hostname'] == 0 or request.form ['ipv4'] == 0:
            raise ValueError("Invalid new host")
        db.commit()
        db.close()
        flash('New host created succefully')
        return redirect(url_for('showHome'))


@app.route('/host/active', methods=['GET', 'POST', 'DELETE'])
def showActiveHosts():
    db, cursor = connect()
    query ='SELECT id, hostname,host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release,ssh_port, ssh_user FROM host WHERE active = TRUE;'
    cursor.execute(query)
    return render_template('activehost.html', items=cursor.fetchall())


# def deleteHost(host_id):
#     if request.method == 'DELETE':
#         return render_template('deletehost.html', host_id = host_id)
#
# def editHost(host_id):
#     if request.method == 'POST':
#         return render_template('edithost.html', host_id = host_id)
#
#
# @app.route('/host/active/<host_id>/delete', methods=['GET', 'POST', 'DELETE'])
# def deleteHostConfirmation(host_id):
#     if request.method == 'DELETE':
#         db,cursor = connect()
#         cursor.execute('DELETE FROM hosts;')
#         db.commit()
#         db.close()
#         flash('Delete Host')
#         return redirect(url_for('showActiveHosts'))
#     if request.method == 'POST':
#         return redirect(url_for('showActiveHosts'))
#
#
#
@app.route('/host/inactive', methods=['GET', 'POST'])
def showInactiveHosts():
    db, cursor = connect()
    inactive_hosts ='SELECT id, hostname,host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release,ssh_port, ssh_user FROM host WHERE active = FAlSE;'
    cursor.execute(inactive_hosts)
    return render_template('inactivehost.html', items=cursor.fetchall())
#

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
