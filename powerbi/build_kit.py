"""
Membangun kit Power BI untuk proyek IBM HR Attrition / People Analytics.

Sumber : data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv (1.470 karyawan)
Keluaran (di folder ini):
  fact_karyawan.csv   -- 1 baris per karyawan (grain tunggal)
  dim_departemen.csv  -- 1 baris per Department
  dim_peran.csv       -- 1 baris per JobRole
  dim_pendidikan.csv  -- 1 baris per EducationField

Tidak ada agregat yang diketik tangan: semua file diturunkan dari CSV mentah
oleh script ini. Kelompok turunan (usia, gaji, masa kerja, jarak) memakai
batas yang sama persis dengan sql/queries.sql proyek ini.

Cara pakai: ~/workspace/mienv/bin/python powerbi/build_kit.py
"""
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
OUT = Path(__file__).resolve().parent


def kelompok_usia(usia):
    if usia < 30:
        return "< 30", 1
    if usia < 40:
        return "30-39", 2
    if usia < 50:
        return "40-49", 3
    return "50+", 4


def kelompok_gaji(gaji):
    if gaji < 3000:
        return "< 3000", 1
    if gaji < 6000:
        return "3000-5999", 2
    if gaji < 10000:
        return "6000-9999", 3
    return ">= 10000", 4


def kelompok_masa_kerja(tahun):
    if tahun < 3:
        return "0-2", 1
    if tahun < 6:
        return "3-5", 2
    if tahun < 11:
        return "6-10", 3
    return "11+", 4


def kelompok_jarak(km):
    if km < 5:
        return "1-4", 1
    if km < 10:
        return "5-9", 2
    if km < 15:
        return "10-14", 3
    return "15+", 4


def buat_dim(df, kolom, prefix, nama_id, nama_label):
    """Dimensi dengan surrogate id deterministik (urut abjad label)."""
    label = sorted(df[kolom].dropna().unique().tolist())
    dim = pd.DataFrame({
        nama_id: [f"{prefix}{i:02d}" for i in range(1, len(label) + 1)],
        nama_label: label,
    })
    peta = dict(zip(dim[nama_label], dim[nama_id]))
    return dim, peta


def main():
    df = pd.read_csv(RAW, encoding="utf-8-sig")
    assert len(df) == 1470, f"jumlah baris tidak 1470: {len(df)}"
    assert df["EmployeeNumber"].is_unique, "EmployeeNumber tidak unik"

    dim_departemen, peta_dep = buat_dim(df, "Department", "DEP", "departemen_id", "departemen")
    dim_peran, peta_peran = buat_dim(df, "JobRole", "ROL", "peran_id", "peran")
    dim_pendidikan, peta_pen = buat_dim(df, "EducationField", "EDU", "pendidikan_id", "bidang_pendidikan")

    fact = pd.DataFrame()
    fact["karyawan_id"] = df["EmployeeNumber"].astype(int)
    fact["departemen_id"] = df["Department"].map(peta_dep)
    fact["peran_id"] = df["JobRole"].map(peta_peran)
    fact["pendidikan_id"] = df["EducationField"].map(peta_pen)
    fact["attrition_flag"] = (df["Attrition"] == "Yes").astype(int)
    fact["overtime_flag"] = (df["OverTime"] == "Yes").astype(int)
    fact["monthly_income"] = df["MonthlyIncome"].astype(int)
    fact["age"] = df["Age"].astype(int)
    fact["years_at_company"] = df["YearsAtCompany"].astype(int)
    fact["total_working_years"] = df["TotalWorkingYears"].astype(int)
    fact["distance_from_home"] = df["DistanceFromHome"].astype(int)
    fact["job_satisfaction"] = df["JobSatisfaction"]
    fact["environment_satisfaction"] = df["EnvironmentSatisfaction"]
    fact["work_life_balance"] = df["WorkLifeBalance"]
    fact["gender"] = df["Gender"]
    fact["marital_status"] = df["MaritalStatus"]
    fact["business_travel"] = df["BusinessTravel"]
    fact["tingkat_pendidikan"] = df["Education"]

    usia = df["Age"].map(kelompok_usia)
    fact["kelompok_usia"] = [u[0] for u in usia]
    fact["kelompok_usia_urutan"] = [u[1] for u in usia]
    gaji = df["MonthlyIncome"].map(kelompok_gaji)
    fact["kelompok_gaji"] = [g[0] for g in gaji]
    fact["kelompok_gaji_urutan"] = [g[1] for g in gaji]
    masa = df["YearsAtCompany"].map(kelompok_masa_kerja)
    fact["kelompok_masa_kerja"] = [m[0] for m in masa]
    fact["kelompok_masa_kerja_urutan"] = [m[1] for m in masa]
    jarak = df["DistanceFromHome"].map(kelompok_jarak)
    fact["kelompok_jarak"] = [j[0] for j in jarak]
    fact["kelompok_jarak_urutan"] = [j[1] for j in jarak]

    fact = fact.sort_values("karyawan_id").reset_index(drop=True)
    assert fact[["departemen_id", "peran_id", "pendidikan_id"]].notna().all().all()

    fact.to_csv(OUT / "fact_karyawan.csv", index=False)
    dim_departemen.to_csv(OUT / "dim_departemen.csv", index=False)
    dim_peran.to_csv(OUT / "dim_peran.csv", index=False)
    dim_pendidikan.to_csv(OUT / "dim_pendidikan.csv", index=False)

    print(f"fact_karyawan : {len(fact)} baris")
    print(f"dim_departemen: {len(dim_departemen)} baris")
    print(f"dim_peran     : {len(dim_peran)} baris")
    print(f"dim_pendidikan: {len(dim_pendidikan)} baris")
    print(f"total resign  : {fact['attrition_flag'].sum()} "
          f"({fact['attrition_flag'].mean() * 100:.1f}%)")


if __name__ == "__main__":
    main()
