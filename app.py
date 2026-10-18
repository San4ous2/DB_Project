import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
 
import funcitons
 
TABLES = {
    "Users": ["nickname", "email"],
    "subscriptions": ["user_id", "plan_type", "monthly_limit"],
    "billing": ["user_id", "amount", "transaction_type", "created_at"],
    "api_keys": ["user_id", "key_value"],
    "categories": ["name"],
    "models": ["category_id", "name", "param_count"],
    "chats": ["user_id", "model_id", "title"],
    "prompts": ["user_id", "title", "body"],
    "datasets": ["name", "file_size"],
    "fine_tuning_jobs": ["model_id", "dataset_id", "status"],
}
 
 
def show_rows(rows, columns):
    tree.delete(*tree.get_children())
    tree["columns"] = columns
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=130)
    for row in rows:
        tree.insert("", "end", iid=str(row[0]), values=row)
 
 
def load_table():
    table = table_var.get()
    columns = TABLES[table]
    search_field_box["values"] = columns
    search_field_var.set(columns[0])
    rows = getattr(funcitons, "get_" + table)()
    show_rows(rows, ["id"] + columns)
 
 
def search():
    text = search_entry.get().strip()
    if not text:
        load_table()
        return
    table = table_var.get()
    rows = funcitons.search_records(table, search_field_var.get(), f"%{text}%")
    show_rows(rows, ["id"] + TABLES[table])
 
 
def selected_id():
    selection = tree.selection()
    if not selection:
        messagebox.showinfo("Nothing selected", "Select a record first.")
        return None
    return selection[0]
 
 
def ask_for_values(title, table, current_values=None):
    values = []
    for i, column in enumerate(TABLES[table]):
        start = current_values[i] if current_values else ""
        answer = simpledialog.askstring(title, column, initialvalue=start, parent=root)
        if answer is None:
            return None
        answer = answer.strip()
        values.append(int(answer) if answer.isdigit() else answer)
    return values
 
 
def add_record():
    table = table_var.get()
    values = ask_for_values("Add " + table, table)
    if values is not None:
        try:
            getattr(funcitons, "add_" + table)(*values)
        except sqlite3.Error as error:
            messagebox.showerror("Database error", str(error))
        load_table()
 
 
def edit_record():
    record_id = selected_id()
    if record_id is None:
        return
    table = table_var.get()
    current_values = tree.item(record_id, "values")[1:]
    values = ask_for_values(f"Edit record {record_id}", table, current_values)
    if values is not None:
        try:
            funcitons.update_record(table, TABLES[table], values, int(record_id))
        except sqlite3.Error as error:
            messagebox.showerror("Database error", str(error))
        load_table()
 
 
def delete_record():
    record_id = selected_id()
    if record_id is None:
        return
    if messagebox.askyesno("Confirm", f"Delete record {record_id}?"):
        try:
            funcitons.delete_record(table_var.get(), int(record_id))
        except sqlite3.Error as error:
            messagebox.showerror("Database error", str(error))
    load_table()
 
 
root = tk.Tk()
root.title("AI Provider Platform")
 
top = ttk.Frame(root, padding=8)
top.pack(fill="x")
 
table_var = tk.StringVar(value="Users")
table_box = ttk.Combobox(top, textvariable=table_var, values=list(TABLES), state="readonly")
table_box.bind("<<ComboboxSelected>>", load_table)
table_box.pack(side="left")
 
ttk.Label(top, text="Search in").pack(side="left", padx=(16, 4))
search_field_var = tk.StringVar()
search_field_box = ttk.Combobox(top, textvariable=search_field_var, state="readonly", width=14)
search_field_box.pack(side="left")
search_entry = ttk.Entry(top, width=16)
search_entry.pack(side="left", padx=4)
ttk.Button(top, text="Search", command=search).pack(side="left")
 
tree = ttk.Treeview(root, show="headings", selectmode="browse")
tree.pack(fill="both", expand=True, padx=8)
 
buttons = ttk.Frame(root, padding=8)
buttons.pack(fill="x")
ttk.Button(buttons, text="Add", command=add_record).pack(side="left", padx=(0, 8))
ttk.Button(buttons, text="Edit selected", command=edit_record).pack(side="left", padx=(0, 8))
ttk.Button(buttons, text="Delete selected", command=delete_record).pack(side="left")
 
load_table()
root.mainloop()