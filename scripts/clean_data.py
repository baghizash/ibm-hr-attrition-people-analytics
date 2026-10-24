"""
Membuat dataset bersih HR Employee Attrition sebagai CSV mandiri.

Sumber : data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv  (1.470 baris x 35 kolom)
Keluaran: data/clean/hr_employee_attrition_clean.csv      (1.470 baris x 35 kolom)

Aturan pembersihan (sama persis dengan scripts/load_to_sqlite.py, yang
menjadi basis analisis/SQL; kit Power BI di powerbi/build_kit.py membaca
file mentah yang sama):
1. File mentah diawali BOM (EF BB BF). File dibaca dengan
   encoding="utf-8-sig" sehingga nama kolom pertama bersih menjadi "Age".
   Tanpa langkah ini nama kolom pertama terbawa BOM.
2. Nama kolom dibersihkan dari spasi di tepi (strip). Tidak ada kolom yang
   berubah nama setelah BOM dibuang: 0 kolom terdampak selain kolom pertama
   pada langkah 1.
3. Pemeriksaan yang dijalankan dan hasilnya nol baris dihapus/diubah:
   tidak ada missing value di 35 kolom (0 sel), tidak ada baris duplikat
   persis (0), EmployeeNumber unik (0 duplikat).
4. Tiga kolom konstan dipertahankan apa adanya demi kesetiaan pada basis
   analisis (tabel "employees" di SQLite): EmployeeCount = 1 pada semua
   1.470 baris, Over18 = "Y" pada semua 1.470 baris, dan
   StandardHours = 80 pada semua 1.470 baris. Kolom kolom ini dicatat
   sebagai konstan di data/clean/README.md, bukan dibuang diam diam.
5. Kolom ordinal pada file mentah ini sudah berbentuk label teks
   (misalnya Education: "Below College"/"College"/"Bachelor"/"Master"/
   "Doctor"; JobSatisfaction, EnvironmentSatisfaction, dan
   RelationshipSatisfaction: "Low"/"Medium"/"High"/"Very High";
   WorkLifeBalance: "Bad"/"Good"/"Better"/"Best"; PerformanceRating:
   "Excellent"/"Outstanding"; JobInvolvement: "Low"/"Medium"/"High"/
   "Very High"). Tidak ada pemetaan kode angka ke label yang dilakukan
   script proyek mana pun, jadi tidak ada aturan decoding yang ditambahkan.

Tidak ada baris yang dihapus dan tidak ada kolom turunan yang ditambahkan
pada file bersih ini: 1.470 baris mentah menjadi 1.470 baris bersih.
Kolom turunan analisis (attrition_flag, overtime_flag, kelompok_usia,
kelompok_gaji, kelompok_masa_kerja, kelompok_jarak, dan ID dimensi) hanya
dibuat di hilir, di powerbi/fact_karyawan.csv oleh powerbi/build_kit.py.
Urutan baris dan urutan kolom dipertahankan persis seperti file mentah.

Cara pakai:
    ~/workspace/mienv/bin/python scripts/clean_data.py
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
OUT_PATH = BASE_DIR / "data" / "clean" / "hr_employee_attrition_clean.csv"

CONSTANT_COLUMNS = ["EmployeeCount", "Over18", "StandardHours"]


def main() -> None:
    df = pd.read_csv(RAW_PATH, encoding="utf-8-sig")
    n_raw, n_cols_raw = df.shape

    df.columns = df.columns.str.strip()

    n_missing = int(df.isna().sum().sum())
    n_duplicate_rows = int(df.duplicated().sum())
    n_duplicate_ids = int(df["EmployeeNumber"].duplicated().sum())
    assert n_missing == 0, f"Ada {n_missing} missing value!"
    assert n_duplicate_rows == 0, f"Ada {n_duplicate_rows} baris duplikat!"
    assert df["EmployeeNumber"].is_unique, "EmployeeNumber tidak unik!"

    for col in CONSTANT_COLUMNS:
        values = df[col].unique().tolist()
        assert len(values) == 1, f"{col} tidak konstan: {values}"
        print(f"Kolom konstan dipertahankan : {col} = {values[0]} ({len(df)} baris)")

    clean = df.copy()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(OUT_PATH, index=False)

    resign = int((clean["Attrition"] == "Yes").sum())
    rate = resign / len(clean) * 100
    print(f"Baris mentah                 : {n_raw} x {n_cols_raw} kolom")
    print(f"Missing value                : {n_missing}")
    print(f"Baris duplikat persis        : {n_duplicate_rows}")
    print(f"EmployeeNumber duplikat      : {n_duplicate_ids}")
    print(f"Baris dihapus                : {n_raw - len(clean)}")
    print(f"Baris bersih                 : {len(clean)} x {clean.shape[1]} kolom")
    print(f"Resign (Attrition = Yes)     : {resign} ({rate:.1f}%)")
    print(f"Tersimpan di                 : {OUT_PATH}")
    assert len(clean) == 1470, f"Diharapkan 1470, dapat {len(clean)}"
    assert resign == 237, f"Diharapkan 237 resign, dapat {resign}"
    print("OK: verifikasi 1.470 baris dan attrition 16,1% berhasil.")


if __name__ == "__main__":
    main()
