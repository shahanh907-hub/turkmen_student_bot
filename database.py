import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    
    # Пользователи
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        registered_date TEXT
    )
    ''')
    
    # Чёрный список
    cur.execute('''
    CREATE TABLE IF NOT EXISTS blacklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_login TEXT,
        reason TEXT,
        added_by INTEGER,
        date TEXT
    )
    ''')
    
    # Поездки
    cur.execute('''
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        trip_text TEXT,
        contacts TEXT,
        created_date TEXT
    )
    ''')
    
    # Жильё
    cur.execute('''
    CREATE TABLE IF NOT EXISTS housing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        housing_text TEXT,
        contacts TEXT,
        created_date TEXT
    )
    ''')
    
    # Обмен валют - белый список
    cur.execute('''
    CREATE TABLE IF NOT EXISTS exchangers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        city TEXT,
        contact TEXT,
        rates TEXT,
        reviews INTEGER DEFAULT 0,
        rating REAL DEFAULT 0,
        added_by INTEGER,
        verified INTEGER DEFAULT 0,
        date TEXT
    )
    ''')
    
    # Обмен валют - чёрный список
    cur.execute('''
    CREATE TABLE IF NOT EXISTS scam_exchangers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        contact TEXT,
        reason TEXT,
        added_by INTEGER,
        date TEXT
    )
    ''')
    
    # Отзывы об обменниках
    cur.execute('''
    CREATE TABLE IF NOT EXISTS exchanger_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exchanger_id INTEGER,
        user_id INTEGER,
        rating INTEGER,
        comment TEXT,
        date TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

def add_user(user_id, username, first_name):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if not cur.fetchone():
        cur.execute('''
        INSERT INTO users (user_id, username, first_name, registered_date)
        VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('SELECT username FROM users WHERE user_id = ?', (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

def add_to_blacklist(tg_login, reason, added_by):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO blacklist (tg_login, reason, added_by, date)
    VALUES (?, ?, ?, ?)
    ''', (tg_login, reason, added_by, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_recent_blacklist(limit=5):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('SELECT tg_login, reason FROM blacklist ORDER BY id DESC LIMIT ?', (limit,))
    items = cur.fetchall()
    conn.close()
    return items

def check_user_in_blacklist(tg_login):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*), GROUP_CONCAT(reason, " | ") FROM blacklist WHERE tg_login = ?', (tg_login,))
    result = cur.fetchone()
    conn.close()
    return result

def add_trip(user_id, trip_text, contacts):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO trips (user_id, trip_text, contacts, created_date)
    VALUES (?, ?, ?, ?)
    ''', (user_id, trip_text, contacts, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_trips(limit=10):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    SELECT user_id, trip_text, contacts FROM trips ORDER BY id DESC LIMIT ?
    ''', (limit,))
    trips = cur.fetchall()
    conn.close()
    return trips

def add_housing(user_id, housing_text, contacts):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO housing (user_id, housing_text, contacts, created_date)
    VALUES (?, ?, ?, ?)
    ''', (user_id, housing_text, contacts, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_housing(limit=10):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    SELECT user_id, housing_text, contacts FROM housing ORDER BY id DESC LIMIT ?
    ''', (limit,))
    items = cur.fetchall()
    conn.close()
    return items

def add_exchanger(name, city, contact, rates, added_by):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO exchangers (name, city, contact, rates, added_by, date)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, city, contact, rates, added_by, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_exchangers():
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    SELECT id, name, city, contact, rates, rating, reviews 
    FROM exchangers WHERE verified = 1 ORDER BY rating DESC
    ''')
    items = cur.fetchall()
    conn.close()
    return items

def get_scam_exchangers():
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('SELECT name, contact, reason FROM scam_exchangers ORDER BY id DESC LIMIT 10')
    items = cur.fetchall()
    conn.close()
    return items