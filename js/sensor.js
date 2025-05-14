// Raspberry Pi Zero 2 W 用：人感センサー GPIO 制御
// node.js + pigpio または onoff パッケージが前提

const Gpio = require("onoff").Gpio;
const sensor = new Gpio(17, "in", "both"); // GPIO17 を使用（必要に応じて変更）

sensor.watch((err, value) => {
  if (err) {
    console.error("センサーエラー:", err);
    return;
  }

  if (value === 1) {
    console.log("人を検知 → ディスプレイON");
    require("child_process").exec("vcgencmd display_power 1");
  } else {
    console.log("人がいなくなった → ディスプレイOFF");
    require("child_process").exec("vcgencmd display_power 0");
  }
});

process.on("SIGINT", () => {
  sensor.unexport();
  process.exit();
});
