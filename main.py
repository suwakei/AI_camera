from printxl import printXl
from flask import Flask, render_template
import sqlite3
from reco import reco # main.pyを実行したときなぜかreco()が二回連続実行されてしまうバグの修正
import datetime


date = datetime.datetime.now()
hour = date.hour
minutes = date.minute
sec = date.second

entry = f"{hour}時{minutes}分{sec}秒"


db = "students"
# DBを作成する（既に作成されていたらこのDBに接続する)
dbname = f"./database/{db}.db"
conn = sqlite3.connect(dbname)
#SQLiteを操作するためのカーソル,コントローラー
cur = conn.cursor()
#データベース内の表示
info = []
records = cur.execute("SELECT * FROM students")
for record in records:
    info.append(list(record))
#print(info)
# コミットしないと登録が反映されない

conn.commit()

key = ["学籍番号", "名前", "出席", "遅刻", "早退"]
stdlist = [dict(zip(key,item)) for item in info]#keyとinfoをまとめて辞書型にする


app = Flask(__name__)
#トップページ
@app.route("/", methods=["GET","POST"])
def top():
    return render_template("/displaydb.html", stdlist = stdlist)#stdlistはdb内の情報が辞書型で入っている変数



printXl(db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)






