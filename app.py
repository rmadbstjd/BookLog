from dataclasses import dataclass
from flask import Flask, render_template, request, jsonify, redirect, url_for
from jinja2 import Undefined
from pymongo import MongoClient
from datetime import datetime, timedelta
import requests
import json
import xmltodict, json
import urllib

import jwt
import hashlib
import certifi
from werkzeug.utils import secure_filename

ca = certifi.where()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

# user가 저장된 db
client = MongoClient('mongodb+srv://rmadbstjd:kys3421@cluster0.xwuyi.mongodb.net/Cluster0?retryWrites=true&w=majority' , tlsCAFile=certifi.where())
db = client.MINIPROJECT

# 리뷰가 저장된 db
review_client = MongoClient('mongodb+srv://test:sparta@cluster0.plrlvlp.mongodb.net/?retryWrites=true&w=majority' , tlsCAFile=certifi.where())
review_db = review_client.spart_week1

# 메인페이지 @문동환
@app.route('/')
def main():
    return render_template("index.html")

@app.route("/review_test", methods=["GET"])
def main_get():
    book_list = list(review_db.review_test.find({},{'_id':False}))
    return jsonify({'books':book_list})

@app.route("/passid", methods=["POST"])
def get_nickname():
    id_value_receive = request.form['id_value_give']
    user_nickname = list(db.users.find({'username': id_value_receive},{'_id':False}))
    nickname = user_nickname[0]['nickname']
    print(nickname)
    return render_template("index.html", nickname=nickname)

# 상세페이지 @최효선
@app.route('/detail')
def detail():
    return render_template("detail.html")

@app.route('/detail/<reviewNo>')
def detailedReview(reviewNo):
    
    return render_template("detail.html", reviewNo=reviewNo)

# 작성페이지 @김보현
@app.route('/edit-page')
def edit_page():
    return render_template("edit-page.html", nickname="둘리")

# 수정페이지 @김보현
@app.route('/edit/<reviewNo>')
def edit_review(reviewNo):
    
    book_list = list(review_db.review_test.find({"content_no":int(reviewNo)},{'_id':False}))

    print(book_list)
    
    title = book_list[0]['title']
    content = book_list[0]['content']
    image_url = book_list[0]['file']
    
    return render_template("edit-page.html", title=title, content=content, image=image_url, review_no=reviewNo, isEdit=title)


# 네이버를 통해 검색된 책자의 리뷰를 작성
@app.route('/edit-page/<isbn>')
def find_bookdetail_via_isbn(isbn):
    
    # /api/call-bookinfo URL로 POST 방식으로 도착한 데이터
    header_info = {"X-Naver-Client-Id": "0g0WhKXaBnkuD7TS7sEC", "X-Naver-Client-Secret": "EV_4uF2dqi"}
    r = requests.get('https://openapi.naver.com/v1/search/book_adv.xml?d_isbn='+str(isbn), headers=header_info)

    o = xmltodict.parse(r.text)
    result=json.dumps(o, ensure_ascii=False)
    data = json.loads(result)
    
    title = data['rss']['channel']['item']['title']
    image_url = data['rss']['channel']['item']['image']
    author = data['rss']['channel']['item']['author']
    description = data['rss']['channel']['item']['description']
    
    return render_template("edit-page.html", title=title, image=image_url, author = author, description = description)


# 작성된 리뷰를 저장 @김보현
@app.route('/save-review', methods=['POST'])
def save_review():
    
    all_reviews = list(review_db.review_test.find({},{'_id':False}))
    print(all_reviews[-1]['content_no'])
    
    booktitle = request.form['booktitle_give']
    review_content = request.form['review_content_give']
    img_url = request.form['imgfile_give']
    
    doc = {
        'title': booktitle,
        'content':review_content,
        'file': img_url,
        'time': datetime.now().strftime('%Y.%m.%d'),
        'content_no': all_reviews[-1]['content_no']+1
        }

    review_db.review_test.insert_one(doc)
    
    return render_template("index.html")


# 수정된 리뷰를 저장 @김보현
@app.route('/update-review', methods=['POST'])
def update_review():
    
    booktitle = request.form['booktitle_give']
    review_content = request.form['review_content_give']
    img_url = request.form['imgfile_give']
    content_no = int(request.form['edited_content_no'])

    doc = {
    'title': booktitle,
    'content':review_content,
    }
        
    review_db.review_test.update_one({'content_no':content_no},{'$set':doc})
    
    return render_template("index.html")


# 리뷰 삭제 @김보현
@app.route('/delete/<reviewNo>')
def delete_review(reviewNo):
    
    review_db.review_test.delete_one({'content_no':int(reviewNo)})
        
    return render_template("index.html")
    
    
# naverapi에서 검색어 정보를 불러오는 코드 @김보현
@app.route('/api/call-bookinfo', methods=['POST'])
def give_bookInfo():

    data = urllib.parse.unquote(request.data)
    print(data)
    
    # /api/call-bookinfo URL로 POST 방식으로 도착한 데이터
    header_info = {"X-Naver-Client-Id": "0g0WhKXaBnkuD7TS7sEC", "X-Naver-Client-Secret": "EV_4uF2dqi"}
    r = requests.get('https://openapi.naver.com/v1/search/book.json?'+data, headers=header_info)
    result = r.json()
    return result



# 로그인페이지 @금윤성
@app.route('/login')
def login():
    return render_template("login.html")

# 로그인  @금윤성
@app.route('/login/sign_in', methods=['POST'])
def sign_in():

    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    user_nickname = db.users.find_one({'username': username_receive})
    nick = user_nickname['nickname']
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})
    if result is not None:
        payload = {
            'id': username_receive,
            'nickname': nick,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token, 'id' : payload["id"]})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 로그인 체크, 닉네임 반환 @금윤성
@app.route('/login/login_check', methods=['POST'])
def login_check():
    check_done_receive = request.form['check_done_give']
    check_id_receive = request.form['check_id_give']
    user = db.users.find_one({'username': check_id_receive})
    if  check_done_receive == 'success':
        return jsonify({'nickname' : user['nickname']})


@app.route('/index/addnick', methods=['POST'])
def add_nick():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    nickname = payload['nickname']

    return jsonify({'nick' : nickname})

# 회원가입 페이지 @금윤성
@app.route('/register')
def register():
    return render_template("register.html")

# 회원가입 명령 @금윤성
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

# 기존에 있는 아이디인지 확인 @금윤성
@app.route('/register/check_dup', methods=['POST'])
def check_dup():

    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

    # if result is not None:
    #     payload = {
    #         'id': username_receive,
    #         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
    #     }
    #     token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    #     return jsonify({'result': 'success', 'token': token})
    # # 찾지 못하면
    # else:
    #     return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
