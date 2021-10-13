from datetime import timedelta
import data_manager
import util

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

    return render_template('admin/login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)

    return redirect('/')


@app.route('/admin')
@app.route('/admin/info')
def admin():
    if 'logged_in' not in session:
        return redirect('/login')

    return render_template('admin/admin_info.html')


@app.route('/admin/content')
def admin_content():
    if 'logged_in' not in session:
        return redirect('/login')

    return render_template('admin/page_content.html')


@app.route('/about')
def about():
    company_info = data_manager.get_company_info()

    return render_template('about.html', company_info=company_info)


@app.route('/info')
def default_info():
    categories = data_manager.get_public_categories()
    category = categories[0]
    content = data_manager.get_public_content_by_category(category)

    return render_template('information.html', categories=categories, blogs=content)


@app.route('/info/<category>')
def info(category):
    categories = data_manager.get_public_categories()
    content = data_manager.get_public_content_by_category(category)

    return render_template('information.html', categories=categories, blogs=content)


if __name__ == '__main__':
    app.run(debug=True)
