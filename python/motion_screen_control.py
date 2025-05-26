#!/usr/bin/env python3

from gpiozero import MotionSensor
from time import time, sleep
import subprocess
import os
import sys

try:
    os.environ["DISPLAY"] = ":0"

    print("センサー初期化中...", flush=True)
    pir = MotionSensor(17, queue_len=1, threshold=0.5)  # GPIO17 = ピン11
    sleep(5)
    last_motion = time()
    print("センサー監視開始...", flush=True)

    display_on = False
    OFF_DELAY = 300
    RECOVERY_THRESHOLD = 600


    def turn_display(on: bool):
        global display_on
        if display_on == on:
            return

        # dpms ON/OFF の前に luakit を停止/再開
        try:
            luakit_pid = subprocess.check_output(["pgrep", "-x", "luakit"]).decode().strip()
            if on:
                os.system(f"kill -CONT {luakit_pid}")
                print(f"[ACTION] luakit resumed (PID: {luakit_pid})", flush=True)
            else:
                os.system(f"kill -STOP {luakit_pid}")
                print(f"[ACTION] luakit suspended (PID: {luakit_pid})", flush=True)
        except subprocess.CalledProcessError:
            print("[WARN] luakit の PID が取得できませんでした", flush=True)

        cmd = (
            "DISPLAY=:0 xset dpms force on"
            if on else
            "DISPLAY=:0 xset dpms force off"
        )
        os.system(cmd)
        print(f"{'ON' if on else 'OFF'} at {time()}", flush=True)
        display_on = on


    def restart_luakit():
        try:
            subprocess.run(["pkill", "-f", "luakit"])
            subprocess.Popen(["luakit", "-U", "http://localhost:8000"], env={"DISPLAY": ":0"})
            print("[INFO] luakit を再起動しました", flush=True)
        except Exception as e:
            print(f"[ERROR] luakit 再起動失敗: {e}", flush=True)


    def update_last_motion():
        global last_motion
        print(f"[DEBUG] センサーイベント受信 → now: {now}", flush=True)
        last_motion = time()
        print(f"[EVENT] motion detected → last_motion updated: {last_motion}", flush=True)


    pir.when_motion = update_last_motion
    # pir.when_no_motion = update_last_motion

    while True:
        now = time()
        loop_check = int(now) % 30 == 0
        if loop_check:
            print(f"[LOOP] now={now}, last_motion={last_motion}, diff={now - last_motion}", flush=True)

        if now - last_motion < 1:
            if not display_on:
                turn_display(True)
                try:
                    if subprocess.call(["pgrep", "-x", "luakit"]) != 0:
                        restart_luakit()
                except Exception as e:
                    print(f"[ERROR] luakit 起動判定失敗: {e}", flush=True)
        elif now - last_motion > OFF_DELAY:
            turn_display(False)

        # if not display_on and (now - last_motion > RECOVERY_THRESHOLD):
        #    print("[INFO] 無反応時間が閾値を超過 → 自己再起動します", flush=True)
        #    pir.close()
        #    os.execv(sys.executable, ['python3'] + sys.argv)

        sleep(1)

except Exception as e:
    print(f"[ERROR] {e}", file=sys.stderr)
    raise
