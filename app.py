from pymongo import MongoClient
<<<<<<< HEAD

import certifi

# import requests
=======
import jwt
import datetime
import hashlib
import certifi
import requests
response = requests.get('https://mydomain.com', verify=False)
ca = certifi.where()
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

>>>>>>> 7a060deed4a75b78a9f3c9ea0f390572d29bb7f4

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb+srv://rmadbstjd:kys3421@cluster0.xwuyi.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.MINIPROJECT


<<<<<<< HEAD
client = MongoClient('mongodb+srv://test:sparta@cluster0.plrlvlp.mongodb.net/?retryWrites=true&w=majority' , tlsCAFile=certifi.where())
db = client.spart_week1
=======


#client = MongoClient('mongodb+srv://test:sparta@cluster0.plrlvlp.mongodb.net/?retryWrites=true&w=majority')
#db = client.spart_week1
>>>>>>> 7a060deed4a75b78a9f3c9ea0f390572d29bb7f4


@app.route('/')
def home():
    return render_template('./index.html')

# 메인페이지 @문동환
@app.route("/review_test", methods=["GET"])
def main_get():
    book_list = list(db.review_test.find({},{'_id':False}))
    return jsonify({'books':book_list})

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
    print('test')
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

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

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
    print('test')
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

# @app.route('/detail/<keyword>')
# def detail(keyword):
#     # API에서 단어 뜻 찾아서 결과 보내기
#     status_receive = request.args.get("status_give", "old")
#     r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}",
#                      headers={"Authorization": "Token c921380aaf23c3c6bdba4a2b2daeda593aa3acb4"})
#     if r.status_code != 200:
#         return redirect(url_for("main", msg="Word not found in dictionary; Try another word"))
#     result = r.json()
#     print(result)
#     return render_template("detail.html", word=keyword, result=result, status=status_receive)


# @app.route('/api/save_word', methods=['POST'])
# def save_word():
#     # 단어 저장하기
#     word_receive = request.form['word_give']
#     definition_receive = request.form['definition_give']
#     doc = {"word": word_receive, "definition": definition_receive}
#     db.words.insert_one(doc)
#     return jsonify({'result': 'success', 'msg': f'word "{word_receive}" saved'})


# @app.route('/api/delete_word', methods=['POST'])
# def delete_word():
#     # 단어 삭제하기
#     word_receive = request.form['word_give']
#     db.words.delete_one({"word": word_receive})
#     db.examples.delete_many({"word": word_receive})
#     return jsonify({'result': 'success', 'msg': f'word "{word_receive}" deleted'})


# @app.route('/api/get_examples', methods=['GET'])
# def get_exs():
#     word_receive = request.args.get("word_give")
#     result = list(db.examples.find({"word": word_receive}, {'_id': 0}))
#     print(word_receive, len(result))

#     return jsonify({'result': 'success', 'examples': result})


# @app.route('/api/save_ex', methods=['POST'])
# def save_ex():
#     word_receive = request.form['word_give']
#     example_receive = request.form['example_give']
#     doc = {"word": word_receive, "example": example_receive}
#     db.examples.insert_one(doc)
#     return jsonify({'result': 'success', 'msg': f'example "{example_receive}" saved'})


# @app.route('/api/delete_ex', methods=['POST'])
# def delete_ex():
#     word_receive = request.form['word_give']
#     number_receive = int(request.form["number_give"])
#     example = list(db.examples.find({"word": word_receive}))[number_receive]["example"]
#     print(word_receive, example)
#     db.examples.delete_one({"word": word_receive, "example": example})
#     return jsonify({'result': 'success', 'msg': f'example #{number_receive} of "{word_receive}" deleted'})

