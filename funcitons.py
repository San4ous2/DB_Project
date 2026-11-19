import sqlite3
from contextlib import closing
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("AI_Provider_Platform.db")

QUERIES = {
    "Users": 'SELECT t.id, t.nickname, t.email FROM "Users" t',
    "subscriptions": (
        "SELECT t.id, u.nickname AS user, t.plan_type, t.monthly_limit "
        "FROM subscriptions t JOIN users u ON t.user_id = u.id"
    ),
    "billing": (
        "SELECT t.id, u.nickname AS user, t.amount, t.transaction_type, t.created_at "
        "FROM billing t JOIN users u ON t.user_id = u.id"
    ),
    "api_keys": (
        "SELECT t.id, u.nickname AS user, t.key_value "
        "FROM api_keys t JOIN users u ON t.user_id = u.id"
    ),
    "categories": "SELECT t.id, t.name FROM categories t",
    "models": (
        "SELECT t.id, c.name AS category, t.name AS name, t.param_count "
        "FROM models t JOIN categories c ON t.category_id = c.id"
    ),
    "chats": (
        "SELECT t.id, u.nickname AS user, m.name AS model, t.title "
        "FROM chats t JOIN users u ON t.user_id = u.id "
        "JOIN models m ON t.model_id = m.id"
    ),
    "prompts": (
        "SELECT t.id, u.nickname AS user, t.title, t.body "
        "FROM prompts t JOIN users u ON t.user_id = u.id"
    ),
    "datasets": "SELECT t.id, t.name, t.file_size FROM datasets t",
    "fine_tuning_jobs": (
        "SELECT t.id, m.name AS model, d.name AS dataset, t.status "
        "FROM fine_tuning_jobs t JOIN models m ON t.model_id = m.id "
        "JOIN datasets d ON t.dataset_id = d.id"
    ),
}


def connect():
    database = sqlite3.connect(DATABASE_PATH)
    database.execute("PRAGMA foreign_keys = ON")
    return database


def add_Users(nickname, email):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                'INSERT INTO "Users" (nickname, email) VALUES (?, ?)',
                (nickname, email),
            )
            return cursor.lastrowid


def add_subscriptions(user_id, plan_type, monthly_limit):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO subscriptions (user_id, plan_type, monthly_limit) "
                "VALUES (?, ?, ?)",
                (user_id, plan_type, monthly_limit),
            )
            return cursor.lastrowid


def add_billing(user_id, amount, transaction_type, created_at):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO billing "
                "(user_id, amount, transaction_type, created_at) "
                "VALUES (?, ?, ?, ?)",
                (user_id, amount, transaction_type, created_at),
            )
            return cursor.lastrowid


def add_api_keys(user_id, key_value):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO api_keys (user_id, key_value) VALUES (?, ?)",
                (user_id, key_value),
            )
            return cursor.lastrowid


def add_categories(name):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO categories (name) VALUES (?)",
                (name,),
            )
            return cursor.lastrowid


def add_models(category_id, name, param_count):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO models (category_id, name, param_count) "
                "VALUES (?, ?, ?)",
                (category_id, name, param_count),
            )
            return cursor.lastrowid


def add_chats(user_id, model_id, title):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO chats (user_id, model_id, title) VALUES (?, ?, ?)",
                (user_id, model_id, title),
            )
            return cursor.lastrowid


def add_prompts(user_id, title, body):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO prompts (user_id, title, body) VALUES (?, ?, ?)",
                (user_id, title, body),
            )
            return cursor.lastrowid


def add_datasets(name, file_size):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO datasets (name, file_size) VALUES (?, ?)",
                (name, file_size),
            )
            return cursor.lastrowid


def add_fine_tuning_jobs(model_id, dataset_id, status):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO fine_tuning_jobs (model_id, dataset_id, status) "
                "VALUES (?, ?, ?)",
                (model_id, dataset_id, status),
            )
            return cursor.lastrowid


def get_table(table):
    with closing(connect()) as database:
        cursor = database.execute(QUERIES[table] + " ORDER BY t.id")
        return [name[0] for name in cursor.description], cursor.fetchall()


def count_rows(table):
    with closing(connect()) as database:
        return database.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]


def get_record(table, record_id):
    with closing(connect()) as database:
        return database.execute(
            f"SELECT * FROM {table} WHERE id = ?", (record_id,)
        ).fetchone()


def delete_record(table, record_id):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                f"DELETE FROM {table} WHERE id = ?", (record_id,)
            )
            return cursor.rowcount


def update_record(table, columns, values, record_id):
    assignments = ", ".join(f"{column} = ?" for column in columns)
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                f"UPDATE {table} SET {assignments} WHERE id = ?",
                (*values, record_id),
            )
            return cursor.rowcount


def search_records(table, column, pattern):
    with closing(connect()) as database:
        cursor = database.execute(
            "SELECT * FROM (" + QUERIES[table] + ") "
            "WHERE " + column + " LIKE ? ORDER BY id",
            (pattern,),
        )
        return [name[0] for name in cursor.description], cursor.fetchall()
