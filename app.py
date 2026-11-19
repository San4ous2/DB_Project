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

COLORS = {
    "bg": "#0a101f",
    "panel": "#0d1526",
    "card": "#111827",
    "border": "#1e293b",
    "text": "#f1f5f9",
    "muted": "#94a3b8",
    "accent": "#22c55e",
    "accent_hover": "#16a34a",
    "accent_light": "#4ade80",
    "accent_text": "#04120a",
    "nav_active": "#132a1e",
    "input": "#0f172a",
    "heading": "#172033",
    "row_alt": "#0e1626",
    "danger": "#f87171",
    "danger_bg": "#3b1717",
    "danger_hover": "#4c1d1d",
    "button": "#1e293b",
    "button_hover": "#273449",
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

LOGO = [
    "6,6 44,6 44,28 26,28 26,60 52,86 6,86 6,62 24,62 24,44 6,26",
    "64,6 94,36 94,86 64,56",
]


def make_logo(parent, size, color, background):
    canvas = tk.Canvas(
        parent, width=size, height=size, bg=background, highlightthickness=0
    )
    scale = size / 100
    for points in LOGO:
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
        parent, bg=COLORS["card"], highlightbackground=COLORS["border"],
        highlightthickness=1,
    )
    card.pack(side="left", fill="x", expand=True, padx=padx)
    tk.Label(
        card, text=label.upper(), bg=COLORS["card"], fg=COLORS["muted"],
        font=("Consolas", 8),
    ).pack(anchor="w", padx=14, pady=(10, 0))
    tk.Label(
        card, textvariable=variable, bg=COLORS["card"], fg=COLORS["text"],
        font=("Segoe UI", 17, "bold"),
    ).pack(anchor="w", padx=14, pady=(0, 10))


def show_rows(rows, columns):
    tree.delete(*tree.get_children())
    tree["columns"] = columns
    for column in columns:
        label = "ID" if column == "id" else column.replace("_", " ").title()
        tree.heading(column, text=label, anchor="w")
        tree.column(column, width=WIDTHS.get(column, 140), anchor="w")
    for index, row in enumerate(rows):
        tag = "even" if index % 2 == 0 else "odd"
        tree.insert("", "end", iid=str(row[0]), values=row, tags=(tag,))


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
root.configure(bg=COLORS["bg"])
root.geometry("1220x740")
root.minsize(980, 600)

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background=COLORS["bg"])
style.configure(
    "TLabel", background=COLORS["bg"], foreground=COLORS["text"],
    font=("Segoe UI", 10),
)
style.configure(
    "Muted.TLabel", background=COLORS["bg"], foreground=COLORS["muted"],
    font=("Segoe UI", 9),
)
style.configure(
    "Treeview", background=COLORS["card"], fieldbackground=COLORS["card"],
    foreground=COLORS["text"], rowheight=30, borderwidth=0,
    bordercolor=COLORS["card"], lightcolor=COLORS["card"],
    darkcolor=COLORS["card"], font=("Segoe UI", 10),
)
style.configure(
    "Treeview.Heading", background=COLORS["heading"], foreground=COLORS["muted"],
    font=("Segoe UI", 9, "bold"), relief="flat", borderwidth=0, padding=(10, 8),
)
style.map("Treeview.Heading", background=[("active", COLORS["heading"])])
style.map(
    "Treeview",
    background=[("selected", COLORS["accent"])],
    foreground=[("selected", COLORS["accent_text"])],
)
style.configure(
    "Nav.Treeview", background=COLORS["panel"], fieldbackground=COLORS["panel"],
    foreground=COLORS["muted"], borderwidth=0, rowheight=34,
    bordercolor=COLORS["panel"], lightcolor=COLORS["panel"],
    darkcolor=COLORS["panel"], font=("Segoe UI", 10),
)
style.configure(
    "Nav.Treeview.Heading", background=COLORS["panel"],
    foreground=COLORS["muted"], font=("Consolas", 8), relief="flat",
    borderwidth=0, padding=(8, 8),
)
style.map(
    "Nav.Treeview",
    background=[("selected", COLORS["nav_active"])],
    foreground=[("selected", COLORS["accent_light"])],
)
style.configure(
    "TButton", font=("Segoe UI", 10), padding=(16, 8), borderwidth=0,
    background=COLORS["button"], foreground=COLORS["text"],
)
style.map(
    "TButton",
    background=[("active", COLORS["button_hover"])],
    foreground=[("active", COLORS["text"])],
)
style.configure(
    "Accent.TButton", background=COLORS["accent"], foreground=COLORS["accent_text"],
)
style.map(
    "Accent.TButton",
    background=[("active", COLORS["accent_hover"])],
    foreground=[("active", COLORS["accent_text"])],
)
style.configure(
    "Danger.TButton", background=COLORS["danger_bg"], foreground=COLORS["danger"],
)
style.map(
    "Danger.TButton",
    background=[("active", COLORS["danger_hover"])],
    foreground=[("active", COLORS["danger"])],
)
style.configure(
    "TCombobox", fieldbackground=COLORS["input"], background=COLORS["input"],
    foreground=COLORS["text"], arrowcolor=COLORS["muted"],
    bordercolor=COLORS["border"], lightcolor=COLORS["border"],
    darkcolor=COLORS["border"], padding=6,
)
style.map(
    "TCombobox",
    fieldbackground=[("readonly", COLORS["input"])],
    foreground=[("readonly", COLORS["text"])],
    selectbackground=[("readonly", COLORS["input"])],
    selectforeground=[("readonly", COLORS["text"])],
)
style.configure(
    "TEntry", fieldbackground=COLORS["input"], foreground=COLORS["text"],
    insertcolor=COLORS["text"], bordercolor=COLORS["border"],
    lightcolor=COLORS["border"], darkcolor=COLORS["border"], padding=6,
)
style.configure(
    "Vertical.TScrollbar", background=COLORS["border"],
    troughcolor=COLORS["card"], bordercolor=COLORS["card"],
    lightcolor=COLORS["border"], darkcolor=COLORS["border"],
    arrowcolor=COLORS["muted"], relief="flat",
)

root.option_add("*TCombobox*Listbox.background", COLORS["input"])
root.option_add("*TCombobox*Listbox.foreground", COLORS["text"])
root.option_add("*TCombobox*Listbox.selectBackground", COLORS["accent"])
root.option_add("*TCombobox*Listbox.selectForeground", COLORS["accent_text"])

header = tk.Frame(root, bg=COLORS["panel"])
header.pack(fill="x")

header_inner = tk.Frame(header, bg=COLORS["panel"], padx=20, pady=12)
header_inner.pack(fill="x")

make_logo(header_inner, 28, COLORS["accent"], COLORS["panel"]).pack(
    side="left", padx=(0, 10)
)

brand = tk.Frame(header_inner, bg=COLORS["panel"])
brand.pack(side="left")
tk.Label(
    brand, text="SMERKIL", bg=COLORS["panel"], fg=COLORS["text"],
    font=("Consolas", 13, "bold"),
).pack(side="left")
tk.Label(
    brand, text=" TECHNOLOGIES", bg=COLORS["panel"], fg=COLORS["muted"],
    font=("Consolas", 11),
).pack(side="left")

tk.Label(
    header_inner, text="AI Provider Platform", bg=COLORS["panel"],
    fg=COLORS["muted"], font=("Segoe UI", 10),
).pack(side="right")

gradient = tk.Canvas(root, height=2, bg=COLORS["panel"], highlightthickness=0)
gradient.pack(fill="x")
gradient.bind("<Configure>", lambda event: paint_gradient(gradient, event.width, 2))

footer = tk.Frame(root, bg=COLORS["panel"])
footer.pack(side="bottom", fill="x")

tk.Label(
    footer, text="SMERKIL Technologies", bg=COLORS["panel"],
    fg=COLORS["muted"], font=("Consolas", 9),
).pack(side="right", padx=20, pady=9)

body = tk.Frame(root, bg=COLORS["bg"])
body.pack(fill="both", expand=True)

sidebar = tk.Frame(body, bg=COLORS["panel"], width=230)
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

tk.Frame(body, bg=COLORS["border"], width=1).pack(side="left", fill="y")

main = tk.Frame(body, bg=COLORS["bg"], padx=22, pady=18)
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

stats = tk.Frame(main, bg=COLORS["bg"])
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

card = tk.Frame(main, bg=COLORS["border"], padx=1, pady=1)
card.pack(fill="both", expand=True)

tree = ttk.Treeview(card, show="headings", selectmode="browse")
scrollbar = ttk.Scrollbar(card, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
tree.tag_configure("even", background=COLORS["card"])
tree.tag_configure("odd", background=COLORS["row_alt"])
tree.bind("<Double-1>", on_double_click)

root.bind("<F5>", load_table)

load_table()
root.mainloop()
