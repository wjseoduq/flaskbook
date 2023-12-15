# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask import redirect, url_for
from apps.crud.forms import UserForm
from apps.crud.models import User
from apps.app import db

crud = Blueprint("crud",
                 __name__, 
                 template_folder="templates",
                 static_folder="static")


@crud.route("/")
def index():
    return render_template("crud/index.html")

# "127.0.0.1:5000/crud/user/new"
@crud.route("/users/new", methods=["GET","POST"])
def create_user():
    # views.py파일에 생성된 class(Userform)의 인스턴스를 생성
    form = UserForm()
    # 폼의 값을 검증한다
    if form.validate_on_submit():
        # 사용자를 작성한다
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # SQLAlchemy를 사용하여 데이터베이스에 ISERT
        # 사용자를 추가하고 commit한다
        db.session.add(user)
        db.session.commit()

        #사용자의 일람화면으로 리다이렉트한다
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)

@crud.route("/sql")
def sql():
    db.session.query(User).all()
    return "콘솔 로그를 확인해 주세요."

@crud.route("/users")
def users():
    # 사용자의 일람을 취득한다
    users = User.query.all()
    return render_template("crud/index.html", users=users)

# methods에 GET과 POST를 지정한다.
@crud.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    form = UserForm()

    # User model을 이용하여 사용자를 취득한다
    user = User.query.filter_by(id=user_id).first()

    # form으로부터 제출된 경우는 사용자를 갱신하여 사용자의 일람화면으로 리다이렉트한다.
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    # GET의 경우는 HTML을 반환한다
    return render_template("crud/edit.html", user=user, form=form)


# 삭제 엔드포인트 만들기
@crud.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user=User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))