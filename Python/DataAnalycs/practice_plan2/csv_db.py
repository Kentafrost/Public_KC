import pandas, numpy
import csv
import logger
import pymysql
import smtplib
import os
from cocacola import calc_price, plot_graph
from demographic import demographic

# get the list of the path from a csv file.
def df_listup():
    csv_list = pandas.read_csv(r'C:\Users\kenta\OneDrive\Public_Github\Public_KC\Python\DataAnalycs\practice_plan2\csv_list.csv')
    df_list = {}
    
    # create the full path to the csv file reading a csv file
    separator = "/"
    
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

def send_mail():
    logger.info('メール送信処理を開始します。')
    try:
        # メールの内容(SSMから取得)
        from_address = "your_gmail@gmail.com"
        to_address = "your_gmail@gmail.com"
        subject = "Data analysis report"
        bodyText = "Here's your data analysis report."
        inquiry_category = "Data analysis"
        attachments = []    
        smtplib.send_mail(to_address, subject, bodyText, attachments)
        logger.info('正常にメール送信完了')
    
    except Exception as e:
        logger.error('メール送信処理でエラーが発生しました。{}'.format(e))


# Send the mail to my gmail server
if __name__ == "__main__":
    #read the csv file contains the csv path to create the dataframe and create its list.
    df_list = df_listup()
    current_file_path = os.path.dirname(__file__)
    
    # SSMパラメータからデータ抜き取る方式に変える予定
    conn = pymysql.connect(host='localhost', user='KenFrost', password='asoeeaoiHSOwq1', db='TESTDB', charset='utf8')
    cur = conn.cursor()

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
                dict = calc_price(cur, df, "open") #戻し値として、成功した数、失敗した数を返す。
                plot_graph(dict, "Coca_open_price", current_file_path)
                
                dict = calc_price(cur, df, "high")
                plot_graph(dict, "Coca_high_price", current_file_path)
                
                dict = calc_price(cur, df, "low")
                plot_graph(dict, "Coca_low_price", current_file_path)
                
                dict = calc_price(cur, df, "close")
                plot_graph(dict, "Coca_close_price", current_file_path)
                
            elif ('PEP' in value) == True and ('price' in value) == True:
                dict = calc_price(cur, df, "open") #戻し値として、成功した数、失敗した数を返す。
                plot_graph(dict, "PEP_open_price", current_file_path)
                
                dict = calc_price(cur, df, "high")
                plot_graph(dict, "PEP_high_price", current_file_path)
                
                dict = calc_price(cur, df, "low")
                plot_graph(dict, "PEP_low_price", current_file_path)
                
                dict = calc_price(cur, df, "close")
                plot_graph(dict, "PEP_close_price", current_file_path)
                
        elif ('Ai' in key) == True:
            print("AAA")
            
        elif ('demographic' in key) == True:
            # County,State,State FIPS Code,County FIPS Code,FIPS,Total Population,Male Population,Female Population,Total Race Responses,White Alone,Black or African American Alone,Hispanic or Latino
            #demographic(df)
            print("AAA")
            
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
        
        # function呼び出す(別ファイルにするとか)
        #print(df)
        
    # 最終的にメール送る。
    # CSVファイルを10個ほどダウンロードして、調整してデータベースに入れる。グラフ化もしてみる。
    