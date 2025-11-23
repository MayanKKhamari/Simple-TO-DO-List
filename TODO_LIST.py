import json
import tkinter as tk
from tkinter import messagebox, simpledialog

file_name = "todo_list.json"



def clean_tasks(tasks):
    new_list = []
    for item in tasks["tasks"]:
        if isinstance(item, dict):
            new_list.append(item)
        else:
            print("REMOVED INVALID TASK:", item)
    tasks["tasks"] = new_list
    save_task(tasks)

def load_task():
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except:
        return {"tasks": []}

def save_task(tasks):
    try:
        with open(file_name, 'w') as file:
            json.dump(tasks, file, indent=4)
    except:
        print("Failed to Save.")



def refresh_listbox():
    listbox.delete(0, tk.END)
    for i, task in enumerate(tasks["tasks"], start=1):
        status = "✔" if task["complete"] else "✗"
        listbox.insert(tk.END, f"{i}. {task['description']}  [{status}]")

def add_task():
    desc = simpledialog.askstring("Add Task", "Enter task description:")
    if desc:
        tasks["tasks"].append({"description": desc, "complete": False})
        save_task(tasks)
        refresh_listbox()

def mark_complete():
    try:
        index = listbox.curselection()[0]
    except:
        messagebox.showwarning("Select Task", "Choose a task first.")
        return

    tasks["tasks"][index]["complete"] = True
    save_task(tasks)
    refresh_listbox()

def delete_task():
    try:
        index = listbox.curselection()[0]
    except:
        messagebox.showwarning("Select Task", "Choose a task first.")
        return

    desc = tasks["tasks"][index]["description"]
    if messagebox.askyesno("Delete", f"Delete '{desc}'?"):
        tasks["tasks"].pop(index)
        save_task(tasks)
        refresh_listbox()

def edit_task():
    try:
        index = listbox.curselection()[0]
    except:
        messagebox.showwarning("Select Task", "Choose a task first.")
        return

    current_desc = tasks["tasks"][index]["description"]
    new_desc = simpledialog.askstring("Edit Task", "New description:", initialvalue=current_desc)

    if new_desc:
        tasks["tasks"][index]["description"] = new_desc
        save_task(tasks)
        refresh_listbox()


tasks = load_task()
clean_tasks(tasks)

root = tk.Tk()
root.title("To-Do List Manager")
root.geometry("400x450")

listbox = tk.Listbox(root, font=("Arial", 12), height=15)
listbox.pack(fill="both", expand=True, padx=10, pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Add Task", width=12, command=add_task).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Complete", width=12, command=mark_complete).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Edit", width=12, command=edit_task).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Delete", width=12, command=delete_task).grid(row=1, column=1, padx=5, pady=5)

refresh_listbox()

root.mainloop()
