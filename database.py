import sqlite3


class Database:
    def __init__(self, db_name="test.sqlite3"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute(self, sql, params=None):
        if params is None:
            params = []
        self.cursor.execute(sql, params)
        self.connection.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def create_table(self, name, columns):
        column_definitions = ', '.join(columns)
        sql = f"CREATE TABLE IF NOT EXISTS {name} ({column_definitions})"
        self.execute(sql)

    def insert_record(self, table, **kwargs):
        columns, values = zip(*kwargs.items())
        values = [str(value) for value in values]
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in values])})"
        self.execute(sql, values)

    def get_record_by_pk(self, table, primary_key, pk_value):
        sql = f"SELECT * FROM {table} WHERE {primary_key} = ?"
        self.execute(sql, (pk_value,))
        return self.fetchone()

    def get_records(self, table, columns, values):
        where_clause = " AND ".join(f"{col} = ?" for col in columns)
        sql = f"SELECT * FROM {table} WHERE {where_clause}"
        self.execute(sql, values)
        return self.fetchall()

    def get_description(self):
        return self.cursor.description

    def fetch_all_records(self, table):
        sql = f"SELECT * FROM {table}"
        self.execute(sql)
        return self.fetchall()

    def get_table_info(self, table_name):
        try:
            self.execute(f"PRAGMA table_info({table_name})")
            return {row[1]: row[2] for row in self.fetchall()}  # Return a dictionary of column names and types
        except sqlite3.OperationalError:
            return None  # Table does not exist

    def alter_table(self, table_name, alterations):
        for alteration in alterations:
            sql = f"ALTER TABLE {table_name} {alteration}"
            self.execute(sql)
