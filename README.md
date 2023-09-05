# co2-concentration-monitor
CO2センサ「mh-z19」を使用し、CO2濃度を毎秒計測します。計測データから分平均を算出し、データベースに記録します。Flaskサーバにアクセスすることでデータを閲覧する事が出来ます。

※本プログラムは現在開発中の習作です。今後のアップデートではデータ閲覧機能の拡充を行います。また、同時並行で安定性の向上を図ってまいります。

##使用方法
①app.pyを実行します。②getDbData.pyを実行します。

[参考画像]Flaskサーバにアクセスした際の画面
「現在のCO2濃度」「現在の室温」「データ取得時刻」は毎秒更新。Chart.jsを使用したグラフは毎分更新。
![20230828](https://github.com/KirishimaCC/co2-concentration-monitor/assets/143318141/a455eaa6-ba38-439b-a84e-72e2cdbb84fe)


##使用した言語・技術・ライブラリ
Python3
Flask
SocketIO
sqlite3
datetime
time
os
mh_z19

JavaScript
Chart.js
