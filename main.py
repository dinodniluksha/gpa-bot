import flask
from flask import Flask, session, request, render_template, url_for
import scrapper
import dashboard

app = Flask(__name__)
app.secret_key = "xyz"

data = {}
user = {}


@app.route('/dashboard/<username>')
def open_dash(username):
    if session['username'] == username:
        m = data[username]['profile_data']
        n = data[username]['result_data']
        print(scrapper.profile_table)
        print(dashboard.string_html)
        # return f'{scrapper.profile_table[0]}{dashboard.string_html}'
        return f'{m}{n}'
    else:
        return flask.redirect("/login")


@app.route('/', methods=['GET'])
def get_default():
    return flask.redirect("/login")


@app.route('/login', methods=['GET'])
def get_logging():
    return render_template('login.html', initial_login="")


@app.route('/login', methods=['POST'])
def auth():
    username = request.form['Uname']
    password = request.form['Pass']

    if scrapper.authentication(username, password):
        session['username'] = username
        dashboard.func(username)
        # result_data = session[username]['result_data']
        print(session)
        # profile_data = session[username]['profile_data']
        user['profile_data'] = scrapper.profile_table[0]
        user['result_data'] = dashboard.string_html
        data[username] = user
        scrapper.profile_table.clear()
        dashboard.string_html = 'empty'
        return flask.redirect(url_for('open_dash', username = username))
    else:
        return render_template('login.html', initial_login=scrapper.login_error)


@app.route('/logout', methods=['GET'])
def get_logout():
    session.pop('username', None)
    return render_template('login.html', initial_login="")


