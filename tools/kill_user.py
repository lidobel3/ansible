#!/usr/bin/env python3

import psutil
import sys
import os

def kill_user_processes(username):
    current_pid = os.getpid()
    killed = 0
    failed = 0

    for proc in psutil.process_iter(['pid', 'username', 'name']):
        try:
            if proc.info['username'] == username and proc.pid != current_pid:
                proc.kill()
                print(f"Killed PID {proc.pid} ({proc.info['name']})")
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"⚠️  Could not kill PID {proc.pid}: {e}")
            failed += 1

    print(f"\n✅ Total killed: {killed}")
    if failed > 0:
        print(f"❌ Total failed: {failed}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sudo python3 kill_user_processes.py <username>")
        sys.exit(1)

    user = sys.argv[1]

    if os.geteuid() != 0:
        print("❗ Ce script doit être exécuté en tant que root (sudo)")
        sys.exit(1)

    kill_user_processes(user)
