from flask import render_template, request, redirect, flash,url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user
from LoginForm import LoginForm
from flask.ext.security import login_required
from models import Category, Todo, Author, db, User
from todoapp import app
from werkzeug.security import generate_password_hash, check_password_hash
from Article import Article
from displayInfo import DisplayInfo
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


# login_manager = LoginManager()
# login_manager.init_app(app)

@app.route('/')
def welcome():
    return render_template(
        'welcome.html',
        categories=Category.query.all(),
        todos=Todo.query.all() #.join(Author).order_by(Author.name)
    )    


@app.route('/<name>')
def list_todos(name):
    category = Category.query.filter_by(name=name).first()
    todos=Todo.query.filter_by(category=category).all()
    displays = []
    for todo in todos:
        print(todo.description)
        thisDisplay = DisplayInfo(todo)
        thisDisplay.get_soup()
        thisDisplay.get_title()
        thisDisplay.get_comments()
        displays.append(thisDisplay)
    return render_template(
        'list.html',
        displays=displays,
        category=category,
        todos=todos, #.join(Author).order_by(Author.name),
        categories=Category.query.all(),

    )


@app.route('/new-task', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        url = request.form['description']
        thisArticle = parse_article(url)
        category = Category.query.filter_by(id=request.form['category']).first()
        #priority = Priority.query.filter_by(id=request.form['priority']).first()
        #todo = Todo(category=category, priority=priority, description=request.form['description'])
        todo = Todo(category=category, description=url)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    else:
        return render_template(
            'new-task.html',
            page='new-task',
            categories=Category.query.all()
            # authors=Author.query.all()
        )

def parse_article(url):
     # given a url, get page content
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(req).read()
    # parse as html structured document
    bs = BeautifulSoup(data,'html.parser')
    # kill javascript content
    # print (bs.prettify())
    for s in bs.findAll('script'):
        s.replaceWith('')

    new_article = Article(bs)
    new_article.add_author()
    new_article.add_title()

    return new_article

@app.route('/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template(
            'new-task.html',
            todo=todo,
            categories=Category.query.all(),
            #authors=Author.query.all()
        )
    else:
        category = Category.query.filter_by(id=request.form['category']).first()
        #author = Author.query.filter_by(id=request.form['author']).first()
        description = request.form['description']
        todo.category = category
        #todo.author = author
        todo.description = description
        db.session.commit()
        return redirect('/')


@app.route('/new-category', methods=['GET', 'POST'])
@login_required
def new_category():
    if request.method == 'POST':
        category = Category(name=request.form['category'])
        db.session.add(category)
        db.session.commit()
        return redirect('/')
    else:
        return render_template(
            'new-category.html',
            page='new-category.html')


@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get(category_id)
    if request.method == 'GET':
        return render_template(
            'new-category.html',
            category=category
        )
    else:
        category_name = request.form['category']
        category.name = category_name
        db.session.commit()
        return redirect('/')


@app.route('/delete-category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    if request.method == 'POST':
        category = Category.query.get(category_id)
        if not category.todos:
            db.session.delete(category)
            db.session.commit()
        else:
            flash('You have TODOs in that category. Remove them first.')
        return redirect('/')


@app.route('/delete-todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')


@app.route('/mark-done/<int:todo_id>', methods=['POST'])
def mark_done(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        todo.is_done = True
        db.session.commit()
        return redirect('/')


# @login_manager.user_loader
# def user_loader(user_id):
#     """Given *user_id*, return the associated User object.

#     :param unicode user_id: user_id (email) user to retrieve
#     """
#     return User.query.get(user_id)

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """For GET requests, display the login form. For POSTS, login the current user
#     by processing the form."""
#     form = LoginForm(request.form)
#     if request.method == 'GET':
#         return render_template("login.html", form=form)
#     else:
#         print(form.validate())
#         if form.validate():
#             print(form.username.data)
#             #fails after this query
#             user = User.query.filter_by(username=form.username.data).first()
#             print("got user")
#             print(user.username)
#             if check_password_hash(user.password, form.password.data) == True:
#                 user.authenticated = True
#                 db.session.add(user)
#                 db.session.commit()
#                 login_user(user, remember=True)
#                 print("4")
#                 return redirect('/')
#             else:
#                 print('user not found')
#                 return redirect('/')          
#         return redirect('/')                      


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")    

