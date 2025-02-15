from flask import Flask, render_template, request, url_for
import requests
import pymysql
from werkzeug.exceptions import NotFound,BadRequest,InternalServerError
import logger

#flaskでWEBサイト作る用。

#ここでどこのフォルダを参照して画像データ、CSSを取得するか指定できる。
app = Flask(__name__, static_folder='./static')

#入力したユーザー名をmainに渡す
usrname = input("Type the username:")
#pw = input("Type the password::")

def msg_url():

    print("Info: You can access the webpage via the URL below")
    real_url = (('/') + usrname)
    return real_url

#PWでのアクセス制限。
#def msg_url():
#    if pw != "AAAA":
#        print("Access Denied")
#        exit()

#    else:
#        print("Info: You can access the webpage via the URL below")
#        real_url = (('/') + usrname)
#        return usrname, real_url

#URLを表示する。
print("--------------------------------")
print(("http://127.0.0.1:5000" + msg_url()))
print("--------------------------------")

url = (("/")+ usrname)

#mainページ
@app.route(url, methods=['Get'])

def main():
    title = 'ゆっくりしていってね!!!'
    method_type = request.method
    return render_template('top_page.html', title=title, method_type=method_type, name=usrname)


#明治維新
@app.route('/history_meiji_restoration', methods=['Get'])

def history_meiji():
    title ="明治維新"
    #本ファイルの変数を渡しつつtemplate配下のHTMLファイルを呼び出す。
    return render_template("history_explaination/block/block_meiji_restoration.html", title=title, name=usrname)


#江戸時代
@app.route('/edo', methods=['Get'])

def history_edo():
    title ="江戸時代"
    #本ファイルの変数を渡しつつtemplate配下のHTMLファイルを呼び出す。
    return render_template("history_explaination/edo.html", title=title, name=usrname)


@app.route('/video', methods=['Get'])

def video_page():
    title = '動画まとめページ'
    return render_template('video_page.html', title=title, name=usrname)


'''エラーハンドリング(エラーに応じて、渡し値を調整可能)'''
@app.errorhandler(BadRequest)
@app.errorhandler(NotFound)
@app.errorhandler(InternalServerError)

def error_handler(error):
    error_res = error.name
    error_description = error.description
    
    return render_template('./common/page_not_found.html', error_res=error_res, error_description=error_description)

if __name__ == '__main__':
    app.run(debug=True)