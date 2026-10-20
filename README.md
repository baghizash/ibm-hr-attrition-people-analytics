# Analisis HR Employee Attrition (People Analytics)

Analisis end-to-end tingkat *attrition* (karyawan resign) menggunakan SQL dan Python:
data dimuat ke SQLite, setiap pertanyaan bisnis dijawab dengan **query SQL asli** (`sql/queries.sql`),
divisualisasikan dalam 12 chart (`charts/`), dan dinarasikan dalam notebook (`analysis.ipynb`).

## Ringkasan Eksekutif

- Attrition rate keseluruhan: **16,1%** (237 dari 1.470 karyawan).
- Segmen paling rawan resign: **Sales Representative 39,8%** (33 dari 83), karyawan **lembur 30,5%**
  (127 dari 416 — hampir 3x lipat yang tidak lembur), **masa kerja 0-2 tahun 29,8%** (102 dari 342),
  **gaji < 3.000 USD 28,6%** (113 dari 395), **umur di bawah 30 tahun 27,9%** (91 dari 326),
  **single 25,5%** (120 dari 470), **sering perjalanan dinas 24,9%** (69 dari 277),
  **work-life balance buruk 31,3%** (25 dari 80), dan **jarak rumah 15+ km 20,6%** (73 dari 355).
- Pola umum: karyawan muda, baru masuk, bergaji rendah, dengan beban kerja berat (lembur/dinas jauh)
  adalah kelompok yang paling sering keluar. Lihat `analysis.ipynb` bagian "Temuan Kunci" untuk tabel lengkap.

## Data

- **Sumber:** IBM HR Analytics Employee Attrition & Performance — dataset publik untuk latihan people analytics.
- **Ukuran:** 1.470 baris karyawan × 35 kolom (tidak ada missing value pada kolom analisis).
- **File mentah:** `data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv` (diawali BOM, dibaca dengan `encoding='utf-8-sig'`).
- **Database:** `data/hr_attrition.db` (SQLite, dibuat ulang oleh script; tidak di-commit ke git).
- **Catatan:** kolom kepuasan (`JobSatisfaction`, `EnvironmentSatisfaction`) tersimpan sebagai label
  *Low / Medium / High / Very High*, dan `WorkLifeBalance` sebagai *Bad / Good / Better / Best*.

## Definisi Metrik

- **Resign:** karyawan dengan kolom `Attrition` bernilai `Yes`.
- **Attrition rate** = jumlah resign / total karyawan pada segmen tersebut.
- Rate pada tiap segmen dihitung langsung dari data via SQL — tidak ada angka yang dikarang.

## Struktur Repo

```
hr-attrition/
├── analysis.ipynb                  # notebook naratif (Bahasa Indonesia): SQL + chart + insight
├── README.md
├── requirements.txt
├── .gitignore
├── scripts/
│   ├── load_to_sqlite.py           # load CSV -> data/hr_attrition.db (+ index), verifikasi 1470 baris
│   └── make_charts.py              # membuat ulang 12 chart dari database
├── sql/
│   └── queries.sql                 # semua query analisis dengan komentar Bahasa Indonesia
├── charts/                         # 12 chart PNG (palet konsisten)
│   ├── 01_attrition_overall.png
│   ├── 02_attrition_department.png
│   ├── 03_attrition_jobrole.png
│   ├── 04_attrition_overtime.png
│   ├── 05_attrition_income_band.png
│   ├── 06_attrition_age_group.png
│   ├── 07_attrition_distance.png
│   ├── 08_attrition_job_satisfaction.png
│   ├── 09_attrition_env_satisfaction.png
│   ├── 10_attrition_worklife_balance.png
│   ├── 11_attrition_tenure.png
│   └── 12_attrition_demografi_travel.png
└── data/
    ├── raw/WA_Fn-UseC_-HR-Employee-Attrition.csv
    └── hr_attrition.db             # dibuat oleh script, diabaikan git
```

## Yang Dikerjakan

1. Pemuatan data CSV ke SQLite dengan index pada kolom yang sering dipakai di `WHERE`/`GROUP BY`,
   plus verifikasi jumlah baris = 1.470.
2. Analisis 10 pertanyaan bisnis (attrition keseluruhan; per departemen & role; lembur; band gaji;
   kelompok umur; jarak rumah; tiga ukuran kepuasan; tiga ukuran masa kerja; gender & status perkawinan;
   perjalanan dinas) — semuanya dengan query SQL yang tersimpan di `sql/queries.sql`.
3. Visualisasi 12 chart PNG dengan palet warna dan gaya yang konsisten.
4. Notebook naratif Bahasa Indonesia: tiap section berisi penjelasan singkat, query SQL yang dijalankan
   langsung ke database (hasil tampil sebagai tabel), chart, dan insight 1-2 kalimat.
   Notebook lolos uji *restart kernel + run all* tanpa error.
5. Rekomendasi retensi berbasis temuan (di notebook dan di bawah).

## Cara Reproduce

```bash
pip install -r requirements.txt
python scripts/load_to_sqlite.py   # membuat data/hr_attrition.db, verifikasi 1470 baris
# buka analysis.ipynb di Jupyter lalu jalankan semua sel,
# atau buat ulang chart: python scripts/make_charts.py
```

## Rekomendasi Retensi

1. **Program onboarding 2 tahun pertama yang terstruktur.** Masa kerja 0-2 tahun resign 29,8% —
   tetapkan buddy/mentor, tinjau beban kerja 90 hari pertama, dan jadwalkan *check-in* karier berkala.
2. **Kelola lembur secara ketat, terutama di Sales dan Lab.** Lembur menaikkan resign hingga 30,5%.
   Batasi jam lembur per bulan, beri kompensasi cuti pengganti, dan pantau tim dengan lembur kronis.
3. **Perbaiki kompensasi dan jenjang karier role berisiko.** Sales Representative (39,8%) dan
   Laboratory Technician (23,9%) bergaji relatif rendah — tinjau struktur gaji, bonus kinerja,
   dan jalur promosi yang jelas (karyawan 6+ tahun tanpa promosi kembali berisiko, 16,3%).
4. **Fleksibilitas untuk karyawan yang jauh dan sering dinas.** Jarak 15+ km (20,6%) dan sering
   dinas (24,9%) menambah beban harian — pertimbangkan hybrid/WFH parsial, tunjangan transportasi,
   dan rotasi jadwal dinas.
5. **Intervensi dini berbasis survei kepuasan.** Lingkungan *Low* (25,4%) dan work-life balance
   *Bad* (31,3%) adalah sinyal yang terdeteksi sebelum resign — tindak lanjuti hasil survei per tim
   dengan rencana perbaikan konkret.

## Dashboard Power BI

Kit Power BI tersedia di folder `powerbi/`: satu tabel fakta `fact_karyawan.csv` (grain 1 baris per karyawan, 1.470 baris) plus tiga dimensi (`dim_departemen.csv`, `dim_peran.csv`, `dim_pendidikan.csv`), dibangun dari data mentah oleh `powerbi/build_kit.py`. Dokumentasinya: `measures_dax.md` (measures DAX beserta angka verifikasinya), `dashboard_layout.md` (rancangan 4 halaman), dan `build_guide.md` (panduan membangun dashboard langkah demi langkah).

Ringkasan 4 halaman dashboard:

1. **Ringkasan Eksekutif** — KPI utama (1.470 karyawan, 237 resign, attrition 16,1%), donut resign vs bertahan, attrition per departemen, dan lembur vs tidak lembur (30,5% vs 10,4%).
2. **Segmen Risiko** — attrition per peran (tertinggi Sales Representative 39,8%), per kelompok gaji, kelompok usia, dan kelompok masa kerja.
3. **Kepuasan dan Kondisi Kerja** — work-life balance, kepuasan lingkungan dan kepuasan kerja, jarak rumah, perjalanan dinas, dan status perkawinan.
4. **Profil dan Metodologi** — tabel matriks per peran, perbandingan gaji karyawan resign vs bertahan, metodologi, dan rekomendasi ringkas.

File `.pbix` dibangun secara lokal di Power BI Desktop mengikuti `powerbi/build_guide.md` (nama berkas yang disarankan: `HR-Attrition-Analytics.pbix`) dan tidak disimpan di repo ini. Pratinjau tata letak halaman 1 tersedia di `powerbi/dashboard_preview_halaman1.png`; screenshot dashboard hasil build akan ditambahkan setelah `.pbix` selesai dibangun.
