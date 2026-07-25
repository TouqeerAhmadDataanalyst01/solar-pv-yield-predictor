-- CS50SQL Final Project — Solar PV Yield Database
-- Schema: locations + daily_readings, related by foreign key

CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL UNIQUE,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    capacity_kw REAL NOT NULL DEFAULT 5.0
);

CREATE TABLE daily_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    ghi_kwh_m2_day REAL,
    temp_c REAL,
    wind_ms REAL,
    yield_kwh REAL,
    FOREIGN KEY (location_id) REFERENCES locations(id),
    UNIQUE(location_id, date)
);

-- Index to make date-range and per-city lookups fast
CREATE INDEX idx_readings_location_date ON daily_readings(location_id, date);
