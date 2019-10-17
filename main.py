from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lc101@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blog = db.relationship('Blog', backref='owner')

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    user = User.query.all()
    return render_template('index.html', user=user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    username = ""
    password = ""
    username_error = ""
    password_error = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            return redirect('/new_post')
        
        if not user:
            username_error ="User does not exist"
            return render_template('login.html', username_error = username_error)
        
        if user and user.password != password:
            password_error ="User password incorrect"
            return render_template('login.html', username=username, username_error=username_error, password=password, password_error = password_error)
    
    return render_template('login.html')

@app.route('/signup', method=['POST'])
def signup(): 
    username_error =""
    password_error =""
    verify_password_error=""
    existing_user_error=""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            existing_user_error ="Username already exists"
            return render_template('login.html', existing_user_error=existing_user_error)


        if password != verify:
            verify_password_error = "Passwords do not match"
            verify = ""
            return render_template('signup.html', username=username, password=password, verify_password_error=verify_password_error)


        if not existing_user_error and not username_error and not password_error and not verify_password_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username 
            return redirect('/new_post')
    
    else:
        return render_template('signup.html')

@app.route('/blog', methods=['GET'])
def blog():
    owner = User.query.filter_by(username=session['username']).first()
    blog = Blog.query.order_by(Blog.pub_date.desc())
    blog_id = request.args.get('id')
    user_id = request.args.get('user')

    if blog_id:
        blog = Blog.query.filer_by(id=blog_id).first()
        return render_template('blog.html', title=blog_title, body=blog_body, user=blog.owner.username, pub_date=blog.pub_date, user_id=blog.owner_id)

    if user_id:
        blog = Blog.query.filter_by(owner_id=user_id).all_features()
        return render_template('entry.html', blog=blog)
   
    return redirect('/blog?user_id'.format(blog.id))
  

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_post = Blog(blog_title, blog_body)
        blog_error = ""
        title_error = ""
        body_error = ""

        if blog_title == "" and blog_body == "":
            blog_error = 'Please enter a title and content for the blog entry'
            return render_template ('new_post.html', title= blog_title, body= blog_body, blog_error=blog_error)

        if blog_title == "":
            title_error = "Please enter a title" 
            return render_template ('new_post.html', title= blog_title, body= blog_body, title_error = title_error) 
            
        if blog_body == "":
            body_error = "Please enter content for the blog entry"
            return render_template ('new_post.html', title= blog_title, body= blog_body, body_error= body_error)
    
        else:    
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id={0}'.format(new_post.id))
    else:
        return render_template('new_post.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['username']
    return redirect('/blog')

if __name__== '__main__':
    app.run()
