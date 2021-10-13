from datetime import timedelta, datetime
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
    session['wrong_credentials'] = False

    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']

        admin_user = data_manager.get_admin()

        if user_name == admin_user['user_name'] and util.verify_password(password, admin_user['password']) is True:
            session['logged_in'] = True
            session.permanent = True
            print("Good credentials")
            return redirect('/admin')
        else:
            print("Wrong credentials")
            session['wrong_credentials'] = True

    return render_template('admin/login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('wrong_credentials', None)

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

    all_contents = data_manager.get_all_content_preview()

    return render_template('admin/page_content.html', contents=all_contents)


@app.route('/admin/add-content')
def add_content():
    if 'logged_in' not in session:
        return redirect('/login')

    categories = data_manager.get_all_categories()

    return render_template('admin/add_content.html', categories=categories)


@app.route('/admin/save-content', methods=['POST'])
def save_content():

    data = {"title": request.form['title'],
            "description": request.form['content'],
            "image": request.form['image'],
            "public": True if 'public' in request.form else False,
            "last_modified": datetime.now(),
            "category": request.form['category']}

    data_manager.save_content(data)

    return redirect('/admin/content')


@app.route('/admin/edit-content/<content_id>', methods=['POST', 'GET'])
def edit_content(content_id):
    if request.method == "POST":
        data = {"id": content_id,
                "title": request.form['title'],
                "description": request.form['content'],
                "public": True if 'public' in request.form else False,
                "last_modified": datetime.now(),
                "category": request.form['category']}

        data_manager.update_content(data)

    content = data_manager.get_content(content_id)
    categories = data_manager.get_all_categories()

    return render_template("admin/edit_content.html", content=content, id=content_id, categories=categories)


@app.route('/admin/delete-content/<content_id>', methods=['GET'])
def delete_content(content_id):
    data_manager.delete_content(content_id)

    return redirect('/admin/content')


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
