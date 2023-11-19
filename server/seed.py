from dotenv import load_dotenv
load_dotenv()
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask import Flask  
from models import User, Blog, Comment, db
from faker import Faker
from random import choice


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

fake=Faker()

db.init_app(app)

with app.app_context():

    User.query.delete()
    Comment.query.delete()
    Blog.query.delete()

    for i in range(10):
        users=[]
        user1 = User(name=fake.name(), username=fake.name())
        users.append(user1)

        db.session.add_all(users)
        db.session.commit()


    for i in range(10):
        blogs=[]
        blog3 = Blog(blog_title=fake.text(20), blog_body=fake.paragraph(100), author=fake.name())
        blogs.append(blog3)

        db.session.add_all(blogs)
        db.session.commit()
        
        


    for i in range(1):
        comments=[]
        comment1 = Comment(comment_body=fake.text(), user=choice(users), blog=choice(blogs))
        comments.append(comment1)
        db.session.add_all(comments)
        db.session.commit()
    
    
