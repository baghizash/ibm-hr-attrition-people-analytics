"""
Memuat dataset HR Employee Attrition (IBM, publik) ke SQLite.

Sumber CSV : data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv  (diawali BOM -> dibaca utf-8-sig)
Tujuan DB  : data/hr_attrition.db, tabel "employees"

Cara pakai:
    python scripts/load_to_sqlite.py
"""
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
DB_PATH = BASE_DIR / "data" / "hr_attrition.db"

# Kolom numerik dibuat integer agar konsisten di SQLite
INDEXES = {
    "idx_employees_attrition": ["Attrition"],
    "idx_employees_department": ["Department"],
    "idx_employees_jobrole": ["JobRole"],
    "idx_employees_overtime": ["OverTime"],
    "idx_employees_businesstravel": ["BusinessTravel"],
    "idx_employees_gender": ["Gender"],
    "idx_employees_marital": ["MaritalStatus"],
    "idx_employees_income": ["MonthlyIncome"],
    "idx_employees_age": ["Age"],
    "idx_employees_distance": ["DistanceFromHome"],
    "idx_employees_tenure": ["YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion"],
    "idx_employees_satisfaction": ["JobSatisfaction", "EnvironmentSatisfaction", "WorkLifeBalance"],
}


def main() -> None:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()  # jaga-jaga sisa spasi/BOM

    if DB_PATH.exists():
        DB_PATH.unlink()

    con = sqlite3.connect(DB_PATH)
    df.to_sql("employees", con, index=False)

    cur = con.cursor()
    for name, cols in INDEXES.items():
        cur.execute(
            f"CREATE INDEX {name} ON employees ({', '.join(f'\"{c}\"' for c in cols)})"
        )
    con.commit()

    n = cur.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    con.close()

    print(f"Baris di CSV  : {len(df)}")
    print(f"Baris di DB   : {n}")
    print(f"Tersimpan di  : {DB_PATH}")
    assert n == 1470, f"Jumlah baris tidak sesuai! Diharapkan 1470, dapat {n}"
    print("OK: verifikasi 1470 baris berhasil.")


if __name__ == "__main__":
    main()
