from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):   # Creating the db model for blogs
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):  # Returns the blogpost (id)
        return 'Blog post ' + str(self.id) 

# all_posts = [    # Its just the dummy data dict for testing
#     {
#         'title' : 'Post 1',
#         'content' : 'Content for post 1',
#         'author' : 'Faran'
#     },
#     {
#         'title' : 'Post 2',
#         'content' : 'Content for post 2'
#     }
# ]

@app.route('/')  # HomePage
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])  # Posting Blogs
def posts():

    if request.method == 'POST':  # Adding the data to the database
        post_title = request.form['title']  # collecting data from <form> in posts.html
        post_content = request.form['content'] 
        post_author = request.form['author']
        # Now creating new Blog Post after collecting the data
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        # Adding the new blog data to the database
        db.session.add(new_post)
        db.session.commit() # Saving the changes permanently
        return redirect('/posts')  # Redirecting to the same page
    else: # If not posting then only display the content
        # Overwriting the data in database into all_posts
        # Also ordering them according to the date posted by using orderby
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()  
        return render_template('posts.html', posts=all_posts)

@app.route('/home/users/<string:name>/posts/<int:id>')
def hello(name, id):
    return "Hello, " + name + " your current id is:" + str(id)

@app.route('/onlyget', methods=['GET'])
def get_req():
    return 'You can only get this webpage 1'

@app.route('/posts/delete/<int:id>')  # Deleting a Blog
def delete(id):
    post = BlogPost.query.get_or_404(id)  # If its already deleted then it should not break
    db.session.delete(post)
    db.session.commit()  # Permanent changes
    return redirect('/posts')  # Redirecting to the posts page after the deletion

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])  # For edititng a Blog
def edit(id):
    
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])  # New page for creating new blog
def new_post():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


if __name__ == "__main__":
    app.run(debug=True) 