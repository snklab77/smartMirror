#!/usr/bin/env python3

from gpiozero import MotionSensor
from time import time, sleep
import os
import sys

try:
    os.environ["DISPLAY"] = ":0"
    pir = MotionSensor(17, queue_len=1, threshold=0.5) # GPIO17 = ピン11
    last_motion = time()
    display_on = True
    OFF_DELAY = 300  # 秒（例：5分）
    RECOVERY_THRESHOLD = 600  # 無反応で再起動（例：10分）

    def turn_display(on: bool):
        global display_on
        if display_on == on:
            return
        cmd = (
            "DISPLAY=:0 xset dpms force on"
            if on else
            "DISPLAY=:0 xset dpms force off"
        )
        os.system(cmd)
        print(f"{'ON' if on else 'OFF'} at {time()}", flush=True)
        display_on = on

    print("センサー監視開始...", flush=True)

    # ✅ イベントで last_motion を更新
    def update_last_motion():
        global last_motion
        last_motion = time()
    pir.when_no_motion = update_last_motion

    while True:
        now = time()

        # ✅ イベントから1秒以内なら反応があったとみなす
        if now - last_motion < 1:
            turn_display(True)
        elif now - last_motion > OFF_DELAY:
            turn_display(False)

        if not display_on and (now - last_motion > RECOVERY_THRESHOLD):
            print("[INFO] 無反応時間が閾値を超過 → 自己再起動します", flush=True)
            os.execv(sys.executable, ['python3'] + sys.argv)

        sleep(1)

except Exception as e:
    print(f"[ERROR] {e}", file=sys.stderr)
    raise
