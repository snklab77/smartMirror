#!/usr/bin/env python3

# CPU使用率とスワップ使用量を監視し、閾値を超えた場合にマシンを再起動するスクリプト
# 貧弱なzero 2 wのCPUやmemoryだとちょっとした負荷の重なりで応答不可な状態に陥る為
# 監視して一定の閾値を超える用ならマシン自体を再起動する事で復帰させる
# Script to monitor CPU usage and swap utilization - reboots the machine if thresholds are exceeded
# Due to the limited CPU and memory resources of Zero 2 W, even slight overlapping loads can lead to unresponsive states
# Monitor these metrics and recover by rebooting the machine when thresholds are exceeded
import psutil
import time
import subprocess

SWAP_THRESHOLD_MB = 200          # 必要に応じて調整
CPU_USAGE_THRESHOLD = 95         # CPU使用率の閾値（95%）
CPU_CHECK_DURATION = 90          # CPU使用率が閾値を超えた状態が続く時間（秒）
CHECK_INTERVAL = 1               # 毎秒チェック

cpu_high_start = None

def restart_motion_service():
    try:
        subprocess.run(["systemctl", "restart", "smartmirror-xinit.service"])
        print("[INFO] smartmirror-xinit.service を再起動しました", flush=True)
    except Exception as e:
        print(f"[ERROR] 再起動失敗: {e}", flush=True)

while True:
    try:
        swap_used = psutil.swap_memory().used / (1024 * 1024)  # MB
        cpu_percent = psutil.cpu_percent(interval=0)

        if swap_used > SWAP_THRESHOLD_MB:
            print(f"[INFO] スワップ使用量 {swap_used:.1f}MB 超過 → 再起動", flush=True)
            restart_motion_service()
            time.sleep(10)
            continue

        if cpu_percent > CPU_USAGE_THRESHOLD:
            if not cpu_high_start:
                cpu_high_start = time.time()
            elif time.time() - cpu_high_start >= CPU_CHECK_DURATION:
                print(f"[INFO] CPU使用率 {cpu_percent:.1f}% が {CPU_CHECK_DURATION}秒続いた → 再起動", flush=True)
                restart_motion_service()
                time.sleep(10)
                continue
        else:
            cpu_high_start = None

    except Exception as e:
        print(f"[ERROR] 監視中エラー: {e}", flush=True)

    time.sleep(CHECK_INTERVAL)
