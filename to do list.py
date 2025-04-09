import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import os

USERS_FILE = "users.txt"

# User data handlers
def read_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                username, password = line.strip().split(",")
                users[username] = password
    return users

def save_user(username, password):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password}\n")

# Task data handlers
def load_tasks(username):
    filename = f"{username}_tasks.txt"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_tasks(username, tasks):
    filename = f"{username}_tasks.txt"
    with open(filename, "w") as f:
        for task in tasks:
            f.write(task + "\n")

# Main App Class
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - To-Do App")
        self.username = ""
        self.tasks = []
        self.bg_color = "grey"
        self.fg_color = "black"
        self.root.configure(bg=self.bg_color)

        self.build_login_ui()

    def clear_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Login UI
    def build_login_ui(self):
        self.clear_ui()

        tk.Label(self.root, text="Login / Sign Up", font=("Helvetica", 16), bg=self.bg_color, fg=self.fg_color).pack(pady=10)

        tk.Label(self.root, text="Username:", bg=self.bg_color, fg=self.fg_color).pack()
        self.username_entry = tk.Entry(self.root, bg="white", fg=self.fg_color)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:", bg=self.bg_color, fg=self.fg_color).pack()
        self.password_entry = tk.Entry(self.root, show="*", bg="white", fg=self.fg_color)
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login, bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        tk.Button(self.root, text="Sign Up", command=self.signup, bg=self.bg_color, fg=self.fg_color).pack()

    def login(self):
        users = read_users()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username in users and users[username] == password:
            self.username = username
            self.tasks = load_tasks(username)
            self.build_todo_ui()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def signup(self):
        users = read_users()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password cannot be empty.")
            return

        if username in users:
            messagebox.showerror("Sign Up Failed", "Username already exists.")
        else:
            save_user(username, password)
            messagebox.showinfo("Success", "User registered! You can now login.")

    # To-Do UI
    def build_todo_ui(self):
        self.clear_ui()
        self.root.title(f"{self.username}'s To-Do List")
        self.root.configure(bg=self.bg_color)

        tk.Label(self.root, text=f"Welcome, {self.username}", font=("Helvetica", 14), bg=self.bg_color, fg=self.fg_color).pack(pady=10)

        self.task_entry = tk.Entry(self.root, width=30, bg="white", fg=self.fg_color)
        self.task_entry.pack(pady=5)

        tk.Label(self.root, text="Select Deadline:", bg=self.bg_color, fg=self.fg_color).pack()
        self.deadline_entry = DateEntry(
            self.root, width=12, background='pink',
            foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd'
        )
        self.deadline_entry.pack(pady=5)

        tk.Button(self.root, text="Add Task", command=self.add_task, bg=self.bg_color, fg=self.fg_color).pack()
        self.task_listbox = tk.Listbox(self.root, width=50, bg="white", fg=self.fg_color, selectbackground="pink", selectforeground="black")
        self.task_listbox.pack(pady=10)

        tk.Button(self.root, text="Delete Selected Task", command=self.delete_task, bg=self.bg_color, fg=self.fg_color).pack(pady=2)
        tk.Button(self.root, text="Logout", command=self.logout, bg=self.bg_color, fg=self.fg_color).pack(pady=5)

        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        deadline = self.deadline_entry.get_date().strftime('%Y-%m-%d')
        if task_text:
            task_full = f"{task_text} - Due: {deadline}"
            self.tasks.append(task_full)
            save_tasks(self.username, self.tasks)
            self.task_entry.delete(0, tk.END)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty.")

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            task_index = selected[0]
            del self.tasks[task_index]
            save_tasks(self.username, self.tasks)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def logout(self):
        self.username = ""
        self.tasks = []
        self.root.title("Login - To-Do App")
        self.build_login_ui()

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x500")
    app = ToDoApp(root)
    root.mainloop()