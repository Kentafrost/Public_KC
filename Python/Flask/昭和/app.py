from flask import Flask, render_template, request, url_for
import pymysql as py, pandas as pd
from botocore.exceptions import ClientError
from werkzeug.exceptions import NotFound,BadRequest,InternalServerError
from logger import logging
import boto3
from datetime import datetime

# メール送信用
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import matplotlib.pyplot as plt

# date
now = datetime.now()
date = now.strftime("%d/%m/%Y %H:%M:%S")
dt_hour = now.strftime("%H:%M:%S")

# 時間ごとのメッセージ
if dt_hour >="00:00:00":
    MSG_hour ="夜遅くまでお疲れ様です。"
elif dt_hour >= "03:00:00":
    MSG_hour = "夜更かしでしょうか。"
elif dt_hour >= "07:00:00":
    MSG_hour = "おはようございます"
elif dt_hour >= "12:00:00":
    MSG_hour = "こんにちは"
elif dt_hour >= "17:00:00":
    MSG_hour = "こんばんは"
elif dt_hour >= "21:00:00":
    MSG_hour = "そろそろご就寝になられた方がよろしいのではないでしょうか。" 

REGION = 'ap-southeast-2' # Sydney Region

def get_parameters(param_key):
    ssm = boto3.client('ssm', region_name=REGION)
    response = ssm.get_parameters(
        Names=[
            param_key,
        ],
        WithDecryption=True
    )
    return response['Parameters'][0]['Value']

'AWS SSMからDBアクセス用、gmailアドレス等の機密データ取得'
try:
    db_id = get_parameters("db_username") 
    db_pw = get_parameters("db_pw")
    db_name = get_parameters("db_tablename")
    gmail_address = get_parameters("my_main_gmail_address")
    gmail_password = get_parameters("my_main_gmail_password") 
except Exception as e:
    logging.error("Error: Can't get data from AWS SSM")
    raise e

try:
    db = py.connect(host="localhost", user=db_id, password=db_pw, database=db_name)
except Exception as e:
    logging.error("database.connection Error")
    raise e



# DBから取得してグラフ化する
# def create_graph():
#     with db.cursor() as cursor:
#         cursor.execute("Select * from webdev_practice")
#         result = cursor.fetchall()
#         df = pd.Dataframe(result)
#         df.to_csv("./test_graph.csv")
        
#         plt.plot(df["date"], df["title"])
#         plt.savefig("./test.png")
#     db.close()

# SecretManager使ってみるとか
#PWでのHTMLへのアクセス制限。
#def msg_url():
#    if pw != "AAAA":
#        print("Access Denied")
#        exit()

#    else:
#        print("Info: You can access the webpage via the URL below")
#        real_url = (('/') + usrname)
#        return usrname, real_url

# gmailメール送信用
def send_email(fromAddress, toAddress, subject, bodyText, inquiry_category):
    try:
        # Access to SMTP mail server
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.starttls()
        smtpobj.login(gmail_address, gmail_password)
        # creating a mail
        msg = MIMEText(bodyText)
        msg['Subject'] = subject & "[" & inquiry_category & "]"
        msg['From'] = fromAddress
        msg['To'] = toAddress
        msg['Date'] = formatdate()
        # sending mail
        smtpobj.send_message(msg)
        smtpobj.close() 
        
    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")

#どこのフォルダを参照して画像データ、CSSを取得するか指定
app = Flask(__name__, static_folder='./static')

#入力したユーザー名をmain_pageに渡す
usrname = input("Type the username:")
print("Info: You can access the webpage via the URL below")
#pw = input("Type the password::")

#URLを表示する。
print("--------------------------------")
print(("http://127.0.0.1:5000" + '/') + usrname)
print("--------------------------------")
url = (("/")+ usrname)
title = 'ホームページ'


#mainページ
@app.route(url, methods=['Get'])

def main():    
    method_type = request.method
    return render_template('top_page.html', title=title, method_type=method_type, name=usrname, date=date, MSG=MSG_hour)

@app.route('/dunbine', methods=['Get'])
def dunbine():
    title ="聖戦士ダンバイン"
    return render_template("./showa_anime/block/block_dunbine.html", title=title, name=usrname)

@app.route('/votoms', methods=['Get'])
def votoms():
    title ="装甲機兵ボトムズ"
    return render_template("./showa_anime/block/block_votoms.html", title=title, name=usrname)

@app.route('/yamato', methods=['Get'])
def yamato():
    title ="宇宙戦艦ヤマト"
    return render_template("./showa_anime/block/block_yamato.html", title=title, name=usrname)

@app.route('/sampleform-post', methods=['POST'])
def sample_form_temp():
    if request.method == "Get":
        print("Get Method受領しました")
        
    if request.method == 'POST':
        print('POSTデータ受領、処理します。処理時刻: {%s}', (dt_hour)) # 日付入れる
        with db.cursor() as cursor:
            name= request.form.get('name') #HTMLファイルに入れたデータ
            mail= request.form.get('mail')
            text = request.form.get("questionaire")
            point = request.form.get('point')
            '同じデータ入ってないなら、入れる'
            select_result_tbl = "SELECT * from webdev_practice WHERE name=%s,  mail=%s, text=%s"
            insert_result_tbl = "INSERT INTO webdev_practice (name, mail, text) VALUES (%s, %s, %s)"
            
            cursor.execute(select_result_tbl, (name, mail, text))
            if cursor.fetchall() != "":
                print("既に登録されていますので、スキップします")
            else:
                cursor.execute(insert_result_tbl, (name, mail, text))
                db.commit()
                # 処理が正常に終了した場合、ログを書いておく。
                return f'正常に処理しました。データ入力情報は以下をご参照ください。名前: {name} メールアドレス: {mail} 回答内容: {text}。 画面をお閉じください。'
            # 50未満の場合、別ページに飛ばしたい。
            if point <= 50:
                return f'改善事項を頂ければ幸いです。'

# 以下、問い合わせ等の練習
@app.route('/inquiry_post', methods=['Get', 'POST'])
def inquiry():
    if request.method == 'POST':
        print('POSTデータ受領、処理します')
        #メール内容を調整する
        subject = 'Inquiry from User'
        fromAddress = request.form.get('Sender_Address') # 送信先
        bodyText = request.form.get('Inquiry_Post')
        inquiry_category = request.form.get('inquiry_category_pulldown')
        toAddress = gmail_address
    
        send_email(fromAddress, toAddress, subject, bodyText, inquiry_category) #メール送信用関数
        # 処理が正常に終了した場合、ログを書いておく。
        
        return f'正常にメール送信完了しました。画面をお閉じください。'


'''エラーハンドリング(エラーに応じて、渡し値を調整可能)'''
@app.errorhandler(BadRequest)
@app.errorhandler(NotFound)
@app.errorhandler(InternalServerError)

def error_handler(error):
    error_res = error.name
    error_description = error.description
    return render_template('./common/page_not_found.html', error_res=error_res, error_description=error_description)

if __name__ == '__main__':
    #host="0.0.0.0", port=5000を入れて、IP合わせればアクセスできるように
    app.run(host="127.0.0.1", debug=True) 