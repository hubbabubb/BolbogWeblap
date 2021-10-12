from datetime import timedelta

from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=6)
app.secret_key = 'my super secret key'.encode('utf8')


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_name = ''
    password = ''

    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']

    if user_name == 'Hubb' and password == '123':
        session['logged_in'] = True
        session.permanent = True
        return redirect('/admin')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)

    return redirect('/')


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        return redirect('/login')
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)
