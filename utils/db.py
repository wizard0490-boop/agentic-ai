import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "health.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            weight_kg REAL,
            height_cm REAL,
            blood_group TEXT,
            conditions TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dosage TEXT,
            frequency TEXT,
            times TEXT,
            start_date TEXT,
            end_date TEXT,
            notes TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS medication_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medication_id INTEGER,
            taken_at TEXT,
            status TEXT,
            FOREIGN KEY(medication_id) REFERENCES medications(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS fitness_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            steps INTEGER DEFAULT 0,
            water_ml INTEGER DEFAULT 0,
            sleep_hours REAL DEFAULT 0,
            exercise_mins INTEGER DEFAULT 0,
            exercise_type TEXT,
            notes TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS diet_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            meal_type TEXT,
            food_item TEXT,
            calories INTEGER,
            protein_g REAL,
            carbs_g REAL,
            fat_g REAL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS vitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            bp_systolic INTEGER,
            bp_diastolic INTEGER,
            heart_rate INTEGER,
            blood_sugar REAL,
            weight_kg REAL,
            temperature REAL,
            spo2 INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS health_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_type TEXT,
            target_value REAL,
            current_value REAL,
            unit TEXT,
            deadline TEXT,
            achieved INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

# ── Medication helpers ────────────────────────────────────────────────────────

def add_medication(name, dosage, frequency, times, start_date, end_date="", notes=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO medications (name, dosage, frequency, times, start_date, end_date, notes) VALUES (?,?,?,?,?,?,?)",
        (name, dosage, frequency, times, start_date, end_date, notes)
    )
    conn.commit(); conn.close()

def get_medications(active_only=True):
    conn = get_connection()
    q = "SELECT * FROM medications WHERE active=1" if active_only else "SELECT * FROM medications"
    rows = conn.execute(q + " ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def log_medication(med_id, status="taken"):
    conn = get_connection()
    conn.execute(
        "INSERT INTO medication_logs (medication_id, taken_at, status) VALUES (?,?,?)",
        (med_id, datetime.now().isoformat(), status)
    )
    conn.commit(); conn.close()

def get_adherence_rate(med_id, days=7):
    conn = get_connection()
    total = conn.execute(
        "SELECT COUNT(*) FROM medication_logs WHERE medication_id=? AND taken_at >= date('now',?)",
        (med_id, f"-{days} days")
    ).fetchone()[0]
    taken = conn.execute(
        "SELECT COUNT(*) FROM medication_logs WHERE medication_id=? AND status='taken' AND taken_at >= date('now',?)",
        (med_id, f"-{days} days")
    ).fetchone()[0]
    conn.close()
    return round((taken / total * 100) if total else 0, 1)

def delete_medication(med_id):
    conn = get_connection()
    conn.execute("UPDATE medications SET active=0 WHERE id=?", (med_id,))
    conn.commit(); conn.close()

# ── Fitness helpers ───────────────────────────────────────────────────────────

def log_fitness(date, steps, water_ml, sleep_hours, exercise_mins, exercise_type="", notes=""):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM fitness_logs WHERE date=?", (date,)).fetchone()
    if existing:
        conn.execute(
            "UPDATE fitness_logs SET steps=?,water_ml=?,sleep_hours=?,exercise_mins=?,exercise_type=?,notes=? WHERE date=?",
            (steps, water_ml, sleep_hours, exercise_mins, exercise_type, notes, date)
        )
    else:
        conn.execute(
            "INSERT INTO fitness_logs (date,steps,water_ml,sleep_hours,exercise_mins,exercise_type,notes) VALUES (?,?,?,?,?,?,?)",
            (date, steps, water_ml, sleep_hours, exercise_mins, exercise_type, notes)
        )
    conn.commit(); conn.close()

def get_fitness_logs(days=7):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM fitness_logs WHERE date >= date('now',?) ORDER BY date DESC",
        (f"-{days} days",)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ── Vitals helpers ────────────────────────────────────────────────────────────

def log_vitals(date, bp_sys=None, bp_dia=None, hr=None, sugar=None, weight=None, temp=None, spo2=None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO vitals (date,bp_systolic,bp_diastolic,heart_rate,blood_sugar,weight_kg,temperature,spo2) VALUES (?,?,?,?,?,?,?,?)",
        (date, bp_sys, bp_dia, hr, sugar, weight, temp, spo2)
    )
    conn.commit(); conn.close()

def get_vitals(days=30):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM vitals WHERE date >= date('now',?) ORDER BY date DESC",
        (f"-{days} days",)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ── User helpers ──────────────────────────────────────────────────────────────

def save_profile(name, age, gender, weight, height, blood_group, conditions):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
    if existing:
        conn.execute(
            "UPDATE users SET name=?,age=?,gender=?,weight_kg=?,height_cm=?,blood_group=?,conditions=? WHERE id=?",
            (name, age, gender, weight, height, blood_group, conditions, existing["id"])
        )
    else:
        conn.execute(
            "INSERT INTO users (name,age,gender,weight_kg,height_cm,blood_group,conditions) VALUES (?,?,?,?,?,?,?)",
            (name, age, gender, weight, height, blood_group, conditions)
        )
    conn.commit(); conn.close()

def get_profile():
    conn = get_connection()
    row = conn.execute("SELECT * FROM users LIMIT 1").fetchone()
    conn.close()
    return dict(row) if row else {}

# ── Diet helpers ──────────────────────────────────────────────────────────────

def log_diet(date, meal_type, food_item, calories, protein, carbs, fat):
    conn = get_connection()
    conn.execute(
        "INSERT INTO diet_logs (date,meal_type,food_item,calories,protein_g,carbs_g,fat_g) VALUES (?,?,?,?,?,?,?)",
        (date, meal_type, food_item, calories, protein, carbs, fat)
    )
    conn.commit(); conn.close()

def get_diet_logs(date):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM diet_logs WHERE date=? ORDER BY id", (date,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ── Goals helpers ─────────────────────────────────────────────────────────────

def add_goal(goal_type, target, current, unit, deadline):
    conn = get_connection()
    conn.execute(
        "INSERT INTO health_goals (goal_type,target_value,current_value,unit,deadline) VALUES (?,?,?,?,?)",
        (goal_type, target, current, unit, deadline)
    )
    conn.commit(); conn.close()

def get_goals():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM health_goals ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

