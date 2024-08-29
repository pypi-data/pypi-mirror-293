import functools
import hashlib
import sqlite3
import pickle

class KeyValueStore:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_value_store (
                key text PRIMARY KEY,
                value blob NOT NULL
            );
        ''')
        self.connection.commit()

    def __getitem__(self, key):
        self.cursor.execute('''
            SELECT value FROM key_value_store WHERE key=?;
        ''', (key,))
        value = self.cursor.fetchone()
        if value is None:
            raise KeyError(key)
        return pickle.loads(value[0])

    def __setitem__(self, key, value):
        value = pickle.dumps(value)
        self.cursor.execute('''
            REPLACE INTO key_value_store (key, value) VALUES (?, ?);
        ''', (key, value))
        self.connection.commit()

    def __delitem__(self, key):
        self.cursor.execute('''
            DELETE FROM key_value_store WHERE key=?;
        ''', (key,))
        self.connection.commit()

    def __contains__(self, key):
        self.cursor.execute('''
            SELECT 1 FROM key_value_store WHERE key=?;
        ''', (key,))
        return bool(self.cursor.fetchone())

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        self.cursor.execute('''
            SELECT key FROM key_value_store;
        ''')
        return [key[0] for key in self.cursor.fetchall()]

    def items(self):
        self.cursor.execute('''
            SELECT key, value FROM key_value_store;
        ''')
        return [(key, pickle.loads(value)) for key, value in self.cursor.fetchall()]

    def __len__(self):
        self.cursor.execute('''
            SELECT COUNT(*) FROM key_value_store;
        ''')
        return self.cursor.fetchone()[0]

def memoize(store):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{hashlib.md5(str(args).encode('utf-8')).hexdigest()}:{hashlib.md5(str(kwargs).encode('utf-8')).hexdigest()}"
            try:
                return store[key]
            except KeyError:
                result = func(*args, **kwargs)
                store[key] = result
                return result
        return wrapper
    return decorator

