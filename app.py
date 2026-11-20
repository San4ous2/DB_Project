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

WIDTHS = {
    "id": 70,
    "user": 160,
    "nickname": 170,
    "email": 230,
    "category": 160,
    "model": 170,
    "dataset": 180,
    "title": 230,
    "body": 320,
    "key_value": 230,
    "created_at": 180,
    "param_count": 120,
    "file_size": 130,
    "monthly_limit": 130,
    "amount": 110,
}

def make_logo(parent, size, color, background):
    canvas = tk.Canvas(
        parent, width=size, height=size, bg=background, highlightthickness=0
    )
    scale = size / 100
    logo_shapes = [
        "6,6 44,6 44,28 26,28 26,60 52,86 6,86 6,62 24,62 24,44 6,26",
        "64,6 94,36 94,86 64,56",
    ]
    for points in logo_shapes:
        coords = []
        for point in points.split():
            x, y = point.split(",")
            coords.extend([float(x) * scale, float(y) * scale])
        canvas.create_polygon(coords, fill=color, outline="")
    return canvas


def paint_gradient(canvas, width, height):
    canvas.delete("all")
    for x in range(width):
        ratio = x / max(width - 1, 1)
        red = int(34 + (74 - 34) * ratio)
        green = int(197 + (222 - 197) * ratio)
        blue = int(94 + (128 - 94) * ratio)
        canvas.create_line(x, 0, x, height, fill=f"#{red:02x}{green:02x}{blue:02x}")


def stat_card(parent, label, variable, padx=(0, 12)):
    card = tk.Frame(
        parent, bg="#111827", highlightbackground="#1e293b",
        highlightthickness=1,
    )
    card.pack(side="left", fill="x", expand=True, padx=padx)
    tk.Label(
        card, text=label.upper(), bg="#111827", fg="#94a3b8",
        font=("Consolas", 8),
    ).pack(anchor="w", padx=14, pady=(10, 0))
    tk.Label(
        card, textvariable=variable, bg="#111827", fg="#f1f5f9",
        font=("Segoe UI", 17, "bold"),
    ).pack(anchor="w", padx=14, pady=(0, 10))


def show_rows(rows, columns):
    tree.delete(*tree.get_children())
    tree["columns"] = columns
    for column in columns:
        label = "ID" if column == "id" else column.replace("_", " ").title()
        tree.heading(column, text=label, anchor="w")
        tree.column(column, width=WIDTHS.get(column, 140), anchor="w")
    for _, row in enumerate(rows):
        tree.insert("", "end", iid=str(row[0]), values=row)


def current_table():
    selection = nav.selection()
    return selection[0] if selection else "Users"


def refresh_counts():
    for name in TABLES:
        nav.item(name, values=(name, funcitons.count_rows(name)))


def update_summary(table, columns, rows):
    title_var.set(table)
    subtitle_var.set(f"{len(rows)} records  ·  {len(columns) - 1} columns")
    records_var.set(str(len(rows)))
    columns_var.set(str(len(columns) - 1))


def load_table(event=None):
    table = current_table()
    columns, rows = funcitons.get_table(table)
    search_field_box["values"] = columns[1:]
    search_field_var.set(columns[1])
    show_rows(rows, columns)
    update_summary(table, columns, rows)
    size_var.set(f"{funcitons.DATABASE_PATH.stat().st_size / 1024:.0f} KB")
    refresh_counts()


def search():
    text = search_entry.get().strip()
    if not text:
        load_table()
        return
    table = current_table()
    columns, rows = funcitons.search_records(
        table, search_field_var.get(), f"%{text}%"
    )
    show_rows(rows, columns)
    update_summary(table, columns, rows)


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
    table = current_table()
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
    table = current_table()
    current_values = funcitons.get_record(table, int(record_id))[1:]
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
            funcitons.delete_record(current_table(), int(record_id))
        except sqlite3.Error as error:
            messagebox.showerror("Database error", str(error))
    load_table()


def on_double_click(event):
    if tree.identify_row(event.y):
        edit_record()


root = tk.Tk()
root.title("AI Provider Platform")
root.configure(bg="#0a101f")
root.geometry("1220x740")
root.minsize(980, 600)

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background="#0a101f")
style.configure(
    "TLabel", background="#0a101f", foreground="#f1f5f9",
    font=("Segoe UI", 10),
)
style.configure(
    "Muted.TLabel", background="#0a101f", foreground="#94a3b8",
    font=("Segoe UI", 9),
)
style.configure(
    "Treeview", background="#111827", fieldbackground="#111827",
    foreground="#f1f5f9", rowheight=30, borderwidth=0,
    bordercolor="#111827", lightcolor="#111827",
    darkcolor="#111827", font=("Segoe UI", 10),
)
style.configure(
    "Treeview.Heading", background="#172033", foreground="#94a3b8",
    font=("Segoe UI", 9, "bold"), relief="flat", borderwidth=0, padding=(10, 8),
)
style.map("Treeview.Heading", background=[("active", "#172033")])
style.map(
    "Treeview",
    background=[("selected", "#22c55e")],
    foreground=[("selected", "#04120a")],
)
style.configure(
    "Nav.Treeview", background="#0d1526", fieldbackground="#0d1526",
    foreground="#94a3b8", borderwidth=0, rowheight=34,
    bordercolor="#0d1526", lightcolor="#0d1526",
    darkcolor="#0d1526", font=("Segoe UI", 10),
)
style.configure(
    "Nav.Treeview.Heading", background="#0d1526",
    foreground="#94a3b8", font=("Consolas", 8), relief="flat",
    borderwidth=0, padding=(8, 8),
)
style.map(
    "Nav.Treeview",
    background=[("selected", "#132a1e")],
    foreground=[("selected", "#4ade80")],
)
style.configure(
    "TButton", font=("Segoe UI", 10), padding=(16, 8), borderwidth=0,
    background="#1e293b", foreground="#f1f5f9",
)
style.map(
    "TButton",
    background=[("active", "#273449")],
    foreground=[("active", "#f1f5f9")],
)
style.configure(
    "Accent.TButton", background="#22c55e", foreground="#04120a",
)
style.map(
    "Accent.TButton",
    background=[("active", "#16a34a")],
    foreground=[("active", "#04120a")],
)
style.configure(
    "Danger.TButton", background="#3b1717", foreground="#f87171",
)
style.map(
    "Danger.TButton",
    background=[("active", "#4c1d1d")],
    foreground=[("active", "#f87171")],
)
style.configure(
    "TCombobox", fieldbackground="#0f172a", background="#0f172a",
    foreground="#f1f5f9", arrowcolor="#94a3b8",
    bordercolor="#1e293b", lightcolor="#1e293b",
    darkcolor="#1e293b", padding=6,
)
style.map(
    "TCombobox",
    fieldbackground=[("readonly", "#0f172a")],
    foreground=[("readonly", "#f1f5f9")],
    selectbackground=[("readonly", "#0f172a")],
    selectforeground=[("readonly", "#f1f5f9")],
)
style.configure(
    "TEntry", fieldbackground="#0f172a", foreground="#f1f5f9",
    insertcolor="#f1f5f9", bordercolor="#1e293b",
    lightcolor="#1e293b", darkcolor="#1e293b", padding=6,
)
style.configure(
    "Vertical.TScrollbar", background="#1e293b",
    troughcolor="#111827", bordercolor="#111827",
    lightcolor="#1e293b", darkcolor="#1e293b",
    arrowcolor="#94a3b8", relief="flat",
)

root.option_add("*TCombobox*Listbox.background", "#0f172a")
root.option_add("*TCombobox*Listbox.foreground", "#f1f5f9")
root.option_add("*TCombobox*Listbox.selectBackground", "#22c55e")
root.option_add("*TCombobox*Listbox.selectForeground", "#04120a")

header = tk.Frame(root, bg="#0d1526")
header.pack(fill="x")

header_inner = tk.Frame(header, bg="#0d1526", padx=20, pady=12)
header_inner.pack(fill="x")

make_logo(header_inner, 28, "#22c55e", "#0d1526").pack(
    side="left", padx=(0, 10)
)

brand = tk.Frame(header_inner, bg="#0d1526")
brand.pack(side="left")
tk.Label(
    brand, text="SMERKIL", bg="#0d1526", fg="#f1f5f9",
    font=("Consolas", 13, "bold"),
).pack(side="left")
tk.Label(
    brand, text=" TECHNOLOGIES", bg="#0d1526", fg="#94a3b8",
    font=("Consolas", 11),
).pack(side="left")

tk.Label(
    header_inner, text="AI Provider Platform", bg="#0d1526",
    fg="#94a3b8", font=("Segoe UI", 10),
).pack(side="right")

gradient = tk.Canvas(root, height=2, bg="#0d1526", highlightthickness=0)
gradient.pack(fill="x")
gradient.bind("<Configure>", lambda event: paint_gradient(gradient, event.width, 2))

footer = tk.Frame(root, bg="#0d1526")
footer.pack(side="bottom", fill="x")

tk.Label(
    footer, text="SMERKIL Technologies", bg="#0d1526",
    fg="#94a3b8", font=("Consolas", 9),
).pack(side="right", padx=20, pady=9)

body = tk.Frame(root, bg="#0a101f")
body.pack(fill="both", expand=True)

sidebar = tk.Frame(body, bg="#0d1526", width=230)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

nav = ttk.Treeview(
    sidebar, columns=("table", "count"), show="headings",
    selectmode="browse", style="Nav.Treeview",
)
nav.heading("table", text="TABLES", anchor="w")
nav.heading("count", text="", anchor="e")
nav.column("table", width=160, anchor="w")
nav.column("count", width=40, anchor="e")
nav.pack(fill="both", expand=True, padx=12, pady=(12, 12))
for name in TABLES:
    nav.insert("", "end", iid=name, values=(name, funcitons.count_rows(name)))
nav.selection_set("Users")
nav.bind("<<TreeviewSelect>>", load_table)

tk.Frame(body, bg="#1e293b", width=1).pack(side="left", fill="y")

main = tk.Frame(body, bg="#0a101f", padx=22, pady=18)
main.pack(side="left", fill="both", expand=True)

page = ttk.Frame(main)
page.pack(fill="x", pady=(0, 14))

titles = ttk.Frame(page)
titles.pack(side="left")
title_var = tk.StringVar()
ttk.Label(
    titles, textvariable=title_var, font=("Segoe UI", 20, "bold"),
).pack(anchor="w")
subtitle_var = tk.StringVar()
ttk.Label(titles, textvariable=subtitle_var, style="Muted.TLabel").pack(
    anchor="w", pady=(2, 0)
)

actions = ttk.Frame(page)
actions.pack(side="right", pady=4)
ttk.Button(actions, text="Add", style="Accent.TButton", command=add_record).pack(
    side="left", padx=(0, 8)
)
ttk.Button(actions, text="Edit", command=edit_record).pack(
    side="left", padx=(0, 8)
)
ttk.Button(
    actions, text="Delete", style="Danger.TButton", command=delete_record
).pack(side="left")

stats = tk.Frame(main, bg="#0a101f")
stats.pack(fill="x", pady=(0, 16))

records_var = tk.StringVar(value="0")
columns_var = tk.StringVar(value="0")
tables_var = tk.StringVar(value=str(len(TABLES)))
size_var = tk.StringVar(value="")
stat_card(stats, "Records", records_var)
stat_card(stats, "Columns", columns_var)
stat_card(stats, "Tables", tables_var)
stat_card(stats, "Database", size_var, padx=(0, 0))

searchbar = ttk.Frame(main)
searchbar.pack(fill="x", pady=(0, 10))

ttk.Label(searchbar, text="Search in", style="Muted.TLabel").pack(
    side="left", padx=(0, 8)
)
search_field_var = tk.StringVar()
search_field_box = ttk.Combobox(
    searchbar, textvariable=search_field_var, state="readonly", width=14
)
search_field_box.pack(side="left")
search_entry = ttk.Entry(searchbar, width=30)
search_entry.pack(side="left", padx=8)
search_entry.bind("<Return>", lambda event: search())
ttk.Button(searchbar, text="Search", style="Accent.TButton", command=search).pack(
    side="left"
)

card = tk.Frame(main, bg="#1e293b", padx=1, pady=1)
card.pack(fill="both", expand=True)

tree = ttk.Treeview(card, show="headings", selectmode="browse")
scrollbar = ttk.Scrollbar(card, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
tree.bind("<Double-1>", on_double_click)

root.bind("<F5>", load_table)

load_table()
root.mainloop()
