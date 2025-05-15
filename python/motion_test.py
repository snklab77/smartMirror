# File Name: motion_test.py
# OS側でpy稼働環境があることが前提なのでここではパッケージエラー等が出る想定(無問題)
from gpiozero import MotionSensor
from time import sleep

pir = MotionSensor(17)  # GPIO17 = ピン11

print("センサー起動中... (2秒程度安定化にかかる場合あり)")

while True:
    pir.wait_for_motion()
    print("🔴 動きを検出！")

    pir.wait_for_no_motion()
    print("⚪ 動きなし")
