#!/usr/bin/env python3

from gpiozero import MotionSensor
from time import time, sleep
import os
import sys

try:
    os.environ["DISPLAY"] = ":0"
    pir = MotionSensor(17) # GPIO17 = ピン11
    last_motion = time()
    display_on = True
    OFF_DELAY = 300  # 秒（例：5分）

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
        print(f"{'ON' if on else 'OFF'} at {time()}")
        display_on = on

    print("センサー監視開始...", flush=True)

    while True:
        if pir.motion_detected:
            last_motion = time()
            turn_display(True)
        elif time() - last_motion > OFF_DELAY:
            turn_display(False)
        sleep(1)

except Exception as e:
    print(f"[ERROR] {e}", file=sys.stderr)
    raise