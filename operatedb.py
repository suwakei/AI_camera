from printxl import createUserForm
import sqlite3
import datetime
import tkinter as tk
import tkinter.messagebox as tmsg
import glob
import os


def now():#現在時刻を出す関数
    dt_now = datetime.datetime.now()#現在時刻
    return dt_now.strftime('%H時%M分')


#DBの更新をするプログラムです
"""
tkinterでdb内の閲覧や情報の更新ができるようにする
"""


window = tk.Tk()
window.geometry("700x500")
window.title("データベース設定")

# 遷移前の画面の作成                                                            
top_page = tk.Canvas(width=800, height=800)
top_page.place(x=0, y=0) # キャンバス



top_label =  tk.Label(window, text = "項目を選んでください", font = ("Helvetica", 10))
top_label.place(x=270, y=10)

btn_createdb = tk.Button(window,text = "データベースの新規作成", command = lambda:run_createdb(top_page))
btn_createdb.place(x=100, y=150)

#データベースの新規作成
def run_createdb(widget):
    widget.place_forget()
    # ウィンドウの作成                                                              

    # 遷移前の画面の作成                                                            
    def_newdb = tk.Canvas(width=800, height=800)
    def_newdb.place(x=0, y=0) # キャンバス

    #新規DBの名前を入力するテキストボックスの処理
    dbname_label = tk.Label(def_newdb, text = "新規作成するデータベースの名前を入力してください", font = ("Helvetica", 10))
    dbname_label.place(x=80, y=10)
    dbname_value = tk.Entry(width=20)
    dbname_value.place(x=175, y=30)

    #新規主キーの名前を入力するテキストボックスの処理
    prikey_label = tk.Label(def_newdb, text = "主キーを入力してください", font = ("Helvetica", 10))
    prikey_label.place(x=80, y=60)
    prikey_value = tk.Entry(width=20)
    prikey_value.place(x=175, y=80)
    #新規サブキー1

    subkey1_label = tk.Label(def_newdb, text = "サブキー1を入力してください", font = ("Helvetica", 10))
    subkey1_label.place(x=80, y=110)
    subkey1_value = tk.Entry(width=20)
    subkey1_value.place(x=175, y=130)
    #新規サブキー2

    subkey2_label = tk.Label(def_newdb, text = "サブキー2を入力してください", font = ("Helvetica", 10))
    subkey2_label.place(x=80, y=160)
    subkey2_value = tk.Entry(width=20)
    subkey2_value.place(x=175, y=180)
    #新規サブキー3

    subkey3_label = tk.Label(def_newdb, text = "サブキー3を入力してください", font = ("Helvetica", 10))
    subkey3_label.place(x=80, y=210)
    subkey3_value = tk.Entry(width=20)
    subkey3_value.place(x=175, y=230)
    #新規サブキー4

    subkey4_label = tk.Label(def_newdb, text = "サブキー4を入力してください", font = ("Helvetica", 10))
    subkey4_label.place(x=80, y=260)
    subkey4_value = tk.Entry(width=20)
    subkey4_value.place(x=175, y=280)
    #次のページへの処理

    def_new_db_btn = tk.Button(def_newdb,text = "次へ", command = lambda:btn_click_to_confirm(def_newdb))
    def_new_db_btn.place(x=175, y=340)

    def btn_click_to_confirm(widget):
        widget.place_forget() # def_newdbを隠す

        #入力されたデータベース名を取得
        global def_dbname
        def_dbname = dbname_value.get()
        
        #入力された主キーを取得
        global def_prikey
        def_prikey = prikey_value.get()
        #入力されたサブキー1を取得
        global def_subkey1
        def_subkey1 = subkey1_value.get()
        #入力されたサブキー2を取得
        global def_subkey2
        def_subkey2 = subkey2_value.get()
        #入力されたサブキー3を取得
        global def_subkey3
        def_subkey3 = subkey3_value.get()
        #入力されたサブキー4を取得
        global def_subkey4
        def_subkey4 = subkey4_value.get()

        #新しい画面を作る
        global def_confirm
        def_confirm = tk.Canvas(width=800, height=800)
        def_confirm.place(x=0, y=0)

        #新規作成するDBの確認
        p = tk.Label(def_confirm, text="この内容で新規作成します", font = ("Helvetica", 9))
        p.place(x=300, y=10)
        preview = tk.Label(def_confirm, text=f"DB名:{def_dbname} ,主キー:{def_prikey} ,サブキー1:{def_subkey1} ,サブキー2:{def_subkey2} ,サブキー3:{def_subkey3} ,サブキー4:{def_subkey4}", font = ("Helvetica", 9))
        preview.place(x=10, y=100)
        #次のページへの処理
        def_container_btn = tk.Button(window,text = "確定", command = lambda:quit(def_newdb))
        def_container_btn.place(x=175, y=340)

        def quit(widget):
            widget.quit()#ここは実行されている
        

        try:
            #今まで入力した情報でDBを新規作成する
            new_db = f"./database/{def_dbname}.db"

            #ここで同じ名前のdbが存在してたらいったん削除する
            if os.path.exists(f"./database/{def_dbname}.db"):
                os.remove(f"./database/{def_dbname}.db")

            # DBを作成する（既に作成されていたらこのDBに接続する)
            conn = sqlite3.connect(new_db)

            #SQLiteを操作するためのカーソル,コントローラー
            cur = conn.cursor()
            
            #テーブルの作成
            cur.execute(f"CREATE TABLE IF NOT EXISTS {def_dbname}({def_prikey} STRING PRIMARY KEY , {def_subkey1} STRING, {def_subkey2} STRING, {def_subkey3} STRING, {def_subkey4} STRING)") 
            
            # コミットしないと登録が反映されない
            conn.commit()
            tmsg.showinfo("OK","正常に作成されました")
        except sqlite3.OperationalError:
            print(def_dbname)
            tmsg.showinfo("エラー","重複しているキーがあるか数字など使用不可のキーを使っています")#空欄を満たせていないときもエラーなため要改善
            #PermissionErrorによりしっぱいしたdbを削除できないため要改善



btn_operatedb = tk.Button(window,text = "生徒情報登録", command = lambda:run_operatedb(top_page))
btn_operatedb.place(x=280, y=150)



#作成済みテーブルに値を挿入する値を挿入した時にエクセルに転記する
def run_operatedb(widget):
    widget.place_forget()
    operateTop_page = tk.Canvas(width=800, height=800)
    operateTop_page.place(x=0, y=0) # キャンバス
    operateTop_label = tk.Label(window, text = "値入力するデータベースを選択してください", font = ("Helvetica", 10))
    operateTop_label.place(x=225, y=10)

        #dbを取り出す
    
    dbs = [os.path.basename(file) for file in glob.glob("./database/*.db")]

    btn = []
    #dbを一つずつ取り出す
    for index, db in enumerate(dbs):
        btn.append(db)
        dbBtn = tk.Button(window, text = db[:-3], command = operate_container(db[:-3]))
        dbBtn.place(x=250, y=40*(1+index))




##押されたボタンの情報を取得する方法は今度考える

#値入力するデータベース
def operate_container(inp_db):
    print(inp_db+"1")
    createUserForm()#登録用紙(Excel)作成
    
    operate_container_page = tk.Canvas(width=800, height=800)
    operate_container_page.place(x=0, y=0) # キャンバス

    operate_container_label = tk.Label(window, text = f"{inp_db}へエクセルファイルの生徒情報を入力します", font = ("Helvetica", 10))
    operate_container_label.place(x=225, y=10)

    

    input_db = f"./database/{inp_db}.db"

    # DBを作成する（既に作成されていたらこのDBに接続する)
    conn = sqlite3.connect(input_db)

    #SQLiteを操作するためのカーソル,コントローラー
    cur = conn.cursor()

    





btn_updatedb = tk.Button(window,text = "作成済みデータベースの編集", command = lambda:run_updatedb(top_page))
btn_updatedb.place(x=460, y=150)


#作成済みデータベースを操作する
def run_updatedb(widget):
    widget.place_forget()
    files = glob.glob("./database/*.db")
    for file in files:
        file[11:]
    
    updateTop_page = tk.Canvas(width=800, height=800)
    updateTop_page.place(x=0, y=0) # キャンバス
    updateTop_label = tk.Label(window, text = "編集するデータベースを選択してください", font = ("Helvetica", 10))
    updateTop_label.place(x=225, y=10)







window.mainloop()













# DBを作成する（既に作成されていたらこのDBに接続する
dbname ="./database/students.db"
conn = sqlite3.connect(dbname)
#SQLiteを操作するためのカーソル,コントローラー
cur = conn.cursor()

conn.commit()












