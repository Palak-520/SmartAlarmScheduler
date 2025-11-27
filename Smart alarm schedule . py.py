# smart_alarm.py
import datetime
import time
import json
import threading
import tkinter as tk
from tkinter import messagebox
from playsound import playsound
import pyttsx3

# -------- SPEECH ENGINE SETUP --------
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# -------- JSON FILE SETUP --------
ALARM_FILE = "alarms.json"

def load_alarms():
    try:
        with open(ALARM_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_alarms(alarms):
    with open(ALARM_FILE, "w") as f:
        json.dump(alarms, f, indent=4)

# -------- ALARM CHECK FUNCTION --------
def check_alarms():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        alarms = load_alarms()
        for alarm in alarms:
            if alarm["time"] == now:
                messagebox.showinfo("Alarm!", f"⏰ {alarm['label']}")
                engine.say(f"Time for {alarm['label']}")
                engine.runAndWait()
                playsound("alarm_sound.mp3")  # Add your mp3 file in same folder
                time.sleep(60)  # Wait a minute before checking again
        time.sleep(10)

# -------- GUI FUNCTIONS --------
def add_alarm():
    alarm_time = time_entry.get()
    label = label_entry.get()
    if alarm_time and label:
        alarms = load_alarms()
        alarms.append({"time": alarm_time, "label": label})
        save_alarms(alarms)
        messagebox.showinfo("Added", f"Alarm set for {alarm_time} - {label}")
        time_entry.delete(0, tk.END)
        label_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Please enter both time and label!")

def show_alarms():
    alarms = load_alarms()
    if alarms:
        all_alarms = "\n".join([f"{a['time']} - {a['label']}" for a in alarms])
        messagebox.showinfo("Saved Alarms", all_alarms)
    else:
        messagebox.showinfo("No Alarms", "No alarms found!")

def delete_alarms():
    save_alarms([])
    messagebox.showinfo("Deleted", "All alarms deleted!")

# -------- GUI DESIGN --------
root = tk.Tk()
root.title("Smart Alarm Scheduler")
root.geometry("400x320")
root.config(bg="#e6f0ff")

tk.Label(root, text="Smart Alarm Scheduler", font=("Arial", 16, "bold"), bg="#e6f0ff", fg="#003366").pack(pady=10)

tk.Label(root, text="Enter Time (HH:MM):", bg="#e6f0ff", font=("Arial", 11)).pack()
time_entry = tk.Entry(root, font=("Arial", 12), justify="center")
time_entry.pack(pady=5)

tk.Label(root, text="Enter Label:", bg="#e6f0ff", font=("Arial", 11)).pack()
label_entry = tk.Entry(root, font=("Arial", 12), justify="center")
label_entry.pack(pady=5)

tk.Button(root, text="Add Alarm", command=add_alarm, bg="#003366", fg="white", font=("Arial", 11, "bold")).pack(pady=5)
tk.Button(root, text="Show Alarms", command=show_alarms, bg="#336699", fg="white", font=("Arial", 11, "bold")).pack(pady=5)
tk.Button(root, text="Delete All Alarms", command=delete_alarms, bg="#990000", fg="white", font=("Arial", 11, "bold")).pack(pady=5)

tk.Label(root, text="Keep window open for alarms to ring!", bg="#e6f0ff", font=("Arial", 9, "italic")).pack(pady=10)

# -------- START ALARM CHECK THREAD --------
t = threading.Thread(target=check_alarms, daemon=True)
t.start()

root.mainloop()

