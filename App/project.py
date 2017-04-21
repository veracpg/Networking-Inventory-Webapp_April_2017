
import psycopg2

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)


def connect(database_name="hosts"):
    # Connect to the PostgreSQL database.  Returns a database connection.
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        print "DB Connected!\n"
        return db,cursor
    except:
        print("<error message>")

@app.route('/host')

def showHome():
    # Landing Page ( 3 links to newHost(), showActiveHosts() & showInactiveHosts)
    return render_template('home.html')


@app.route('/host/add', methods=['GET', 'POST'])
def newHost():
    if request.method == 'POST':
        hostname=request.form.get('hostname')
        host_alias = request.form.get('host_alias')
        hostgroup = request.form.get('hostgroup')
        ipv4 = request.form.get('ipv4')
        ipv6 = request.form.get('ipv6')
        os = request.form.get('os')
        os_type = request.form.get('os_type')
        os_release = request.form.get('os_release')
        ssh_port = request.form.get('ssh_port')
        ssh_user = request.form.get('ssh_user')
        active = request.form.get('active')
        db, cursor = connect()
        query = 'INSERT INTO host (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ' \
                'ssh_port, ssh_user, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        params = (hostname, host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release, ssh_port, ssh_user, active,)
        cursor.execute(query, params)
        db.commit()
        db.close()
        if active == True:
            flash('New host add successfully')
            return redirect(url_for('showActiveHosts'))
        else:
            flash('New host add successfully')
            return redirect(url_for('showInactiveHosts'))

    else:
        flash('All the form fields are required')
        return render_template('newhost.html')


@app.route('/host/active', methods=['GET', 'POST'])
def showActiveHosts():
    # Inventory of all active hosts with Link to editHost()
    db, cursor = connect()
    query ='SELECT id, hostname,host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release,ssh_port, ssh_user' \
           ' FROM host WHERE active = TRUE;'
    cursor.execute(query)
    rows = cursor.fetchall()
    db.close()
    return render_template('activehost.html', rows=rows)


@app.route('/host/edit', methods=['GET', 'POST'])
def editHost():
    if request.method == 'GET':
        db, cursor = connect()
        cursor.execute("SELECT id,hostname,host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release,ssh_port, "
                       "ssh_user, active FROM host;")
        row = cursor.fetchone()
        db.close()
        return render_template('edithost.html', id=row)
    else:
        return redirect(url_for('showInactiveHosts'))



@app.route('/host/inactive', methods=['GET', 'POST'])
# Inventory of all inactive hosts with link to EDIT
def showInactiveHosts():
    db, cursor = connect()
    query ='SELECT id, hostname,host_alias, hostgroup, ipv4, ipv6, os, os_type, os_release,ssh_port, ssh_user ' \
           'FROM host WHERE active = FAlSE;'
    cursor.execute(query)
    rows = cursor.fetchall()
    db.close()
    return render_template('inactivehost.html', rows=rows)


@app.route('/host/delete', methods=['GET', 'POST'])
def deleteHost():
    if request.method == 'POST':
        db, cursor = connect()
        cursor.execute("DELETE FROM host;")
        db.commit()
        db.close()
        return redirect(url_for('showHome'))
    else:
        return render_template('deletehost.html')


if __name__ == '__main__':
    connect(database_name='hosts')
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
