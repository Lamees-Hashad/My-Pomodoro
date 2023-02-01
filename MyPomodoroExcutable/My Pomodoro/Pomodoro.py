import customtkinter
import tkinter as tk
import time
import threading
from win10toast import ToastNotifier
import random


class PomodoroTimer(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="header", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.header_name = header_name
        
        self.pack_propagate(1)
        
        self.timer_options_dict = {"pomodoro":25, "short break":5, "long break":15}
        self.elapsed_pomodoros = 0
        self.stopped = False
        self.skipped = False
        self.paused = False
        self.optionmenu_var = customtkinter.StringVar(value="pomodoro")
        self.phrases = ["You got this.", "Good luck today!", "Keep on keeping on!", "Go for it", "Just do it!", "Keep up the good work", "Keep it up.", "Good job.", "Don’t give up.", "Keep pushing.", "Never give up.", "Come on! You can do it!.", "Follow your dreams.", "Reach for the stars.", "Believe in yourself.", "The sky is the limit.", "Do the impossible.", "You are doing awesome!"]
        
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.time_label = customtkinter.CTkLabel(self, text="25 : 00", font=("Arial", 40))
        self.time_label.grid(row=0, column=1, columnspan=2, padx=10, pady=(10,5), sticky="ew")
        
        self.timer_options_select = customtkinter.CTkOptionMenu(self, values=["pomodoro", "short break", "long break"], variable=self.optionmenu_var, command=self.set_timer)
        self.timer_options_select.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        
        self.start_button = customtkinter.CTkButton(self, width=50, height=30, text="start", command=self.start_timer_thread)
        self.start_button.grid(row=2, column=0, padx=(10,5), pady=(5,10), sticky="ew")
        
        self.pause_button = customtkinter.CTkButton(self, width=50, height=30, text="pause", command=self.pause_timer)
        self.pause_button.grid(row=2, column=1, padx=5, pady=(5,10), sticky="ew")
        
        self.skip_button = customtkinter.CTkButton(self, width=50, height=30, text="skip", command=self.skip_timer)
        self.skip_button.grid(row=2, column=2, padx=5, pady=(5,10), sticky="ew")
        
        self.stop_button = customtkinter.CTkButton(self, width=50, height=30, text="stop", command=self.stop_timer)
        self.stop_button.grid(row=2, column=3, padx=(5,10), pady=(5,10), sticky="ew")
        

        
        self.pomodor_counter_label = customtkinter.CTkLabel(self, text="elapsed pomodoros: 0", font=("Arial", 10))
        self.pomodor_counter_label.grid(row=3, column=0, columnspan=4, padx=5, pady=(5,10), sticky="ew")
        
    
    def start_timer_thread(self):
        t = threading.Thread(target=self.start_timer)
        t.start()
            
    
    
    def start_timer(self):
        
        self.stopped = False
        self.skipped = False
        self.start_button.configure(state= customtkinter.DISABLED)
        self.timer_options_select.configure(state= customtkinter.DISABLED)
        
        #total_seconds = self.timer_options_dict[self.timer_options_select.get()]
        total_seconds = int(self.time_label.cget("text")[:2]) * 60 + int(self.time_label.cget("text")[-2:])
        
        while (total_seconds > 0) and (not self.stopped):
            minutes, seconds = divmod(total_seconds, 60)
            self.time_label.configure(text=f'{minutes:02d} : {seconds:02d}')
            self.update()
            time.sleep(1)
            total_seconds -= 1
        
        if self.timer_options_select.get() == "pomodoro":
                
            if (not self.stopped) or self.skipped:
                self.elapsed_pomodoros += 1
                self.pomodor_counter_label.configure(text=f'elapsed pomodoros: {self.elapsed_pomodoros:02d}')
                
                if self.elapsed_pomodoros % 4 == 0:
                    self.timer_options_select.set("long break")
                    self.time_label.configure(text="15 : 00")
                    self.show_notification("Long Break!", "Take fifteen")
                else:
                    self.timer_options_select.set("short break")
                    self.time_label.configure(text="05 : 00")
                    self.show_notification("Short Break!", "Take five")
                    
                self.start_timer()
            
        elif (self.timer_options_select.get() == "long break") or (self.timer_options_select.get() == "short break"):
                            
            if (not self.stopped) or self.skipped:
                self.timer_options_select.set("pomodoro")
                self.time_label.configure(text="25 : 00")
                self.show_notification("Pomodoro!", self.phrases[random.randint(0, len(self.phrases))])
                self.start_timer()
            
    
    def stop_timer(self):
        self.stopped = True
        self.start_button.configure(state= customtkinter.NORMAL)
        self.timer_options_select.configure(state= customtkinter.NORMAL)
        self.timer_options_select.set("pomodoro")
        self.time_label.configure(text="25 : 00")
        self.elapsed_pomodoros = 0
        self.pomodor_counter_label.configure(text="elapsed pomodoros: 0")
        
    
    def skip_timer(self):
        self.skipped = True
        self.stopped = True
        
        
    def pause_timer(self):
        self.paused = not self.paused
        self.stopped = True
        if not self.paused:
            print(int(self.time_label.cget("text")[:1]))
            self.start_timer()
        
        
    def set_timer(self, selection):
        self.time_label.configure(text=f'{self.timer_options_dict[selection]:02d} : 00')
        
    def show_notification(self, title, text):
        toaster = ToastNotifier()
        toaster.show_toast(title, text, icon_path="tomato.ico", duration=3, threaded=True)