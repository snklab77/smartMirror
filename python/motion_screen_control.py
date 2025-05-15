#!/usr/bin/env python3

from gpiozero import MotionSensor
from time import time, sleep
import os
os.environ["DISPLAY"] = ":0"

pir = MotionSensor(18)
last_motion = time()
display_on = False
OFF_DELAY = 300  # 秒（例：5分）

def turn_display(on: bool):
    global display_on
    if display_on == on:
        return
    # cmd = "xset dpms force on" if on else "xset dpms force off"これだとチラつく
    cmd = (
        "xrandr --output HDMI-1 --auto"
        if on else
        "xrandr --output HDMI-1 --off"
    )
    os.system(cmd)
    print(f"{'ON' if on else 'OFF'} at {time()}")
    display_on = on

print("センサー監視開始...")

while True:
    if pir.motion_detected:
        last_motion = time()
        turn_display(True)
    elif time() - last_motion > OFF_DELAY:
        turn_display(False)
    sleep(1)