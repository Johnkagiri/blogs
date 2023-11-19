from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask import Flask, jsonify, request, make_response, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy import and_
from werkzeug.exceptions import NotFound
from flask_cors import CORS
import os
from models import db, Blog, Comment, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True
migrate = Migrate(app,db,render_as_batch=True)

CORS(app)

app.secret_key = b'?w\x85Z\x08Q\xbdO\xb8\xa9\xb65Kj\xa9_'

db.init_app(app)
api = Api(app)

# @app.before_request
# def check_if_logged_in():
#     allowed_endpoint=['login','signup','session','logout','users']
#     if not session.get('userid') and request.endpoint not in allowed_endpoint:
#         return {"error":'must login first'}
    

class SignUp(Resource):
    def post(self):
        data= request.get_json()

        name=data.get('name')
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return{'message': 'Username or password required'},400
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'message': 'Username already in use. Please choose a different one.'}, 400
        
        newuser=User(username=username, name=name)
        newuser.password_hash=password

        db.session.add(newuser)
        db.session.commit()

        session['userid']=newuser.id
        
        return make_response(newuser.to_dict(),201)
    
api.add_resource(SignUp,'/signup',endpoint='signup')   


class Login(Resource):
    def post(self):
        data=request.get_json()

        username=data.get('username')
        password=data.get('password')

        userinst = User.query.filter(User.username==username).first()

        if not username:
            return{'message':'Username and password required'},400
        
        if userinst and userinst.authenticate(password):
            session['userid'] = userinst.id

            return {'message':'login successful', "dict":userinst.to_dict(), "status":201}
                
        else:
            return {'message':'invalid password or username'},402
        
api.add_resource(Login,'/login',endpoint='login')

class Logout(Resource):
    def delete(self):
        if session.get('userid'):
            session['userid']=None
            return jsonify({'message': 'User logged out successfully'})
        else: 
            return {"error": "User must be logged in"}

api.add_resource(Logout, '/logout', endpoint='logout')

class CheckSession(Resource):
    def get(self):
        if session.get('userid'):
            user=User.query.filter(User.id==session.get('userid')).first()
            user_dict=user.to_dict()
            return make_response(jsonify(user_dict),200)
        else:
            return 'user is not in session please log in'
        

api.add_resource(CheckSession, '/session', endpoint='session')

class Blogres(Resource):
    def get(self):
        blog_dict=[n.to_dict() for n in Blog.query.all()]
        response = make_response(
            jsonify(blog_dict),200
        )
        return response
 

    def post(self):
        data = request.get_json()        
        newrec= Blog(
            author=data.get('author'),
            blog_title=data.get('blog_title'),
            blog_body=data.get('blog_body'),
        )

        db.session.add(newrec)
        db.session.commit() 

        newrec_dict=newrec.to_dict()

        response=make_response(jsonify(newrec_dict))
        response.content_type='application/json'

        return response

        

api.add_resource(Blogres, '/blogs', endpoint='blogs')


class BlogById(Resource):
    def get(self,id):
        blog= Blog.query.filter_by(id=id).first()

        if not blog:
            return {"error": "Blog not found"}, 404

        
        blog_dict=blog.to_dict()

        response=make_response(jsonify(blog_dict),200)
        return response
    
    def patch(self,id):
        blog= Blog.query.filter_by(id=id).first()

        if not blog:
            return {"error": "Blog not found"}, 404


        for attr in request.get_json():
            setattr(blog,attr,request.get_json()[attr])

            db.session.add(blog)
            db.session.commit()

            user_dict=blog.to_dict()

            response = make_response(jsonify(user_dict),200)
            return response


    def delete(self,id):
        blog= Blog.query.filter_by(id=id).first()
        comment=Comment.query.filter( and_(Comment.blog_id == id , Comment.user_id==session.get('userid')) ).delete() 

        if not blog:
            return {"error": "Blog not found"}, 404

        db.session.delete(blog)
       
        db.session.commit()

        response_body={"message": "Blog deleted successfully"},200
        return response_body
    
api.add_resource(BlogById,'/blog/<int:id>', endpoint='blogid')

class Users(Resource):
    def get(self):
        users=[user.to_dict() for user in User.query.all()]


        response=make_response(jsonify(users), 200)
        return response
    
api.add_resource(Users,'/users', endpoint='users')

class Comments(Resource):
    def get(self):
        comments=[comment.to_dict() for comment in Comment.query.all()]

        response=make_response(jsonify(comments),200)

        return response
    
    def post(self):
        new_comment=Comment(
            comment_body=request.get_json()['comment_body'],
            user_id= request.get_json()['user_id'],
            blog_id= request.get_json()['blog_id']
        )

        db.session.add(new_comment)
        db.session.commit()

        new_comment_dict=new_comment.to_dict()

        response=make_response(jsonify(new_comment_dict))
        response.content_type='application/json'
   
        return response
             
    
api.add_resource(Comments, '/comments', endpoint='comments')

class CommentById(Resource):
    def get(self,id):
        comment = Comment.query.filter_by(id=id).first()
        if not comment:
           return("comment not found"),404
        comment_to_dict= comment.to_dict()
        response = make_response(jsonify(comment_to_dict),201)
        return response 
    

    def patch(self,id):
        comment = Comment.query.filter_by(id=id).first()
        if not comment:
            return ('comment not found'), 404
        
        for attr in request.get_json():
            setattr(comment,attr,request.get_json()[attr])

            db.session.add(comment)
            db.session.commit()

            comment_dict=comment.to_dict()

            response=make_response(jsonify(comment_dict),201)

            return response


    def delete(self,id):
        comment = Comment.query.filter_by(id=id).first()
        if not comment:
            return({"message":"comment not found"}),404
        db.session.delete(comment)
        db.session.commit()
        response = make_response({"message": "comment deleted successfully"},200)
        return response

        
api.add_resource(CommentById,'/comment/<int:id>', endpoint='comment')

@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found:The requested endpoint(resource) does not exist",
        404
        )
    return response
 


if __name__=='__main__':
    app.run(debug=True, port=5000)

