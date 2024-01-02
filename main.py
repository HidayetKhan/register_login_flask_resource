from flask import Flask, request
from flask_restful import Api,Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)


# user_args=reqparse.RequestParser()
# user_args.add_argument('name',type=str,required=True)
# user_args.add_argument('username',type=str,help='Username required',required=True)
# user_args.add_argument('email',type=str,help='Email required',required=True)
# user_args.add_argument('password',type=str,required=True)


class UserModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    username=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)

user_resourse_field={
     "id":fields.Integer,
     "name":fields.String,
     "username":fields.String,
     "email":fields.String,
     "password":fields.String,

}


class Register(Resource):
    @marshal_with(user_resourse_field)
    def put(self):
        data=request.get_json()
        print(data)
        # now createa model class to save data to db
        # check user name alredy taken or not
        username=data['username']
        user=UserModel.query.filter_by(username=username).first()
        if user:
            abort(489,message='user alredy register with given username')

        user=UserModel(name=data['name'],username=data['username'],email=data['email'],password=data['password'])
        db.session.add(user)
        db.session.commit()
        return user
    

class Login(Resource):
    @marshal_with(user_resourse_field)
    def post(self):
        data=request.get_json()
        print(data)
        if 'username' not in data or 'password' not in data:
            abort(400,message='both username and password are required for login ')
        username=data['username']
        password=data['password']
        user=UserModel.query.filter_by(username=username,password=password).first()
        if not user:
            abort(400,message='username or password not valid')   

        return user 






#handle requset
api.add_resource(Register,'/register')
api.add_resource(Login,'/login')






if __name__=='__main__':
    with app.app_context():
      db.create_all()
      app.run(debug=True)