# Log Pembersihan Data — HR Employee Attrition

Dokumen ini mencatat setiap aturan pembersihan yang menghasilkan file bersih,
jumlah baris yang terdampak per aturan, dan cara mereproduksinya dari data mentah.
File bersih ini adalah basis yang sama dengan yang dipakai analisis SQL, notebook,
chart, dan kit Power BI proyek ini. Kesimpulan utamanya: dataset ini memang sudah
bersih dari sumbernya, jadi tidak ada baris yang dihapus; yang dilakukan script
hanyalah pembacaan yang benar (BOM) dan pemeriksaan yang terdokumentasi.

## File

| | |
|---|---|
| File mentah | `data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv` |
| File bersih | `data/clean/hr_employee_attrition_clean.csv` |
| Script reproduksi | `scripts/clean_data.py` |
| Basis pembanding | Tabel `employees` di `data/hr_attrition.db` (dibuat `scripts/load_to_sqlite.py`) dan `powerbi/fact_karyawan.csv` |

## Ringkasan sebelum dan sesudah

| Ukuran | Mentah | Bersih |
|---|---|---|
| Baris | 1.470 | 1.470 |
| Kolom | 35 | 35 |
| Karyawan resign (`Attrition = Yes`) | 237 | 237 |
| Attrition rate | **16,1%** (237 dari 1.470) | **16,1%** (237 dari 1.470) |
| Missing value | 0 | 0 |
| Baris dihapus | — | 0 |

## Aturan pembersihan

### 1. BOM di awal file dibuang saat membaca
- Masalah: file mentah diawali BOM (byte `EF BB BF`). Bila dibaca sebagai UTF-8
  biasa, BOM itu menempel pada nama kolom pertama.
- Tindakan: file dibaca dengan `encoding="utf-8-sig"`, sehingga kolom pertama
  terbaca bersih sebagai `Age`.
- Baris terdampak: 0. Kolom terdampak: 1 nama kolom (kolom pertama).

### 2. Nama kolom dibersihkan dari spasi di tepi
- Tindakan: `df.columns = df.columns.str.strip()` sebagai pengaman.
- Baris terdampak: 0. Kolom terdampak: 0 (tidak ada nama kolom yang berubah
  setelah BOM dibuang pada aturan 1).

### 3. Pemeriksaan missing value, duplikat, dan kunci
Pemeriksaan berikut dijalankan oleh script dan tidak menghapus atau mengubah baris apa pun:
- Missing value pada 35 kolom: **0 sel**.
- Baris duplikat persis: **0**.
- `EmployeeNumber` duplikat: **0** (`EmployeeNumber` unik pada 1.470 baris,
  rentang 1 sampai 2.068).

### 4. Tiga kolom konstan dipertahankan, bukan dibuang
Kolom berikut bernilai sama pada semua baris. Ketiganya **dipertahankan apa adanya**
demi kesetiaan pada basis analisis (tabel `employees` di SQLite), dan dicatat di sini
agar pembaca tahu kolom ini tidak membawa variasi untuk analisis:
- `EmployeeCount` = 1 pada 1.470 baris.
- `Over18` = `Y` pada 1.470 baris.
- `StandardHours` = 80 pada 1.470 baris.
- Baris terdampak: 0 dihapus, 0 diubah.

### 5. Kolom ordinal sudah berbentuk label, tidak ada decoding
- Pada file mentah ini kolom ordinal sudah berupa label teks, misalnya
  `Education` (`Below College`, `College`, `Bachelor`, `Master`, `Doctor`),
  `JobSatisfaction`, `EnvironmentSatisfaction`, dan `RelationshipSatisfaction`
  (`Low`, `Medium`, `High`, `Very High`), `WorkLifeBalance` (`Bad`, `Good`,
  `Better`, `Best`), `PerformanceRating` (`Excellent`, `Outstanding`), dan
  `JobInvolvement` (`Low`, `Medium`, `High`, `Very High`).
- Tidak ada script proyek yang memetakan kode angka menjadi label, jadi
  **tidak ada aturan decoding** yang diterapkan atau ditambahkan.
- Baris terdampak: 0.

## Kolom turunan

- **Tidak ada kolom turunan yang ditambahkan** pada file bersih ini. Nama, urutan
  kolom, urutan baris, dan setiap nilai sama persis dengan file mentah, dan isinya
  identik dengan tabel `employees` di SQLite.
- Kolom turunan hanya dibuat di hilir untuk Power BI oleh `powerbi/build_kit.py`
  pada `powerbi/fact_karyawan.csv`: `attrition_flag` (1 bila `Attrition = Yes`),
  `overtime_flag`, `kelompok_usia` (di bawah 30, 30-39, 40-49, 50+), `kelompok_gaji`
  (di bawah 3000, 3000-5999, 6000-9999, 10000 ke atas), `kelompok_masa_kerja`
  (0-2, 3-5, 6-10, 11+ tahun), `kelompok_jarak` (1-4, 5-9, 10-14, 15+ km) beserta
  kolom urutannya, serta ID pengganti `departemen_id`, `peran_id`, dan
  `pendidikan_id`. Kolom kolom itu tidak masuk ke file bersih ini.

## Cara reproduksi

```bash
~/workspace/mienv/bin/python scripts/clean_data.py
```

Script membaca file mentah dengan `utf-8-sig`, menjalankan pemeriksaan aturan 3
dan 4, menulis `data/clean/hr_employee_attrition_clean.csv`, dan berhenti dengan
assertion bila jumlah baris bukan 1.470 atau jumlah resign bukan 237.

## Verifikasi (dijalankan 2026-10-24)

- File bersih dibaca ulang secara independen: **1.470 baris x 35 kolom**, missing value 0.
- Attrition dihitung ulang dari file bersih: 237 dari 1.470 = **16,1%**.
- Pemeriksaan silang lembur dari file bersih: resign 30,5% pada karyawan lembur
  (127 dari 416) berbanding 10,4% pada yang tidak lembur, sesuai angka headline proyek.
- Himpunan `EmployeeNumber` file bersih **sama persis** dengan himpunan `karyawan_id`
  pada `powerbi/fact_karyawan.csv` (1.470 ID, tanpa selisih).
- Isi file bersih **identik** dengan file mentah (perbandingan per sel setelah BOM
  dibuang) dan dengan tabel `employees` di `data/hr_attrition.db`.
