import threading
import time
import random
import requests
import uuid
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from datetime import datetime

# ==========================================
# 🔑 NAYA FRESH SESSION ID YAHAN DALO
MY_SESSION_ID = "78347277685%3A7ZaxrwsT9zGwlG%3A7%3AAYhVuKQfOo4BkZRZZ2hHE1m6QsDn2jI4zgTgegTOArs"
# ==========================================

running = False
success_count = 0
fail_count = 0

def get_thread_id(url):
    try:
        if "/t/" in url:
            return url.split("/t/")[1].strip("/")
        return None
    except:
        return None

def neon_engine(t_id, msg, delay, s_type, status_lbl, log_box):
    global success_count, fail_count, running
    
    # ⚡ ULTRA-BYPASS HEADERS (Android 13 Emulation)
    headers = {
        "User-Agent": "Instagram 314.0.0.33.106 Android (33/13; 480dpi; 1080x2235; samsung; SM-G998B; o1q; exynos2100; en_US; 546274714)",
        "Cookie": f"sessionid={MY_SESSION_ID}",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-IG-App-ID": "1217981644879628",
        "X-IG-Capabilities": "3brTvwE=",
        "X-IG-Connection-Type": "WIFI",
        "X-ASBD-ID": "129477",
    }

    url = f"https://www.instagram.com/api/v1/direct_v2/threads/{t_id}/items/send_text/"

    while running:
        # Har message ko unique banane ke liye suffix
        suffix = f" {random.choice(['🦅','🔥','👑','⚡'])} [{random.randint(100, 999)}]"
        final_msg = f"{msg}{suffix}"
        
        # Payload randomization
        payload = {
            "text": final_msg,
            "client_context": str(uuid.uuid4()),
            "mutation_token": str(uuid.uuid4()),
            "offline_threading_id": str(uuid.uuid4())
        }

        try:
            r = requests.post(url, headers=headers, data=payload, timeout=10)
            
            if r.status_code == 200:
                success_count += 1
                status_lbl.config(text=f"✅ SUCCESS: {success_count}", fg="#00ff00")
            elif r.status_code == 401:
                log_box.insert(tk.END, "[-] Error 401: Session ID Expire ho gaya hai!\n", "err")
                running = False
                break
            elif r.status_code == 429:
                log_box.insert(tk.END, "[-] Error 429: Instagram ne block kiya. 2 min ruko.\n", "warn")
                time.sleep(10)
            else:
                fail_count += 1
                status_lbl.config(text=f"❌ FAIL: {fail_count} (Code: {r.status_code})", fg="red")
        except:
            fail_count += 1
            
        time.sleep(delay + random.uniform(0.1, 0.4))

def start_overdrive(url, msg, thr, dly, status, logs):
    global running, success_count, fail_count
    t_id = get_thread_id(url)
    if not t_id:
        messagebox.showerror("Error", "Bhai valid Chat URL dalo!")
        return

    running = True
    success_count = 0
    fail_count = 0
    logs.insert(tk.END, f"[*] NEON OVERDRIVE ACTIVATED: {t_id}\n", "info")

    for _ in range(thr):
        threading.Thread(target=neon_engine, args=(t_id, msg, dly, "Number", status, logs), daemon=True).start()

# --- GUI ---
root = tk.Tk()
root.title("EREN X NYXON7X v17.0 NEON")
root.geometry("600x700")
root.configure(bg="#000")

tk.Label(root, text="NEON OVERDRIVE V17", font=("Impact", 35), fg="#ff0000", bg="#000").pack(pady=20)
f = tk.Frame(root, bg="#0a0a0a", padx=20, pady=20, bd=1, relief="solid"); f.pack(fill="both", expand=True, padx=20)

tk.Label(f, text="CHAT LINK (URL):", fg="#777", bg="#0a0a0a", font=("Arial", 10, "bold")).pack(anchor="w")
url_in = tk.Entry(f, width=60, bg="#111", fg="white", bd=0); url_in.pack(pady=5, ipady=10)

tk.Label(f, text="MESSAGE:", fg="#777", bg="#0a0a0a", font=("Arial", 10, "bold")).pack(anchor="w")
msg_in = tk.Entry(f, width=60, bg="#111", fg="#00ff00", bd=0); msg_in.pack(pady=5, ipady=10)
msg_in.insert(0, "NEON SPEED BY EREN")

cfg = tk.Frame(f, bg="#0a0a0a")
cfg.pack(pady=15)
tk.Label(cfg, text="THREADS:", fg="white", bg="#0a0a0a").grid(row=0, column=0)
thr_in = tk.Entry(cfg, width=8, bg="#222", fg="white"); thr_in.insert(0, "2"); thr_in.grid(row=0, column=1, padx=5)
tk.Label(cfg, text="DELAY (SEC):", fg="white", bg="#0a0a0a").grid(row=0, column=2)
del_in = tk.Entry(cfg, width=8, bg="#222", fg="white"); del_in.insert(0, "1.0"); del_in.grid(row=0, column=3, padx=5)

status_lbl = tk.Label(f, text="SYSTEM READY", fg="cyan", bg="#0a0a0a", font=("Arial", 12, "bold"))
status_lbl.pack(pady=10)

log_box = scrolledtext.ScrolledText(f, height=10, bg="black", fg="#00ff00", font=("Consolas", 9))
log_box.tag_config("err", foreground="red")
log_box.tag_config("info", foreground="cyan")
log_box.tag_config("warn", foreground="orange")
log_box.pack(fill="both", expand=True)

btn_fr = tk.Frame(root, bg="#000"); btn_fr.pack(pady=20)
tk.Button(btn_fr, text="🚀 LAUNCH NEON", bg="red", fg="white", width=22, font=("Arial", 12, "bold"), bd=0, 
          command=lambda: start_overdrive(url_in.get(), msg_in.get(), int(thr_in.get()), float(del_in.get()), status_lbl, log_box)).pack(side="left", padx=10)
tk.Button(btn_fr, text="STOP", bg="#333", fg="white", width=12, font=("Arial", 12, "bold"), bd=0, command=lambda: globals().update(running=False)).pack(side="left")

root.mainloop()