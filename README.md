# Smart Mirror

A lightweight HTML/CSS/JS-based smart mirror UI for Raspberry Pi Zero 2 W. Displays clock, weather, and optionally controls display power using a motion sensor.

Raspberry Pi Zero 2 W 用の軽量HTML/CSS/JS製スマートミラーUIです。時刻や天気を表示し、人感センサーと連動させることも可能です。  

主に日本国内の日本語話者向けに書いていますが少しカスタムすればどこの国の方でも使って頂けると思います。

世間ではraspberry pi 4/5を使ったスマートミラーの情報が多くありますが、私のように安価なRaspberry Pi Zero 2 Wを使いたい方もいると思います。  
(ラズパイ4/5だとsmart mirror用途では少しオーバースペックすぎるし、高すぎる)  
小さいのでミラー裏にうまく仕込むにも適しています。  

ただし、chromium等重いブラウザを使うにはメモリもCPUも貧弱なので可能な限り軽量なツールを使う用に工夫しました。

プログラムは主にjs + html + cssを使って書いています。  
重いフレームワーク等は使わずプレーンなコードを心掛けました。  
pythonはhttpサーバーと人感センサーの制御に使用しています。  


<img src="./docs/images/SmartMirror.png" width="400" alt="Smart Mirror Preview">


## リポジトリ / Repository

### クローン方法 / How to Clone

HTTPSを使用する場合:
```bash
git clone https://github.com/snklab77/smartMirror.git
```

SSHを使用する場合:
```bash
git clone git@github.com:snklab77/smartMirror.git
```

## 機能 / Features

- 時刻表示 (clock.js)
- 天気情報表示 (weather.js + WeatherAPI.com)
- 人感センサー連動でディスプレイON/OFF (sensor.js)
- 背景黒 + シンプルUI

## システム要件 / Requirements

- Raspberry Pi Zero 2 W
- Raspberry Pi OS (64bit)
- Node.js
- WeatherAPI.com API key
- Python 3.x
- GPIO関連パッケージ（gpiozero）

## インストール / Installation

1. リポジトリのクローン:
```bash
git clone https://github.com/snklab77/smartMirror.git
cd smartMirror
```

2. 依存関係のインストール:
```bash
npm install
pip3 install gpiozero
```

3. 環境設定ファイルの作成:
   `example.env-config.js` を `env-config.js` にコピーして編集:
```javascript
const ENV = {
  WEATHERAPI_KEY: "YOUR-API-KEY-HERE",
  LOCATION: {
    lat: 35.681143654455774, // google mapで取得した設置予定場所緯度
    lon: 139.76749021382773, // google mapで取得した設置予定場所経度
    name: "品川区" // 現在未使用ですが、現在地を表示する場合に使用
  }
};
```
今回天気予報APIはWeatherAPI.comを使用しています。  
APIキーは[こちら](https://www.weatherapi.com/)から取得してください。


4. 必要なPythonスクリプトを配置:
   - `motion_screen_control.py` を `/usr/local/bin/` に配置
   - `smartmirror_server.py` を `/usr/local/bin/` に配置
   - 実行権限を付与:
```bash
sudo chmod +x /usr/local/bin/motion_screen_control.py
sudo chmod +x /usr/local/bin/smartmirror_server.py
```

## セットアップガイド / Setup Guide

### 1. ブートコンフィグの設定

`/boot/firmware/config.txt` に以下を追加:
```ini
dtoverlay=vc4-fkms-v3d
```

### 2. X設定

`~/.xinitrc` の設定:
```sh
#!/bin/sh
export DISPLAY=:0
export LANG=ja_JP.UTF-8
xrandr --output HDMI-1 --rotate right # 画面回転させない場合は不要
xset s off
xset +dpms
xset -dpms
xset s noblank
unclutter -idle 0 &
matchbox-window-manager -use_titlebar no &
/usr/bin/python3 /usr/local/bin/motion_screen_control.py &
/usr/bin/python3 /usr/local/bin/smartmirror_server.py &
luakit -U http://localhost:8000
sleep infinity
```

### 3. 自動起動の設定

`/etc/systemd/system/smartmirror-xinit.service`:
```service
[Unit]
Description=Start X session for Smart Mirror
After=network.target

[Service]
User=[your username]
WorkingDirectory=/home/[your username]
ExecStart=/usr/bin/startx
Restart=on-failure
RestartSec=5
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/[your username]/.Xauthority
StandardOutput=journal
StandardError=journal
Type=simple

[Install]
WantedBy=multi-user.target
```

サービスの有効化:
```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable smartmirror-xinit.service
```

## GPIOピン配置 / GPIO Pin Configuration

今回3pinのRen He AM312 焦電型 ミニ 人体赤外線感応モジュールと言うものを使いました
- VCC: 3.3V (ピン1)
- GND: GND (ピン6)
- 人感センサー（動作検知用）: GPIO17 (ピン11)

## 制限事項 / Known Issues

- luakitの一部バージョンで、ステータスバーやURL表示が再描画される場合があります
- 将来的に`--notabs` `--no-configuration`フラグの使用や、他ブラウザ（`uzbl`, `surf`など）への移行を検討中
- センサーの初期化に2秒程度かかる場合があります

## ライセンス / License

MITライセンスにするのでお好きに改変してご利用くださいませ。  


MIT License
```