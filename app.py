from pymongo import MongoClient
import jwt
import datetime
import hashlib
import certifi
import requests
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

#client = MongoClient('mongodb+srv://rmadbstjd:kys3421@cluster0.xwuyi.mongodb.net/Cluster0?retryWrites=true&w=majority')
#db = client.MINIPROJECT


client = MongoClient('mongodb+srv://test:sparta@cluster0.plrlvlp.mongodb.net/?retryWrites=true&w=majority')
db = client.spart_week1

# 메인페이지 @문동환
@app.route('/')
def main():
    return render_template("index.html")


# 상세페이지 @최효선
@app.route('/detail')
def detail():
    return render_template("detail.html")


# 작성페이지 @김보현
@app.route('/edit-page')
def edit_page():
    return render_template("edit-page.html")


# 로그인페이지 @금윤성
@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login/sign_in', methods=['POST'])
def sign_in():
    # 로그인

    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})
    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token, 'id' : payload["id"]})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/login/login_check', methods=['POST'])
def login_check():
    check_done_receive = request.form['check_done_give']
    check_id_receive = request.form['check_id_give']
    user = db.users.find_one({'username': check_id_receive})
    if  check_done_receive == 'success':

        return jsonify({'nickname' : user['nickname']})




# 회원가입 페이지 @금윤성
@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/register/sign_up', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "nickname": nickname_receive,
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
        "profile_pic": "",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""  # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/register/check_dup', methods=['POST'])
def check_dup():

    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})
    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


