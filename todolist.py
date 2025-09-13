import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Data storage
        self.tasks = []
        self.data_file = "tasks.json"
        
        # Load existing tasks
        self.load_tasks()
        
        # Create GUI
        self.create_widgets()
        
        # Load tasks into listbox
        self.refresh_task_list()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="📝 To-Do List Manager", 
                              font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title_label.pack(pady=(0, 20))
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Task entry
        tk.Label(input_frame, text="New Task:", font=("Arial", 12), 
                bg="#f0f0f0", fg="#34495e").pack(anchor=tk.W)
        
        self.task_entry = tk.Entry(input_frame, font=("Arial", 12), width=50)
        self.task_entry.pack(fill=tk.X, pady=(5, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Priority selection
        priority_frame = tk.Frame(input_frame, bg="#f0f0f0")
        priority_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(priority_frame, text="Priority:", font=("Arial", 10), 
                bg="#f0f0f0", fg="#34495e").pack(side=tk.LEFT)
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(priority_frame, textvariable=self.priority_var, 
                                     values=["High", "Medium", "Low"], state="readonly", width=10)
        priority_combo.pack(side=tk.LEFT, padx=(10, 20))
        
        # Due date entry
        tk.Label(priority_frame, text="Due Date (YYYY-MM-DD):", font=("Arial", 10), 
                bg="#f0f0f0", fg="#34495e").pack(side=tk.LEFT)
        
        self.due_date_entry = tk.Entry(priority_frame, font=("Arial", 10), width=12)
        self.due_date_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add task button
        add_btn = tk.Button(button_frame, text="➕ Add Task", command=self.add_task,
                           bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                           relief=tk.FLAT, padx=20, pady=5)
        add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Update task button
        update_btn = tk.Button(button_frame, text="✏️ Update Task", command=self.update_task,
                              bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                              relief=tk.FLAT, padx=20, pady=5)
        update_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Complete task button
        complete_btn = tk.Button(button_frame, text="✅ Mark Complete", command=self.complete_task,
                                bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                                relief=tk.FLAT, padx=20, pady=5)
        complete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Delete task button
        delete_btn = tk.Button(button_frame, text="🗑️ Delete Task", command=self.delete_task,
                              bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                              relief=tk.FLAT, padx=20, pady=5)
        delete_btn.pack(side=tk.LEFT)
        
        # Filter frame
        filter_frame = tk.Frame(main_frame, bg="#f0f0f0")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(filter_frame, text="Filter by:", font=("Arial", 10), 
                bg="#f0f0f0", fg="#34495e").pack(side=tk.LEFT)
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["All", "Pending", "Completed", "High Priority", "Medium Priority", "Low Priority"],
                                   state="readonly", width=15)
        filter_combo.pack(side=tk.LEFT, padx=(10, 20))
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())
        
        # Search frame
        search_frame = tk.Frame(filter_frame, bg="#f0f0f0")
        search_frame.pack(side=tk.RIGHT)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10), 
                bg="#f0f0f0", fg="#34495e").pack(side=tk.LEFT)
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=20)
        self.search_entry.pack(side=tk.LEFT, padx=(10, 0))
        self.search_entry.bind('<KeyRelease>', lambda e: self.refresh_task_list())
        
        # Task list frame
        list_frame = tk.Frame(main_frame, bg="white", relief=tk.SUNKEN, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Task listbox
        self.task_listbox = tk.Listbox(list_frame, font=("Courier", 10), 
                                      yscrollcommand=scrollbar.set,
                                      selectmode=tk.SINGLE, bg="white")
        self.task_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Statistics frame
        stats_frame = tk.Frame(main_frame, bg="#ecf0f1", relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.stats_label = tk.Label(stats_frame, text="", font=("Arial", 10), 
                                   bg="#ecf0f1", fg="#2c3e50", pady=10)
        self.stats_label.pack()
        
        # Update statistics
        self.update_statistics()
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        
        # Validate due date
        due_date = None
        if self.due_date_entry.get().strip():
            try:
                due_date = datetime.strptime(self.due_date_entry.get().strip(), "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return
        
        task = {
            'id': len(self.tasks) + 1,
            'text': task_text,
            'priority': self.priority_var.get(),
            'due_date': due_date.isoformat() if due_date else None,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_task_list()
        self.update_statistics()
        
        # Clear input fields
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Task added successfully!")
    
    def update_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to update!")
            return
        
        task_index = self.get_task_index_from_selection(selection[0])
        if task_index is None:
            return
        
        current_task = self.tasks[task_index]
        
        # Get new task text
        new_text = simpledialog.askstring("Update Task", "Enter new task:", 
                                         initialvalue=current_task['text'])
        if new_text is None:
            return
        
        if new_text.strip():
            current_task['text'] = new_text.strip()
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Success", "Task updated successfully!")
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")
    
    def complete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to mark as complete!")
            return
        
        task_index = self.get_task_index_from_selection(selection[0])
        if task_index is None:
            return
        
        self.tasks[task_index]['completed'] = not self.tasks[task_index]['completed']
        status = "completed" if self.tasks[task_index]['completed'] else "pending"
        
        self.save_tasks()
        self.refresh_task_list()
        self.update_statistics()
        
        messagebox.showinfo("Success", f"Task marked as {status}!")
    
    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            task_index = self.get_task_index_from_selection(selection[0])
            if task_index is not None:
                del self.tasks[task_index]
                self.save_tasks()
                self.refresh_task_list()
                self.update_statistics()
                messagebox.showinfo("Success", "Task deleted successfully!")
    
    def get_task_index_from_selection(self, listbox_index):
        # Get the filtered tasks currently displayed
        filtered_tasks = self.get_filtered_tasks()
        if listbox_index < len(filtered_tasks):
            selected_task = filtered_tasks[listbox_index]
            # Find the actual index in self.tasks
            for i, task in enumerate(self.tasks):
                if task['id'] == selected_task['id']:
                    return i
        return None
    
    def get_filtered_tasks(self):
        filtered_tasks = self.tasks.copy()
        
        # Apply status filter
        filter_value = self.filter_var.get()
        if filter_value == "Pending":
            filtered_tasks = [t for t in filtered_tasks if not t['completed']]
        elif filter_value == "Completed":
            filtered_tasks = [t for t in filtered_tasks if t['completed']]
        elif filter_value in ["High Priority", "Medium Priority", "Low Priority"]:
            priority = filter_value.split()[0]
            filtered_tasks = [t for t in filtered_tasks if t['priority'] == priority]
        
        # Apply search filter
        search_term = self.search_entry.get().strip().lower()
        if search_term:
            filtered_tasks = [t for t in filtered_tasks if search_term in t['text'].lower()]
        
        return filtered_tasks
    
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        
        filtered_tasks = self.get_filtered_tasks()
        
        for task in filtered_tasks:
            # Format task display
            status = "✅" if task['completed'] else "⏳"
            priority_symbol = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            priority = priority_symbol.get(task['priority'], "⚪")
            
            due_info = ""
            if task['due_date']:
                due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                days_left = (due_date - date.today()).days
                if days_left < 0:
                    due_info = f" (OVERDUE by {abs(days_left)} days)"
                elif days_left == 0:
                    due_info = " (DUE TODAY)"
                elif days_left <= 3:
                    due_info = f" (Due in {days_left} days)"
            
            task_display = f"{status} {priority} {task['text']}{due_info}"
            self.task_listbox.insert(tk.END, task_display)
            
            # Color coding for overdue and due today tasks
            if "OVERDUE" in due_info:
                self.task_listbox.itemconfig(tk.END, {'fg': '#e74c3c'})
            elif "DUE TODAY" in due_info:
                self.task_listbox.itemconfig(tk.END, {'fg': '#f39c12'})
            elif task['completed']:
                self.task_listbox.itemconfig(tk.END, {'fg': '#95a5a6'})
    
    def update_statistics(self):
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task['completed'])
        pending_tasks = total_tasks - completed_tasks
        
        # Count overdue tasks
        overdue_tasks = 0
        for task in self.tasks:
            if task['due_date'] and not task['completed']:
                due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                if due_date < date.today():
                    overdue_tasks += 1
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        stats_text = f"Total: {total_tasks} | Completed: {completed_tasks} | Pending: {pending_tasks} | Overdue: {overdue_tasks} | Completion Rate: {completion_rate:.1f}%"
        self.stats_label.config(text=stats_text)
    
    def save_tasks(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
    
    def load_tasks(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
            self.tasks = []

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
