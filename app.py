from dataclasses import dataclass
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import requests
import json


app = Flask(__name__)

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

# (미완성) naverapi에서 검색어 불러오는 코드  (한글 인코딩 문제 있음 ㅠ)
@app.route('/api/<isbn>')
def find_bookdetail_via_isbn(isbn):
    
    # /api/call-bookinfo URL로 POST 방식으로 도착한 데이터
    print(isbn.split()[-1])
    header_info = {"X-Naver-Client-Id": "0g0WhKXaBnkuD7TS7sEC", "X-Naver-Client-Secret": "EV_4uF2dqi"}
    r = requests.get('https://openapi.naver.com/v1/search/book_adv.xml?d_isbn='+str(isbn.split()[-1]), headers=header_info)
    result = r.json()
    print(result)
    
    return render_template("edit-page.html", isbn=result)

# (미완성) naverapi에서 검색어 불러오는 코드  (한글 인코딩 문제 있음 ㅠ)
@app.route('/api/call-bookinfo', methods=['POST'])
def give_bookInfo():

    data = str(request.data)
    print(data)
    
    # /api/call-bookinfo URL로 POST 방식으로 도착한 데이터
    header_info = {"X-Naver-Client-Id": "0g0WhKXaBnkuD7TS7sEC", "X-Naver-Client-Secret": "EV_4uF2dqi"}

    r = requests.get('https://openapi.naver.com/v1/search/book.json?query=데이터', headers=header_info)
    result = r.json()
    
    return result

# 작성된 리뷰를 저장
@app.route('/save-review', methods=['POST'])
def save_review():

    # /save-review URL로 POST 방식으로 들어올 때 전달받은 콘텐츠를 각 변수에 저장
    booktitle = request.form['booktitle_give']
    review_content = request.form['review_content_give']
    imgfile = request.files["imgfile_give"]
    print("test-log", booktitle, review_content)
    
    # 책 이미지 파일을 static 폴더에 저장
    extension = imgfile.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}'
    imgfile.save(f'static/books_pic/{filename}.{extension}')
    
    print("test-log", filename, mytime, extension)

    doc = {
        'title':booktitle,
        'content':review_content,
        'file': f'{filename}.{extension}',
        'time': today.strftime('%Y.%m.%d')
    }
    
    print("test-log: doc 생성 완료")

    db.review_test.insert_one(doc)

    return jsonify({'msg': '책 리뷰 저장 완료!'})


# 로그인페이지 @금윤성
@app.route('/login')
def login():
    return render_template("login.html")

# 회원가입 페이지 @금윤성
@app.route('/register')
def register():
    return render_template("register.html")


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

