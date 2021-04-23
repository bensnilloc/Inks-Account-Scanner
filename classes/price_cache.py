import sqlite3
import time
import json
import os

class PriceCache:
    def __init__(self):
        self.path = "data/database/cache.db"
        self.max_cache = 1209600

    def get_cached_item_price(self, item):
        with SQLite(self.path) as cursor:
            item = cursor.execute(f"""select price from cache where item='{item}'""").fetchone()
            if item:
                return item[0]
        return "item_does_not_exist"

    def create_cached_item_price(self, item, price):
        with SQLite(self.path) as cursor:
            if not cursor.execute(f"""select price from cache where item='{item}'""").fetchone():
                cursor.execute("""insert into cache (item, price, last_updated) values (?,?,?)""", (item, price, int(time.time(),)))

    def update_cached_item_price(self, item, price):
        if int(time.time()) - self.get_last_updated(item) >= self.max_cache:
            with SQLite(self.path) as cursor:
                cursor.execute(f"""update cache set price = ?,last_updated = ? where item = '{item}' """, (price, int(time.time(),)))

    def get_last_updated(self, item):
        with SQLite(self.path) as cursor:
            return int(cursor.execute(f"""select last_updated from cache where item='{item}'""").fetchone()[0])

class SQLite:
    def __init__(self, file):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory  = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()
