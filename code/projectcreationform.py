from tkinter import *
import csv
import os
import tkinter as tk

##### note: comment the input command at the end of the program before running this python file########

screen = Tk()
screen.geometry("500x500")
screen.title("Project creation form")
heading = Label(screen, text = "Create Project", bg = "grey", fg="black", width ="500")
heading.pack()

#clearing the fields
def clear_field(entry_box):
    entry_box.delete(0, tk.END)
    
#declaring the datatypes
project      = StringVar()

project_text = Label(screen, text = "Create Project")
project_text.place(x = 15, y = 70)

#entry for fields
project_entry = Entry(screen, textvariable = project, width="30")
project_entry.place(x=15, y=90)

## LISTBOX type, search and dropdown LISTBOX
project_suggestion = Listbox(screen, font = ("Arial", 11), height = 3)
project_suggestion.place(x = 210, y = 70)

#tkinter needs lambda since command needs no-argument callable; lambda means do this later when the button is created
project_delete_button = Button(screen, text = "Delete", width = "5", height = "1", command = lambda: clear_field(project_entry), bg = "grey")
project_delete_button.place(x = 15, y = 110)

# TASK
task           = StringVar()

task_text = Label(screen, text = "Create Task")
task_text.place(x = 15, y = 150)

task_entry = Entry(screen, textvariable = task, width="30")
task_entry.place(x=15, y = 180)

task_suggestion = Listbox(screen, font = ("Arial", 11), height = 3)
task_suggestion.place(x = 210, y = 150)

task_delete_button = Button(screen, text = "Delete", width = "5", height = "1", command = lambda: clear_field(task_entry), bg = "grey")
task_delete_button.place(x = 15, y = 200)

#SUBTASK
subtask     = StringVar()

subtask_text = Label(screen, text = "Create Subtask")
subtask_text.place(x = 15, y = 250)

subtask_entry = Entry(screen, textvariable = subtask, width="30")
subtask_entry.place(x=15, y=280)

subtask_suggestion = Listbox(screen, font = ("Arial", 11), height = 3)
subtask_suggestion.place(x = 210, y = 250)

subtask_delete_button = Button(screen, text = "Delete", width = "5", height = "1", command = lambda: clear_field(subtask_entry), bg = "grey")
subtask_delete_button.place(x = 15, y = 300)
##def load_saved_data_from_csv():
##    project_list = []
##    task_list = []
##    subtask_list = []
##    with open('projectandtask.csv', 'r') as projectandtaskfile:
##            reader = csv.DictReader(projectandtaskfile) # next(reader) not needed as DictReader skips the first row
##            for row in reader:
##                project_fromcsv = row['project']
##                task_fromcsv      = row['task']
##                subtask_fromcsv= row['subtask']
##                if project_fromcsv not in project_list:
##                        project_list.append(project_fromcsv)
##                if task_fromcsv not in task_list:
##                        task_list.append(task_fromcsv)
##                if subtask_fromcsv not in subtask_list:
##                        subtask_list.append(subtask_fromcsv)
##    return project_list, task_list, subtask_list

   

def save_info():
    get_project = project_entry.get()
    get_task      = task_entry.get()
    get_subtask= subtask_entry.get()

##    print(get_date, get_time, get_notes)
    filename = "projectandtask.csv"
    #check if file exists to decide whether to write header
    file_exists = os.path.isfile(filename)
    #append a new row
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        #write header only once
        if not file_exists:
            writer.writerow(["project", "task", "subtask"])

        writer.writerow([get_project, get_task, get_subtask])

    if get_project not in project_list:
        project_list.append(get_project)
    if get_task not in task_list:
        task_list.append(get_task)
    if get_subtask not in subtask_list:
        subtask_list.append(get_subtask)

    update_suggestions(project, project_list, project_suggestion)
    update_suggestions(task, task_list, task_suggestion)
    update_suggestions(subtask, subtask_list, subtask_suggestion)
##    project_list, task_list, subtask_list=load_saved_data_from_csv()
##    print("after writing to csv : ", project_list, task_list, subtask_list)

##    project_list, task_list, subtask_list = load_saved_data_from_csv()
##    return project_list, task_list, subtask_list

###
        #for auto seeing the options already saved for project/task/subtask
###

project_list = []
task_list = []
subtask_list = []

try:
        
    with open('projectandtask.csv', 'r') as projectandtaskfile:
        
##        with open(csv_path, 'r') as projectandtaskfile:
        reader = csv.DictReader(projectandtaskfile) # next(reader) not needed as DictReader skips the first row
        for row in reader:
            project_fromcsv = row['project']
            task_fromcsv      = row['task']
            subtask_fromcsv= row['subtask']
            if project_fromcsv not in project_list:
                    project_list.append(project_fromcsv)
            if task_fromcsv not in task_list:
                    task_list.append(task_fromcsv)
            if subtask_fromcsv not in subtask_list:
                    subtask_list.append(subtask_fromcsv)

except FileNotFoundError:
    pass
##except Exception as e:
##    print("Startup error:", e)
##    input("Press Enter to exit...")
                    
def resize_listbox_to_content(listbox):
    items = listbox.get(0, "end")
    if not items:
        return
    longest = max(items, key = len)
    listbox.config(width = len(longest))
    
def update_suggestions(search_var, suggestions, listbox):
    search_term = search_var.get()
    matching_suggestions = [suggestion for suggestion in suggestions if suggestion.lower().startswith(search_term.lower())]
    listbox.delete(0, tk.END)
    for suggestion in matching_suggestions:
        listbox.insert(tk.END, suggestion)
    resize_listbox_to_content(listbox)

###trace() requires a function with this signature: def callback(var_name, index, mode):So you must wrap your function in a lambda.
###lambda receives the 3 arguments but ignores them
##project.trace("w", lambda var, idx, mode: update_suggestions(project, project_list, project_suggestion))

def select_suggestion(event, search_var, listbox):
    selection = listbox.curselection()
    if not selection:
        return     #avoid crash if clicked on empty space
    selected_suggestion = listbox.get(selection)
    search_var.set(selected_suggestion)
    perform_search(search_var)

def perform_search(search_var):
    search_term = search_var.get()
    #perform search based on search term
##project_list, task_list, subtask_list = load_saved_data_from_csv()

#trace() requires a function with this signature: def callback(var_name, index, mode):So you must wrap your function in a lambda.
#lambda receives the 3 arguments but ignores them
project.trace("w", lambda var, idx, mode: update_suggestions(project, project_list, project_suggestion))
#Tkinter supplies event, your lambda supplies project and project_suggestion.
project_suggestion.bind("<<ListboxSelect>>", lambda event: select_suggestion(event, project, project_suggestion))
project_entry.bind("<Return>", lambda event: perform_search(project))

task.trace("w", lambda var, idx, mode: update_suggestions(task, task_list, task_suggestion))
task_suggestion.bind("<<ListboxSelect>>", lambda event: select_suggestion(event, task, task_suggestion))
task_entry.bind("<Return>", lambda event: perform_search(task))
    
subtask.trace("w", lambda var, idx, mode: update_suggestions(subtask, subtask_list, subtask_suggestion))
subtask_suggestion.bind("<<ListboxSelect>>", lambda event: select_suggestion(event, subtask, subtask_suggestion))
subtask_entry.bind("<Return>", lambda event: perform_search(subtask))

submit = Button(screen, text = "Submit", width = "30", height = "2", command = save_info, bg = "grey")
submit.place(x = 0, y = 350)

input("Press enter to proceed...") #### Exclusively for exe since after app creation the app was not opening


##screen.mainloop()
    
