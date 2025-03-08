import pandas, numpy
import boto3, csv
import os, logging
import pymysql, smtplib
from cocacola import calc_price, plot_graph
from demographic import *

# get the list of the path from a csv file.
def df_listup(path):
    csv_list = pandas.read_csv(r'{}\OwnLearning\Python\DataAnalycs\practice_plan2\csv_list.csv'.format(path))
    df_list = {}
    separator = "/" # create the full path to the csv file reading a csv file
    for index, row in csv_list.iterrows():
        df_list[row[1]] = separator.join([row[0], row[1], row[2]]) # dictionary: folder, full path
    return df_list


def insert_data():
    chk = "Select * from sqlite_master where type=%"
    for index, row in df.iterrows():    
        #print(row['name'], row['age'], row['city'])
        sql = "INSERT INTO sample (name, age, city) VALUES (%s, %s, %s)"
        chk = cur.execute(chk, row['name'] , row['age'], row['city'])
        
        if chk == 0:
            success = success + 1
        else:
            fail = fail + 1
        # カウント入れていく。
    success_chk_list = {'number of success query': success, 'number of fail': fail}
    return success_chk_list

def send_mail(gmail_address, gmail_pw, port, yourchoice):
    
    if yourchoice == 'y':
        logging.info('メール送信処理を開始します。')
        try:
            # メールの内容(SSMから取得)
            from_address = gmail_address
            to_address = gmail_address
            subject = "Data analysis report"
            bodyText = "Here's your data analysis report."
            inquiry_category = "Data analysis"
            attachments = []
        except Exception as e:
            logging.error('メールの内容をSSMから取得できませんでした。{}'.format(e))
            
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', port) as smtp_server:
                smtp_server.login(gmail_address, gmail_pw)
                message = 'Subject: {}\n\n{}'.format(subject, bodyText)
                smtp_server.sendmail(from_address, to_address, message)
            logging.info('正常にメール送信完了')
        except Exception as e:
            logging.error('メール送信処理でエラーが発生しました。{}'.format(e))
    else:
        logging.info('メール送信処理を中止します。')


# Send the mail to my gmail server
if __name__ == "__main__":

    try:
        logging.info("SSMパラメータ取得開始します。")
        ssm_client = boto3.client('ssm', region_name='ap-southeast-2')
        
        db_name = ssm_client.get_parameter(Name='db_dbname', WithDecryption=True)['Parameter']['Value']
        db_tbl = ssm_client.get_parameter(Name='db_tablename', WithDecryption=True)['Parameter']['Value']
        db_usrname = ssm_client.get_parameter(Name='db_username', WithDecryption=True)['Parameter']['Value']
        db_pw = ssm_client.get_parameter(Name='db_pw', WithDecryption=True)['Parameter']['Value']
        path = ssm_client.get_parameter(Name='folder_path', WithDecryption=True)['Parameter']['Value']
        
        gmail_addr = ssm_client.get_parameter(Name='my_main_gmail_address', WithDecryption=True)['Parameter']['Value']
        gmail_pw = ssm_client.get_parameter(Name='my_main_gmail_password', WithDecryption=True)['Parameter']['Value']
    except Exception as e:
        logging.error('SSMパラメータの取得に失敗しました。{}'.format(e))
    
    #read the csv file contains the csv path to create the dataframe and create its list.
    df_list = df_listup(path)
    current_file_path, cur = os.path.dirname(__file__)
    
    logging.info("データベースへの接続開始します。")
    try:
        conn = pymysql.connect(
            host='localhost', 
            user=db_usrname, 
            password=db_pw, 
            db=db_name, 
            charset='utf8'
            )
        cur = conn.cursor()
    except Exception as e:
        logging.error('データベースへの接続失敗: {}'.format(e))

    for key, value in df_list.items():
        print(f"Processing...{key}")
        print('--------------------------------')

        if ('coca-cola' in key) == True:
            replace_num = [1, 2, 3, 4, 5, 6]
            
            # 複数のパスがあり、辞書型ではそのまま入らないため、"_1"等で辞書型に格納。
            # パスが合わないため、数字部分の削除を行う
            for num in replace_num:
                if ("_" + str(num) in value) == True:
                    value = value.replace(("_" + str(num)), "")
            df = pandas.read_csv(value)
            
            if ('KO' in value) == True and ('price' in value) == True:
                dict = calc_price(df, "open") #戻し値として、成功した数、失敗した数を返す。
                plot_graph(dict, "Coca_open_price", current_file_path, cur, cur)
                
                dict = calc_price(df, "high")
                plot_graph(dict, "Coca_high_price", current_file_path, cur)
                
                dict = calc_price(df, "low")
                plot_graph(dict, "Coca_low_price", current_file_path, cur)
                
                dict = calc_price(df, "close")
                plot_graph(dict, "Coca_close_price", current_file_path, cur)
                
            elif ('PEP' in value) == True and ('price' in value) == True:
                dict = calc_price(df, "open") #戻し値として、成功した数、失敗した数を返す。
                plot_graph(dict, "PEP_open_price", current_file_path, cur)
                
                dict = calc_price(df, "high")
                plot_graph(dict, "PEP_high_price", current_file_path, cur)
                
                dict = calc_price(df, "low")
                plot_graph(dict, "PEP_low_price", current_file_path, cur)
                
                dict = calc_price(df, "close")
                plot_graph(dict, "PEP_close_price", current_file_path, cur)
        else: 
            df = pandas.read_csv(value)
            
            if ('Ai' in key) == True:
                print("AAA")
            
            elif ('demographic' in key) == True:
                # County,State,State FIPS Code,County FIPS Code,FIPS,Total Population,Male Population,Female Population,Total Race Responses,White Alone,Black or African American Alone,Hispanic or Latino
                dict = demographic(df)
                plot_graph_graphic(dict, "demographic", current_file_path, cur)
                
            elif ('internet' in key) == True:
                print("AAA")
                
            elif ('laptop' in key) == True:
                print("AAA")
                
            elif ('sleep' in key) == True:
                print("AAA")
                
            elif ('user' in key) == True:
                print("AAA")
                
            elif ('population' in key) == True:
                print('AAA')
    
    send_option = input("Send mail?(y/n): ")
    
    send_mail(gmail_addr, gmail_pw, 465, send_option)
        # function呼び出す(別ファイルにするとか)
        #print(df)
        
    # 最終的にメール送る。
    # CSVファイルを10個ほどダウンロードして、調整してデータベースに入れる。グラフ化もしてみる。
    