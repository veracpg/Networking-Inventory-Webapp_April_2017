
import json
import random
import string
import httplib2
import requests
import jinja2

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from flask import make_response, jsonify
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_connector import Base, Host

# App Configuration

CLIENT_ID = json.loads(
    open('client_secrets.json','r').read())['web']['client_id']

APPLICATION_NAME = "Inventory webapp"

app = Flask(__name__)

# Connect to Database


engine = create_engine('postgresql:///hosts')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Routes

@app.route('/')
@app.route('/host')
def showHome():
    # Landing Page
    return render_template('home.html')

# JSON APIs read  NET info

@app.route('/host/JSON',  methods=['GET', 'POST'])
def getNet():
    # Return JSON version of the Network
    output_json = []
    rows = session.query(Host).all()
    return jsonify (rows=[r.serialize for r in rows ])

# Login Oauth2 Google

@app.route('/login', methods=['POST','GET'])
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST','GET'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<br><h3 style = "margin-left:40%;">Welcome, '
    output += login_session['username']
    output += '!</h3><br><br>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; margin-left:40%"><br><br> '

    return output

@app.route('/gdisconnect')
def gdisconnect():
    # DISCONNECT
    credentials = login_session.get('state')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showHome'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Create a new host

@app.route('/host/add', methods=['GET', 'POST'])
def newHost():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newHost = Host(hostname = request.form.get('hostname'),
                        host_alias = request.form.get('host_alias'),
                        hostgroup = request.form.get('hostgroup'),
                        ipv4 = request.form.get('ipv4'),
                        ipv6 = request.form.get('ipv6'),
                        os = request.form.get('os'),
                        os_type = request.form.get('os_type'),
                        os_release = request.form.get('os_release'),
                        ssh_port = request.form.get('ssh_port'),
                        ssh_user = request.form.get('ssh_user'),
                        active = request.form.get('active'))
        session.add(newHost)
        session.commit()
        return redirect(url_for('showActiveHosts'))
    else:
        return render_template('newhost.html')

@app.route('/host/active', methods=['GET', 'POST'])
def showActiveHosts():
    # Inventory of all active hosts with Link to editHost()
    rows = session.query(Host).filter_by(active = True).all()
    return render_template('activehost.html',rows=rows)


@app.route('/host/edit/<int:host>', methods=['GET', 'POST'])
def editHost(host):
    if 'username' not in login_session:
        return redirect('/login')
<<<<<<< Updated upstream

    editedHost= session.query(Host).filter_by(id=host).one_or_none()

    if editedHost == None:
        return redirect("/host?invalid_host=true")

||||||| merged common ancestors
    editedHost= session.query(Host).filter_by(id=host).one()
=======

    editedHost= session.query(Host).filter_by(id=host).one()

    if editedHost == None:
        return redirect("/host?invalid_host=true")

>>>>>>> Stashed changes
    if request.method =='POST':
        print "POST"
        if request.form['hostname'] and request.form['host_alias'] and \
            request.form['hostgroup'] and request.form['ipv4'] and \
            request.form['ipv6'] and request.form['os'] and \
            request.form['os_type'] and request.form['os_release'] and \
            request.form['ssh_port'] and request.form['ssh_user'] and \
            request.form['active']:
            print "Everything present"
            # Every row is present in the request
            editedHost.hostname = request.form['hostname']
            editedHost.host_alias = request.form['host_alias']
            editedHost.hostgroup = request.form['hostgroup']
            editedHost.ipv4 = request.form['ipv4']
            editedHost.ipv6 = request.form['ipv6']
            editedHost.os = request.form['os']
            editedHost.os_type = request.form['os_type']
            editedHost.os_release = request.form['os_release']
            editedHost.ssh_port = request.form['ssh_port']
            editedHost.ssh_user = request.form['ssh_user']
            editedHost.active = request.form['active']
            session.add(editedHost)
            session.commit()
            return redirect(url_for('showActiveHosts'))
        else:
            return redirect("/host?updated=false")
    else:
        print "GET"
        return render_template('edithost.html', row = editedHost)


@app.route('/host/inactive', methods=['GET', 'POST'])
# Inventory of all inactive hosts with link to EDIT
def showInactiveHosts():
    rows = session.query(Host).filter_by(active = False).all()
    return render_template('inactivehost.html', rows=rows)


@app.route('/host/delete/<int:host>', methods=['GET', 'POST'])
def deleteHost(host):
    if 'username' not in login_session:
        return redirect('/login')
    deletedhost = session.query(Host).filter_by(id=host).one()
    if request.method == 'POST':
        session.delete(deletedhost)
        session.commit()
        return redirect(url_for('showHome'))
    else:
        return render_template('deletehost.html', row = deletedhost)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
