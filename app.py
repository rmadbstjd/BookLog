from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

import certifi

# import requests

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.plrlvlp.mongodb.net/?retryWrites=true&w=majority' , tlsCAFile=certifi.where())
db = client.spart_week1


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

