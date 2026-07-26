"""
CS50SQL Final Project — builds solar_data.db from the schema and loads
your existing CSVs (bahawalpur_2023.csv, dubai_2023.csv, riyadh_2023.csv
and their matching _monthly_yield.csv files) into it.

Runs entirely offline — sqlite3 is part of Python's standard library,
no internet or extra install needed.

Usage:
    Place this script in the same folder as your /data CSVs (or adjust
    the DATA_DIR path below), then run:

    python build_database.py
"""

import sqlite3
import csv
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")   # data/ sits one level up from sql/
DB_PATH = os.path.join(SCRIPT_DIR, "..", "solar_data.db")
SCHEMA_PATH = os.path.join(SCRIPT_DIR, "schema.sql")  # schema.sql lives next to this script

# (city name, lat, lon, capacity_kw, raw weather CSV filename)
LOCATIONS = [
    ("Bahawalpur", 29.4, 71.68, 5.0, "bahawalpur_2023.csv"),
    ("Dubai", 25.20, 55.27, 5.0, "dubai_2023.csv"),
    ("Riyadh", 24.71, 46.68, 5.0, "riyadh_2023.csv"),
]


def build_schema(conn):
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())


def insert_locations(conn):
    for city, lat, lon, capacity_kw, _ in LOCATIONS:
        conn.execute(
            "INSERT INTO locations (city, lat, lon, capacity_kw) VALUES (?, ?, ?, ?)",
            (city, lat, lon, capacity_kw),
        )


def get_location_id(conn, city):
    row = conn.execute("SELECT id FROM locations WHERE city = ?", (city,)).fetchone()
    return row[0]


def load_weather_csv(conn, city, filename):
    """Loads the raw weather CSV (date, ghi_kwh_m2_day, temp_c, wind_ms)."""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"  Skipping {filename} — not found in {DATA_DIR}/")
        return 0

    location_id = get_location_id(conn, city)
    count = 0
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            conn.execute(
                """INSERT OR IGNORE INTO daily_readings
                   (location_id, date, ghi_kwh_m2_day, temp_c, wind_ms)
                   VALUES (?, ?, ?, ?, ?)""",
                (location_id, row["date"], row["ghi_kwh_m2_day"], row["temp_c"], row["wind_ms"]),
            )
            count += 1
    return count


def backfill_yield(conn):
    """
    Calculates yield_kwh for every row using the same formula as
    pv_yield_model.py, so the database stays consistent with the rest
    of the project rather than duplicating logic differently.
    """
    rows = conn.execute(
        """SELECT daily_readings.id, daily_readings.ghi_kwh_m2_day,
                  daily_readings.temp_c, locations.capacity_kw
           FROM daily_readings
           JOIN locations ON daily_readings.location_id = locations.id"""
    ).fetchall()

    tilt = 25
    system_efficiency = 0.80
    temp_coeff = -0.004
    tilt_factor = 1.0 + (tilt / 90) * 0.05

    updated = 0
    for row_id, ghi, temp_c, capacity_kw in rows:
        if ghi is None or temp_c is None:
            continue
        temp_derate = min(1.0, 1 + temp_coeff * (temp_c - 25))
        yield_kwh = round(ghi * capacity_kw * system_efficiency * tilt_factor * temp_derate, 2)
        conn.execute("UPDATE daily_readings SET yield_kwh = ? WHERE id = ?", (yield_kwh, row_id))
        updated += 1
    return updated


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)  # rebuild clean each time this script runs

    conn = sqlite3.connect(DB_PATH)
    build_schema(conn)
    insert_locations(conn)

    total_rows = 0
    for city, lat, lon, capacity_kw, filename in LOCATIONS:
        n = load_weather_csv(conn, city, filename)
        print(f"  Loaded {n} rows for {city}")
        total_rows += n

    updated = backfill_yield(conn)
    print(f"  Calculated yield for {updated} rows")

    conn.commit()
    conn.close()
    print(f"\nDatabase built: {DB_PATH} ({total_rows} total readings)")


if __name__ == "__main__":
    main()
