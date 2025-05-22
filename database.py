import sqlite3

DB_PATH = "/home/runner/applicants.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS applicants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                fio TEXT,
                contact TEXT,
                age TEXT,
                edu TEXT,
                year TEXT,
                exp TEXT,
                about TEXT
            )
        """)
        conn.commit()
        print("База данных успешно инициализирована")  # Логирование
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
init_db()

def save_applicant(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Обработка числовых полей: если None или пусто, подставляем None
    age = data.get("age")
    if age is not None and age != '':
        try:
            age = int(age)
        except ValueError:
            age = None
    else:
        age = None

    year = data.get("year")
    if year is not None and year != '':
        try:
            year = int(year)
        except ValueError:
            year = None
    else:
        year = None

    cur.execute("""
        INSERT INTO applicants (
            telegram_id, fio, contact, age, edu, year, exp, about
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("telegram_id"),
        data.get("fio"),
        data.get("contact"),
        data.get("age"),
        data.get("edu"),
        data.get("year"),
        data.get("exp"),
        data.get("about")
    ))
    conn.commit()
    cur.close()
    conn.close()

def get_all_applicants():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM applicants")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results