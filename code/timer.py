import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
import os
from tkinter import *
import csv
import datetime
from csv import DictReader
from win11toast import toast



class CountdownTimer:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("")
        self.root.title("Countdown timer")
        self.state = threading.Condition()

        self.time_entry = tk.Entry(self.root, font=("Helvetica", 30))
        self.time_entry.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)

        self.start_button = tk.Button(self.root, font = ("Helvetica", 30), text = "Start", command = self.start_thread)
        self.start_button.grid(row = 1, column = 0, padx = 3, pady = 3)
##        self.start_button = tk.Button(self.root, font = ("Helvetica", 30), text = "Start", command = self.start)
##        self.start_button.grid(row = 1, column = 0, padx = 5, pady = 5)
        

        self.pause_button = tk.Button(self.root, font = ("Helvetica", 30), text = "Pause", command = self.pause)
        self.pause_button.grid(row = 1, column = 1, padx = 3, pady = 3)

        self.resume_button = tk.Button(self.root, font = ("Helvetica", 30), text = "Resume", command = self.resume_thread)
        self.resume_button.grid(row = 1, column = 2, padx = 3, pady = 3)

        self.stop_button = tk.Button(self.root, font = ("Helvetica", 30), text = "Stop", command = self.stop)
        self.stop_button.grid(row = 1, column = 3, padx = 3, pady = 3)

        self.time_label = tk.Label(self.root, font = ("Helvetica", 30), text = "Time: 00:00:00")
        self.time_label.grid(row = 2, column = 0, columnspan = 2, padx = 3, pady = 3)

        self.stop_loop = False

        #for clean closing of the timer window otherwise the loop keeps running while the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def start_thread(self):
        t = threading.Thread(target = self.start)
        t.start()

    def resume_thread(self):
        r = threading.Thread(target = self.resume)
        r.start()

    def start(self):
        self.stop_loop = False
        hours, minutes, seconds = 0, 0, 0
        string_split = self.time_entry.get().split(":")
        if len(string_split) == 3:
            hours      = int(string_split[0])
            minutes   = int(string_split[1])
            seconds = int(string_split[2])
        elif len(string_split) == 2:
            minutes  = int(string_split[0])
            seconds = int(string_split[1])
        elif len(string_split) == 1:
            seconds = int(string_split[0])
        else:
            print("Invalid time format")
            return

        # timer logic
        full_seconds = hours * 3600 + minutes * 60 + seconds
        self.start_seconds = full_seconds

        while full_seconds > 0 and self.stop_loop == False:
            full_seconds -= 1

            minutes, seconds = divmod(full_seconds, 60)
            hours, minutes      = divmod(minutes, 60)
            self.curr_hours     = hours
            self.curr_minutes = minutes
            self.curr_seconds= seconds

            self.time_label.config(text = f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.update()
            time.sleep(1)

        if not self.stop_loop:
            toast("timer", " Time is up!", 10)
            
            
    def pause(self):
        self.stop_loop = True
##        print(self.curr_hours, self.curr_minutes, self.curr_seconds)

    def resume(self):
        self.stop_loop = False

        hours     = self.curr_hours
        minutes = self.curr_minutes
        seconds= self.curr_seconds
        # timer logic
        full_seconds = hours * 3600 + minutes * 60 + seconds


        while full_seconds > 0 and self.stop_loop == False:
            full_seconds -= 1

            minutes, seconds = divmod(full_seconds, 60)
            hours, minutes      = divmod(minutes, 60)
            self.curr_hours     = hours
            self.curr_minutes = minutes
            self.curr_seconds= seconds

            self.time_label.config(text = f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.update()
            time.sleep(1)

        if not self.stop_loop:
            toast("timer", "Time is up!", 10)        

        
    def stop(self):
        self.stop_loop = True
##        self.time_label.config(text = "Text : 00:00:00")
##        stopped_time = f"{self.curr_hours:02d}:{self.curr_minutes:02d}:{self.curr_seconds:02d}"
##        self.root.destroy()
        remaining_time = self.curr_hours * 3600 + self.curr_minutes * 60 + self.curr_seconds
        elapsed_time    = self.start_seconds - remaining_time
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)
        elapsed_hours, elapsed_minutes      = divmod(elapsed_minutes, 60)
        stopped_time = f"{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_seconds:02d}"
        open_form(self.root, stopped_time)
##        script_dir   = os.path.dirname(os.path.abspath(__file__))
##        main_path = os.path.join(script_dir,"main.py")
##        print(main_path)
##        subprocess.Popen([sys.executable, main_path, stopped_time])
##        self.root.destroy()

    def on_closing(self):
        self.stop_loop = True
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

#form for logging time after stopping timer
def open_form(parent, time):
    screen = Toplevel(parent)
    screen.geometry("500x500")
    screen.title("Python Form")
    heading = Label(screen, text = "Python Form", bg = "grey", fg="black", width ="500")
    heading.pack()
    #setting the date and time
    date          = datetime.date.today()
    ##time_now = datetime.datetime.now()
    ##time          = time_now.strftime("%H:%M:%S") 
##    if len(sys.argv) > 1:
##        time = sys.argv[1]
    
    #setting the labels and place holders
    date_text = Label(screen, text="Date")
    time_text = Label(screen, text= "Time")
    date_val  = Label(screen, text=date)  # show the date
    time_val  = Label(screen, text= time) # show the time
    project_text = Label(screen, text= "Project",)
    log_text = Label(screen, text= "Log",)

    date_text.place(x=15, y = 70)
    date_val.place(x=15, y = 90)
    time_text.place(x=15, y = 140)
    time_val.place(x=15, y = 160)
    project_text.place(x=15, y = 210)
    log_text.place(x=15, y = 280)
    #declaring the datatypes
    project      = StringVar()
    log            = StringVar()
    # entry for the text fields
    date_entry   = Entry(screen) # create the Entry widget
    date_entry.insert(0, str(date)) # insert date into the Entry
    time_entry   = Entry(screen)
    time_entry.insert(0, time)
    log_entry = Entry(screen, textvariable = log, width="30")
    log_entry.place(x=15, y=300)

    #dropdown

    projectandtask = StringVar()
    optionMenu = ttk.OptionMenu(screen, projectandtask, "<select>")
    optionMenu.place(x=15, y = 230)
    
    menu = optionMenu["menu"]

    hierarchy = {}
    
    with open('projectandtask.csv', 'r') as projectandtaskfile:
        reader = csv.DictReader(projectandtaskfile) # next(reader) not needed as DictReader skips the first row
        for row in reader:
            project = row['project']
            task      = row['task']
            subtask= row['subtask']

            #if project does not exist in hierarchy yet create it
            if project not in hierarchy:
                hierarchy[project] = {}
            # if task does not exist inside project yet create it
            if task not in hierarchy[project]:
                hierarchy[project][task] = []
            #add subtask to task
            hierarchy[project][task].append(subtask)

    for project, task_dict in hierarchy.items():
        project_menu = tk.Menu(menu, tearoff = False)

        for tasks, subtasks in task_dict.items():
            task_menu  = tk.Menu(project_menu, tearoff = False)

            for sub in subtasks:
                task_menu.add_command(
                    label = sub,
                    command =  lambda value=f"{project} > {tasks} > {sub}" : projectandtask.set(value)
                    )
            project_menu.add_cascade(label = tasks, menu = task_menu)
        menu.add_cascade(label = project, menu = project_menu)

    # define the functions
    def save_info():
        get_date                     = date_entry.get()
        get_time                     = time_entry.get()
        get_log                       = log.get()
        get_projectandtask    = projectandtask.get()
        filename = "timelog.csv"
        #check if file exists to decide whether to write header
        file_exists = os.path.isfile(filename)
        #append a new row
        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            #write header only once
            if not file_exists:
                writer.writerow(["Date", "Time", "ProjectandTask","Log"])

            writer.writerow([get_date, get_time, get_projectandtask, get_log])
        screen.destroy() ###############
            
    # submit button
    submit = Button(screen, text = "Submit", width = "30", height = "2", command = save_info, bg = "grey")
    submit.place(x = 0, y = 350)
##    screen.mainloop()
    
    
CountdownTimer()
