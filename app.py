from flask import Flask, render_template, redirect, request, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from werkzeug.utils import secure_filename
import os
import string
import random
import uuid
from datetime import datetime
app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messeges.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    messege = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"name is {self.name} and email is {self.email} and he said {self.messege}"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(50))
    desc = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"title is {self.title} blog image if {self.filename} and description is {self.desc}"


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"someone commented {self.comment}"


def generate_unique_filename(filename):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = str(uuid.uuid4().hex[:8])
    _, extension = os.path.splitext(filename)
    unique_filename = current_time + '_' + random_string + extension
    return secure_filename(unique_filename)


@app.route("/")
def home():
    return render_template("index.html", showhero=True)


@app.route("/about")
def about():
    return render_template("index.html", showabout=True)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form['name']
        email = request.form['email']
        messege = request.form['messege']
        msg = User(name=name, email=email, messege=messege)
        db.session.add(msg)
        db.session.commit()
    return render_template("index.html", showcontact=True)


@app.route("/blogs")
def blogs():
    post = Posts.query.all()

    return render_template("index.html", showblogs=True, posts=post)


@app.route("/blog/<proj_id>")
def blog(proj_id=None):
    post = Posts.query.filter_by(id=proj_id).first()
    pagecomments = Comments.query.filter_by(blog_id=proj_id)

    return render_template("blog.html", proj_id=proj_id, posts=post, comments=pagecomments)


@app.route("/admin/<password>", methods=['GET', 'POST'])
def admin(password=None):
    data = User.query.all()
    blogs = Posts.query.all()
    if request.method == "POST":
        image_file = request.files['image']
        title = request.form['title']
        desc = request.form['desc']

        # Generate a unique filename
        extension = os.path.splitext(image_file.filename)[
            1]  # Get the file extension
        random_string = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=8))  # Generate a random string
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}{random_string}{extension}"

        # Create the directory if it doesn't exist
        upload_folder = os.path.join(app.root_path, 'static', 'post_image')
        os.makedirs(upload_folder, exist_ok=True)

        # Save the image file to the static/post_image folder with the unique filename
        image_path = os.path.join(upload_folder, filename)
        image_file.save(image_path)

        # Create a new instance of the Posts model and set the attributes
        post = Posts(title=title, filename=filename, desc=desc)

        # Add the post instance to the session and commit changes
        db.session.add(post)
        db.session.commit()
        print(Posts.query.all())

    return render_template("admin.html", data=data, blogs=blogs, password=password)


@app.route("/update/<proj_id>", methods=['GET', 'POST'])
def update(password=None, proj_id=None):
    post = Posts.query.filter_by(id=proj_id).first()
    image = post.filename
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        post = Posts.query.filter_by(id=proj_id).first()
        post.title = title
        post.desc = desc
        post.filename = image
        db.session.add(post)
        db.session.commit()
        return redirect("/admin/tamimofficial")

    return render_template("update.html", proj_id=proj_id, posts=post, password=password)


@app.route("/delete/<proj_id>")
def delete(proj_id=None):
    post = Posts.query.filter_by(id=proj_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect("/admin/tamimofficial")


@app.route("/changeimg/<proj_id>", methods=['GET', 'POST'])
def changeimg(proj_id=None):
    post = Posts.query.filter_by(id=proj_id).first()
    title = post.title
    desc = post.desc
    if request.method == "POST":
        post.title = title
        post.desc = desc
        if 'update_img' in request.files:
            image = request.files['update_img']
            if image.filename != '':
                filename = generate_unique_filename(image.filename)
                image.save(os.path.join(app.root_path,
                           'static', 'post_image', filename))
                post.filename = filename
        db.session.add(post)
        db.session.commit()
        return redirect(f"/update/{post.id}")
    return render_template("changeimg.html", posts=post)


@app.route("/comment/<proj_id>", methods=['GET', 'POST'])
def comment(proj_id=None):
    post = Posts.query.filter_by(id=proj_id).first()

    if request.method == "POST":
        comment = request.form['comment']
        blog_id = post.id
        postComment = Comments(comment=comment, blog_id=blog_id)
        db.session.add(postComment)
        db.session.commit()
        print(
            f"some one commentted {postComment.comment} on {postComment.blog_id}")

    return redirect(f"/blog/{post.id}")


if __name__ == "__main__":
    app.run(debug=True)
