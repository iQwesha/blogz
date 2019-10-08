from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        new_post = Blog(blog_title)
        db.session.add(new_post)
        db.session.commit()

    blog = Blog.query.filter_by(title=title).all()
    new_post = Blog.query.filter_by(body=body).all()
    return render_template('blog.html', blog_title="Build a Blog", title=title, blog=blog) 


@app.route('/blog', methods=['POST'])
def blog():

    blog_title = request.form['blog-title']
    blog_body = request.form['blog-body']
    title_error = ""
    body_error = ""
    db.session.add(blog)
    db.session.commit()

    if blog_title = ""
        post = Blog.query.all()
        title_error = "Please enter a blog title"   
    else:
        return render_template('blog.html', post=post, title='blog-title')
    if blog_body == ""
        post = Blog.query.all()
        title_error = "Please enter a blog entry"  
    else:
        return render_template('new_post.html', post=post, title='blog-entry')


@app.route('/new_post', methods=['POST'])
def new_post():
    blog_id = int(request.form['blog-id'])
    blog - Blog.query.get(blog_id)

    return redirect('/')


app.run()
