# Smart Mirror

A lightweight HTML/CSS/JS-based smart mirror UI for Raspberry Pi Zero 2 W. Displays clock, weather, and optionally controls display power using a motion sensor.

Raspberry Pi Zero 2 W 用の軽量HTML/CSS/JS製スマートミラーUIです。時刻や天気を表示し、人感センサーと連動させることも可能です。

---

## Features / 機能

- 時刻表示 (clock.js)
- 天気情報表示 (weather.js + WeatherAPI.com)
- 人感センサー連動でディスプレイON/OFF (sensor.js)
- 背景黒 + シンプルUI

---

## Requirements / 動作環境

- Raspberry Pi Zero 2 W
- Raspberry Pi OS (64bit)
- Chromium (kiosk mode)
- Node.js (for sensor.js only)
- WeatherAPI.com API key

---

## Installation / インストール

1. Clone this repository:

```bash
git clone https://github.com/snklab77/smartMirror.git
```

2. Install dependencies:

```bash
cd smartMirror
npm install
```

3. Create your API key file:

```js
// cp config/example.env-config.js config/env-config.js
const ENV = {
  WEATHER_API_KEY: "your-api-key"
};
```

4. Set up Chromium kiosk mode or autostart index.html

5. Optional: Run motion detection script

```bash
sudo node js/sensor.js
```

---

## License

MIT License