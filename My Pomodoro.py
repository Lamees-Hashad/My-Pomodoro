#tomato icon attribution:
#<a href="https://www.flaticon.com/free-icons/tomato" title="tomato icons">Tomato icons created by Rudiyana - Flaticon</a>

import customtkinter
from Pomodoro import *
from ToDoList import*
from tkinter import *


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("300x500")
        self.resizable(0, 0)
        self.title("My Pomodoro")
        self.wm_iconbitmap("tomato.ico")
        
        
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.pack(side="top", fill="both", expand=True)
        self.tabview.add("Pomodoro")
        self.tabview.add("To-Do")

        
        self.timer_frame = PomodoroTimer(self.tabview.tab("Pomodoro"), header_name="PomodoroTimer")
        self.timer_frame.pack(side="top", fill="both", expand=True)


        self.list_frame = ToDoList(self.tabview.tab("To-Do"), header_name="TO DO List")
        self.list_frame.pack(side="top", fill="both", expand=True)
            

if __name__ == "__main__":
    app = App()
    app.mainloop()