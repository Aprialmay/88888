from flask import Flask, request, render_template, jsonify
import spacy
from pymongo import MongoClient
from gridfs import GridFS
from flask import send_file
from bson import ObjectId
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 初始化登录管理
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'random_key'

# 用户类定义
class User(UserMixin):
    def __init__(self, email, user_type):
        self.id = email
        self.user_type = user_type

# 用户加载函数
@login_manager.user_loader
def load_user(email):
    client = MongoClient("MongDBURL")  # 替换为你的 MongoDB URL
    db = client["login"]
    user_data = db.users.find_one({"email": email})
    if user_data:
        return User(email=user_data["email"], user_type=user_data["user_type"])

# 登录表单
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('登录')

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        client = MongoClient("MongDBURL")
        db = client["login"]
        user = db.users.find_one({"email": form.email.data})
        matched = check_password_hash(user['password'], form.password.data)
        
        if user and matched:
            user_obj = User(email=user["email"], user_type=user["user_type"])
            login_user(user_obj)  # 设置当前用户
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('登录失败，请检查邮箱和密码', 'danger')
    return render_template('login.html', title='登录', form=form)
