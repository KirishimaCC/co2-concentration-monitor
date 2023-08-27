from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import os
from datetime import datetime
import time
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)

socketio = SocketIO(app)
current_value = 0  # 更新する値

#SocketIO
@socketio.on("currentData")
def recievedata(currentData):
    socketio.emit("update", currentData, namespace="/")

#アクセス時に最新順のデータ取得
queryAccess = "SELECT * FROM data ORDER BY timestamp DESC LIMIT 60;"
queryUpdate = "SELECT * FROM data ORDER BY timestamp DESC LIMIT 1;"

@socketio.on("requestLatestData")
def getLatestData():
    conn = sqlite3.connect('/home/kirishima/Co2Monitor/instance/co2Data.db')
    cursor = conn.cursor()

    cursor.execute(queryAccess)
    dataList = cursor.fetchall()
    conn.close()
    co2datalist = [co2data[1] for co2data in dataList]
    timedatalist = [timedata[3].split("T")[1] for timedata in dataList]
    co2datalist.reverse()
    timedatalist.reverse()
    AveData = [co2datalist, timedatalist]

    socketio.emit("getLatestData", AveData)

@socketio.on("updateData")
def updateData(updateData):
    socketio.emit("updateData", updateData, namespace="/")

#ルーティング
@app.route("/")
def main():
    return render_template("main.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, host="192.168.1.20", port=5000)