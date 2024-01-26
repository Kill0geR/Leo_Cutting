import tkinter as tk
from datetime import timedelta


class GetTime:
    def __init__(self, seconds_pro_beat):
        self.seconds_pro_beat = seconds_pro_beat

    def start_countdown(self):
        hours = int(hours_entry.get() or 0)
        minutes = int(minutes_entry.get() or 0)
        seconds = int(seconds_entry.get() or 0)

        total_seconds = hours * 3600 + minutes * 60 + seconds
        often_in_one = 1 / self.seconds_pro_beat
        real_seconds_pro_beat = often_in_one * total_seconds

        print(total_seconds)

    @staticmethod
    def start_tkinter():
        root = tk.Tk()
        root.title("Dyma der beste")
        root.geometry("300x250")

        hours_label = tk.Label(root, text="Stunden:")
        hours_label.grid(row=0, column=0)
        hours_entry = tk.Entry(root)
        hours_entry.grid(row=0, column=1)

        minutes_label = tk.Label(root, text="Minuten:")
        minutes_label.grid(row=1, column=0)
        minutes_entry = tk.Entry(root)
        minutes_entry.grid(row=1, column=1)

        seconds_label = tk.Label(root, text="Sekunden:")
        seconds_label.grid(row=2, column=0)
        seconds_entry = tk.Entry(root)
        seconds_entry.grid(row=2, column=1)

        start_button = tk.Button(root, text="Fertig", command=start_countdown)
        start_button.grid(row=3, column=0, columnspan=2)

        times_str = tk.StringVar()
        times_str.set("Gib die gefundene Zeit an")
        timer_label = tk.Label(root, textvariable=times_str)
        timer_label.grid(row=4, column=0, columnspan=2)

        root.mainloop()

