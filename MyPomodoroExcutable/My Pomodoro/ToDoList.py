import customtkinter
import time
import threading
#from tkinter import *
import tkinter as tk
#from tkinter.ttk import *
import itertools
import csv
import os
from tkinter.filedialog import askopenfilename



class Scrollable(customtkinter.CTkFrame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, frm_list, width=16):

        #self.configure(fg_color="transparent")
        
        scrollbar = customtkinter.CTkScrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set, background=frame["bg"], bd=0, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.configure(command=self.canvas.yview)

        self.canvas.bind('<Configure>', lambda event, arg=frm_list: self.__fill_canvas(event, arg))

        # base class initialization
        customtkinter.CTkFrame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)


    def __fill_canvas(self, event, frm_list):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        #canvas_height = event.height
        #for f in frm_list:
            #canvas_height += f.winfo_height()
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))




class ToDoList(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="header", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.pack_propagate(1)
        
        self.list = []
        self.btn_list = []
        self.frm_list = []
        
        ##self.grid_rowconfigure((0,1,2), weight=1)
        ##self.grid_columnconfigure((0,1,2), weight=1)
        
        self.time_label = customtkinter.CTkLabel(self, text="To-Do:", font=("Arial", 30))
        ##self.time_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10,5), sticky="new")
        self.time_label.pack(padx=10, pady=10, side=tk.TOP)
        
        self.list_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        ##self.list_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
        self.list_frame.pack(padx=10, pady=10, side=tk.TOP, fill=tk.BOTH, expand=True)
        self.scrollable_frame = Scrollable(self.list_frame, self.frm_list)
        
        self.btn_frm = customtkinter.CTkFrame(self, fg_color="transparent")
        self.btn_frm.pack(padx=1, pady=1, side=tk.TOP)
        self.item_entry = customtkinter.CTkEntry(self.btn_frm, placeholder_text="add a task", width=200, height=30)
        ##self.item_entry.grid(row=2, column=0, padx=(10,5), pady=(5,10), sticky="sew")
        self.item_entry.pack(padx=9, pady=9, side=tk.LEFT, anchor="sw")
        
        self.add_button = customtkinter.CTkButton(self.btn_frm, width=50, height=30, text="add", command= self.add_item)
        ##self.add_button.grid(row=2, column=2, padx=(5,10), pady=(5,10), sticky="sew")
        self.add_button.pack(padx=9, pady=9, side=tk.LEFT, anchor="se")
        
        
        self.delete_done_button = customtkinter.CTkButton(self, width=50, height=30, text="delete done", command= self.delete_done)
        self.delete_done_button.pack(padx=5, pady=10, side=tk.RIGHT, anchor="s")
        self.delete_all_button = customtkinter.CTkButton(self, width=50, height=30, text="delete all", command= self.delete_all)
        self.delete_all_button.pack(padx=5, pady=10, side=tk.RIGHT, anchor="s")
        self.save_button = customtkinter.CTkButton(self, width=50, height=30, text="save", command= self.save_list)
        self.save_button.pack(padx=5, pady=10, side=tk.RIGHT, anchor="s")
        self.load_button = customtkinter.CTkButton(self, width=50, height=30, text="load", command= self.load_list)
        self.load_button.pack(padx=5, pady=10, side=tk.RIGHT, anchor="s")
        
        self.list_frame.pack_propagate(1)
        
        #self.scrollbar = customtkinter.CTkScrollbar(self.list_frame, orientation="vertical")
        #self.scrollbar.grid(row=1, column=2, sticky="ns")
        #self.list_frame.configure(yscrollcommand=self.scrollbar.set)
        
        
        
        
    def add_item(self):
        item_text = self.item_entry.get()
        frm = customtkinter.CTkFrame(self.scrollable_frame, fg_color="transparent")
        frm.pack(padx=10, pady=1, side=tk.TOP)
        self.frm_list.append(frm)
        item = customtkinter.CTkCheckBox(frm, text=item_text)
        ##item.grid(row=(len(self.list)), column=0, padx=5, pady=5, sticky="ew")
        item.pack(padx=10, pady=4, side=tk.LEFT, anchor="w")
        self.list.append(item)
        btn = customtkinter.CTkButton(frm, width=10, height=10, corner_radius=5, fg_color=('#808080'), hover_color=('#f44336'), text="", command=(lambda: self.delete(self.btn_list.index(btn))))
        ##btn.grid(row=(len(self.btn_list)), column=1, padx=5, pady=5, sticky="ew")
        btn.pack(padx=10, pady=4, side=tk.LEFT, anchor="e")
        self.btn_list.append(btn)
        self.scrollable_frame.update()
        self.item_entry.delete(0, "end")
        #print(self.scrollable_frame.winfo_children())
        
        
        
        
    def delete(self, i):
        self.btn_list[i].destroy()
        self.list[i].destroy()
        self.frm_list[i].destroy()
        #print(self.list[1].cget("text"))
        del self.btn_list[i]
        del self.list[i]
        del self.frm_list[i]
        #print(len(self.frm_list))
        #print(len(self.list))
        #print(len(self.btn_list))
        
        
    def delete_all(self):
        for i in self.list:
            #self.btn_list.index(i).destroy()
            #self.list.index(i).destroy()
            #self.frm_list.index(i).destroy()
            indx = self.list.index(i)
            #print(indx)
            self.btn_list[indx].destroy()
            #del self.btn_list[indx]
            self.list[indx].destroy()
            #del self.list[indx]
            self.frm_list[indx].destroy()
            #del self.frm_list[indx]
            self.scrollable_frame.update()
        
        #print("here")
        self.btn_list = []
        self.list = []
        self.frm_list = []
        #print(len(self.frm_list))
        #print(len(self.list))
        #print(len(self.btn_list))
        #print(self.list[0].cget("text"))
            
            
    def delete_done(self):
        for (i, j, k) in zip(self.list[:], self.btn_list[:], self.frm_list[:]):
            #print(i.cget("text"))
            if i.get():
                #self.btn_list[i].destroy()
                #self.list[i].destroy()
                #self.frm_list[self.list.index(i)].destroy()
                
                i.destroy()
                j.destroy()
                k.destroy()
                self.list.remove(i)
                self.btn_list.remove(j)
                self.frm_list.remove(k)
                self.scrollable_frame.update()
        #print(len(self.frm_list))
        #print(len(self.list))
        #print(len(self.btn_list))
                
                
                
    def save_list(self):
        
        timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
        header = ['task', 'state']
        filepath = os.path.join('savedLists', '%s.csv' %timestr)
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for i in self.list:
                task = i.cget("text")
                state = i.get()
                writer.writerow([task, state])
        #print(timestr)
        
        
    def load_list(self):
        filepath = askopenfilename(initialdir=os.path.join('savedLists') , title="select a list", filetypes=(("CSV Files","*.csv"),))
        with open(filepath, 'r')  as file:
            csvreader = csv.reader(file)
            next(csvreader, None)
            for row in csvreader:
                item_text = row[0]
                frm = customtkinter.CTkFrame(self.scrollable_frame, fg_color="transparent")
                frm.pack(padx=10, pady=1, side=tk.TOP)
                self.frm_list.append(frm)
                item = customtkinter.CTkCheckBox(frm, text=item_text)
                if row[1] == '1':
                    item.select()
                item.pack(padx=10, pady=4, side=tk.LEFT, anchor="w")
                self.list.append(item)
                btn = customtkinter.CTkButton(frm, width=10, height=10, corner_radius=5, fg_color=('#808080'), hover_color=('#f44336'), text="", command=(lambda: self.delete(self.btn_list.index(btn))))
                btn.pack(padx=10, pady=4, side=tk.LEFT, anchor="e")
                self.btn_list.append(btn)
                self.scrollable_frame.update()
                self.item_entry.delete(0, "end")
        #print(filepath)
        
    
    
    #lambda: self.delete(self.add_button)    