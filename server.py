from datetime import timedelta, datetime
import data_manager
import util
import os

from flask import Flask, render_template, session, redirect, request

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=6)
app.config['IMAGE_UPLOADS'] = "static/images"
app.secret_key = 'my super secret key'.encode('utf8')


@app.route('/')
def index():
    print(util.hash_password('admin1234'))
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
    session.pop('message', None)

    return redirect('/')


@app.route('/admin')
@app.route('/admin/info', methods=['POST', 'GET'])
def admin():
    if 'message' in session:
        session.pop('message', None)
    if 'logged_in' not in session:
        return redirect('/login')

    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'telephone_number': request.form['telephone_number'],
            'email': request.form['email'],
            'address': request.form['address'],
            'description': request.form['description'],
        }

        data_manager.update_info(data)
        session['message'] = "Céginformációk elmentve!"

    basic_info = data_manager.get_company_info()
    admin_info = data_manager.get_admin()

    return render_template('admin/admin_info.html', basic_info=basic_info, admin_info=admin_info)


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
    image = request.files["image"]
    path = app.config['IMAGE_UPLOADS']

    image_name = None
    image_direction = None
    if image.filename:
        image_name = util.get_image_name(image)

        if not util.allowed_file(image.filename):
            return render_template('admin/add_content.html', message='Not a valid file format!', categories=data_manager.get_all_categories())

        image.save(os.path.join(path, image.filename))
        image_direction = util.image_direction(image_name)

    data = {"title": request.form['title'],
            "description": request.form['content'],
            "image": image_name,
            "image_source": request.form['image-source'],
            "image_direction": image_direction,
            "public": True if 'public' in request.form else False,
            "last_modified": datetime.now(),
            "category": request.form['category']}

    data_manager.save_content(data)

    return redirect('/admin/content')


@app.route('/admin/edit-content/<content_id>', methods=['POST', 'GET'])
def edit_content(content_id):
    if request.method == "POST":
        print(request.form['image-source'])
        data = {"id": content_id,
                "title": request.form['title'],
                "description": request.form['content'],
                "public": True if 'public' in request.form else False,
                "last_modified": datetime.now(),
                "category": request.form['category'],
                "image-source": request.form['image-source']
                }

        data_manager.update_content(data)

    content = data_manager.get_content(content_id)
    categories = data_manager.get_all_categories()

    return render_template("admin/edit_content.html", content=content, id=content_id, categories=categories)


@app.route('/admin/delete-content/<content_id>', methods=['GET'])
def delete_content(content_id):
    data_manager.delete_content(content_id)

    return redirect('/admin/content')


@app.route('/elerhetoseg')
def about():
    company_info = data_manager.get_company_info()
    return render_template('about.html', company_info=company_info)


@app.route('/info')
def default_info():
    categories = data_manager.get_public_categories()
    category = categories[0]
    content = data_manager.get_public_content_by_category(category)

    return render_template('information.html', categories=categories, blogs=content, submenu=False)


@app.route('/info/<category>')
def info(category):
    categories = data_manager.get_public_categories()
    content = data_manager.get_public_content_by_category(category)

    return render_template('information.html', categories=categories, blogs=content, submenu=True, selected_category=category)


if __name__ == '__main__':
    app.run(debug=True)
