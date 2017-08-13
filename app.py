# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, validators

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '10111105'
app.config['MYSQL_DB'] = 'messageboard'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MySQL
mysql = MySQL(app)

# msgForm Class
class msgForm(Form):
    username = StringField('姓名', [validators.required()])
    content = TextAreaField('留言', [validators.Length(min=1, max=999)])

# Home Page
@app.route('/', methods=['GET','POST'])
def index():

    form = msgForm(request.form)
    cur = mysql.connection.cursor()

    result = cur.execute('SELECT * FROM msg ORDER BY create_date DESC ')
    messages = cur.fetchall()

    if request.method == 'POST' and form.validate():
        username = form.username.data
        content = form.content.data

        cur.execute('INSERT INTO msg(username, content) VALUES(%s, %s)', (username, content))
        mysql.connection.commit()
        cur.close()
        # flash('您已留言', 'success')
        return redirect(url_for('index'))

    if result > 0:
        return render_template('index.html', form=form, messages=messages)
    else:
        msg = '暂时还没有人留言'
        return render_template('index.html', form=form, msg=msg)

    cur.close()

    return render_template('index.html',form=form)



if __name__ == '__main__':
    app.secret_key = 'sohardtoguess'
    app.run(debug=True)
