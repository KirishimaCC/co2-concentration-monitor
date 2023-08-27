import sqlite3
import socketio
import time
from datetime import datetime
import mh_z19

sio = socketio.Client()

#mh_z19からデータを取得
def getCo2Data(conn, cursor):
    dataList = []
    lastMinute = datetime.now().minute

    while True:
        #現在時刻（分）を取得
        currentMinute = datetime.now().minute

        #1分経過した場合の処理
        if lastMinute != currentMinute:
            lastMinute = currentMinute
            #データ数が30以上の場合：平均値を算出しdbに保存。リスト初期化
            if len(dataList) > 30:
                avgCo2 = sum(d["co2"] for d in dataList) // len(dataList)
                avgTemperature = sum(d["temperature"] for d in dataList) // len(dataList)
                currentTime = datetime.now().strftime('%Y-%m-%dT%H:%M')
                cursor.execute("INSERT INTO data (co2, temperature, timestamp) VALUES (?, ?, ?)", (avgCo2, avgTemperature, currentTime))
                conn.commit()
                #Chart.js更新用データを送信
                currentTime = currentTime.split("T")[1]
                sio.emit("updateData", {"co2": avgCo2, "timestamp": currentTime})
                dataList = []
            #データ数が30未満の場合：リスト初期化
            else:
                dataList = []
            
        #データを取得しリストに保存
        data = mh_z19.read_all()
        dataList.append(data)
        currentCo2 = data["co2"]
        currentTemperature = data["temperature"]
        currentTime = datetime.now().strftime('%Y年%m月%d日%H時%M分%S秒')
        sio.emit("currentData", {"co2": currentCo2, "temperature": currentTemperature, "time": currentTime})
        time.sleep(1)

if __name__ == "__main__":
    #データベースの作成
    conn = sqlite3.connect('/home/kirishima/Co2Monitor/instance/co2Data.db')  #データベースファイルが存在しない場合、新しく作成されます
    #カーソルの作成
    cursor = conn.cursor()
    #SQLクエリの実行
    cursor.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, co2 INTEGER, temperature INTEGER, timestamp STRING)')
    conn.commit()
    sio.connect("http://192.168.1.20:5000")
    getCo2Data(conn, cursor)
    conn.close()