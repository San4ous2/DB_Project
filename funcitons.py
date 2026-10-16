import sqlite3
from contextlib import closing
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("AI_Provider_Platform.db")


def connect():
    database = sqlite3.connect(DATABASE_PATH)
    database.execute("PRAGMA foreign_keys = ON")
    return database


def add_user(nickname, email):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                'INSERT INTO "Users" (nickname, email) VALUES (?, ?)',
                (nickname, email),
            )
            return cursor.lastrowid


def add_subscription(user_id, plan_type, monthly_limit):
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


def add_api_key(user_id, key_value):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO api_keys (user_id, key_value) VALUES (?, ?)",
                (user_id, key_value),
            )
            return cursor.lastrowid


def add_category(name):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO categories (name) VALUES (?)",
                (name,),
            )
            return cursor.lastrowid


def add_model(category_id, name, param_count):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO models (category_id, name, param_count) "
                "VALUES (?, ?, ?)",
                (category_id, name, param_count),
            )
            return cursor.lastrowid


def add_chat(user_id, model_id, title):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO chats (user_id, model_id, title) VALUES (?, ?, ?)",
                (user_id, model_id, title),
            )
            return cursor.lastrowid


def add_prompt(user_id, title, body):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO prompts (user_id, title, body) VALUES (?, ?, ?)",
                (user_id, title, body),
            )
            return cursor.lastrowid


def add_dataset(name, file_size):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO datasets (name, file_size) VALUES (?, ?)",
                (name, file_size),
            )
            return cursor.lastrowid


def add_fine_tuning_job(model_id, dataset_id, status):
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                "INSERT INTO fine_tuning_jobs (model_id, dataset_id, status) "
                "VALUES (?, ?, ?)",
                (model_id, dataset_id, status),
            )
            return cursor.lastrowid


def get_users():
    with closing(connect()) as database:
        return database.execute(
            'SELECT id, nickname, email FROM "Users" ORDER BY id'
        ).fetchall()


def get_subscriptions():
    with closing(connect()) as database:
        return database.execute(
            "SELECT id, user_id, plan_type, monthly_limit "
            "FROM subscriptions ORDER BY id"
        ).fetchall()


def get_billing():
    with closing(connect()) as database:
        return database.execute(
            "SELECT id, user_id, amount, transaction_type, created_at "
            "FROM billing ORDER BY id"
        ).fetchall()


def get_api_keys():
    with closing(connect()) as database:
        return database.execute(
            "SELECT id, user_id, key_value FROM api_keys ORDER BY id"
        ).fetchall()


def get_categories():
    with closing(connect()) as database:
        return database.execute(
            "SELECT id, name FROM categories ORDER BY id"
        ).fetchall()


def get_models():
    with closing(connect()) as database:
        return database.execute(
            "SELECT id, category_id, name, param_count FROM models ORDER BY id"
        ).fetchall()


def get_chats():
    with closing(connect()) as database:
        return database.execute(
            "SELECT id, user_id, model_id, title FROM chats ORDER BY id"
        ).fetchall()


def get_prompts():
    with closing(connect()) as database:
        return database.execute(
            "SELECT id, user_id, title, body FROM prompts ORDER BY id"
        ).fetchall()


def get_datasets():
    with closing(connect()) as database:
        return database.execute(
            "SELECT id, name, file_size FROM datasets ORDER BY id"
        ).fetchall()


def get_fine_tuning_jobs():
    with closing(connect()) as database:
        return database.execute(
            "SELECT id, model_id, dataset_id, status "
            "FROM fine_tuning_jobs ORDER BY id"
        ).fetchall()