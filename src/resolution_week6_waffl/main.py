import tkinter as tk
from tkinter import messagebox
import json, os

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def main():
    root = tk.Tk()
    root.title("Todo List")
    root.geometry("400x300")
    #config geometry at the end

    # Funcion defining
    def format_task(task):
        status = "Complete" if task["done"] else "Incomplete"
        return f"{status} - {task['task']}"


    def add_task():
        task_txt = entry.get().strip()

        tasks = load_tasks()
        new_task = {"task": task_txt, "done": False}
        tasks.append(new_task)
        save_tasks(tasks)

        listbox.insert(tk.END, format_task(new_task))
        entry.delete(0, tk.END)

    def delete():
        item = listbox.curselection()
        if not item:
            return
        if messagebox.askyesno("Confirm", "NAOOO DONT LEAVE MEEEE (yes to delete, no to cancel)"):
            index = item[0]

            listbox.delete(index)
            tasks = load_tasks()
            tasks.pop(index)
            save_tasks(tasks)
            messagebox.showinfo("Deleted", "NAOOOOOOOOOOOOO")
        else:
            messagebox.showinfo("Cancelled", "YAYYY NOW PLEASE COMPLETE ME")
    # woah i discovered .pop

    def markas():
        item = listbox.curselection()
        index = item[0]
        tasks = load_tasks()

        tasks[index]["done"] = not tasks[index]["done"]
        save_tasks(tasks)

        listbox.delete(index)
        listbox.insert(index, format_task(tasks[index]))

    def edit_task(event):
        item = listbox.curselection()
        if not item:
            return

        index = item[0]
        tasks = load_tasks()
        old_name = tasks[index]["task"]

        x, y, width, height = listbox.bbox(index)

        edit_box = tk.Entry(listbox)
        edit_box.insert(0, old_name)
        edit_box.place(x=x, y=y, width=width, height=height)

        def save_edit(event=None):
            new_name = edit_box.get().strip()
            if new_name:
                tasks[index]["task"] = new_name
                save_tasks(tasks)
                listbox.delete(index)
                listbox.insert(index, format_task(tasks[index]))
            edit_box.destroy()

        edit_box.bind("<Return>", save_edit)
        edit_box.bind("<FocusOut>", save_edit)
        edit_box.focus()

    def reset_all():
        if messagebox.askyesno("Confirm", "Are you certain? This can't be undone!"):
            save_tasks([])
            listbox.delete(0, tk.END)
            messagebox.showinfo("Deleted", "EVERYTHING BLWON UP")
        else:
            messagebox.showinfo("Cancelled", "uh ok... get back to work")




    # frame for adding new task
    make_task = tk.Frame(root)
    make_task.pack(pady=5)

    tk.Label(make_task, text="New Task:").grid(column=0, row=0)
    entry = tk.Entry(make_task)
    entry.grid(column=1, row=0)
    tk.Button(make_task, text="Add", command=add_task).grid(column=2, row=0)

    # Tasks list frame
    TaskList = tk.Frame(root)
    TaskList.pack(fill="both", expand=True)


    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    TaskList.columnconfigure(0, weight=1)
    TaskList.rowconfigure(0, weight=1)


    scrollbar = tk.Scrollbar(TaskList)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(TaskList, yscrollcommand=scrollbar.set)
    listbox.pack(side="left", fill="both", expand=True)

    listbox.bind("<Double-Button-1>", edit_task)
    scrollbar.config(command=listbox.yview)

    # Update/Delete and total reset frame
    update = tk.Frame(root)
    update.pack(pady=5)

    tk.Button(update, text="Mark Complete", command=markas).grid(column=0, row=0)
    tk.Button(update, text="Delete Task", command=delete).grid(column=1, row=0)
    tk.Button(update, text="RESET ALL", command=reset_all).grid(column=2, row=0)

    # adds tasks to listbox from .json
    tasks = load_tasks()
    for task in tasks:
        listbox.insert(tk.END, format_task(task))


    root.mainloop()


if __name__ == "__main__":
    main()