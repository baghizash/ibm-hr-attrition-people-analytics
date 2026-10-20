# DAX Measures — IBM HR Attrition / People Analytics

## Catatan level (PENTING — baca dulu)

Model ini memakai **satu tabel fakta dengan satu grain tunggal**:

| Tabel fakta | Grain (1 baris =) | Isi |
|---|---|---|
| `fact_karyawan` | 1 karyawan | 1.470 baris, satu untuk setiap `karyawan_id` (dari kolom EmployeeNumber data mentah, unik tanpa duplikat) |

Tidak ada baris agregat, tidak ada baris ringkasan departemen, dan tidak ada grain campuran di dalam `fact_karyawan`. Semua agregasi (per departemen, per peran, per kelompok) terjadi di measure dan visual, bukan di data. Karena itu setiap measure di bawah membaca tepat satu grain dan tidak perlu filter penjaga level.

Tiga tabel dimensi, semuanya satu-ke-banyak dengan arah tunggal ke `fact_karyawan`:

| Dimensi | Kunci | Isi |
|---|---|---|
| `dim_departemen` | `departemen_id` (DEP01 sampai DEP03) | 3 departemen: Human Resources, Research & Development, Sales |
| `dim_peran` | `peran_id` (ROL01 sampai ROL09) | 9 peran pekerjaan (JobRole) |
| `dim_pendidikan` | `pendidikan_id` (EDU01 sampai EDU06) | 6 bidang pendidikan (EducationField) |

Surrogate id dibuat deterministik oleh `build_kit.py` (urut abjad label), jadi pemetaan id ke label selalu sama setiap kit dibangun ulang.

Kolom turunan di `fact_karyawan` (dihitung `build_kit.py`, batasnya sama persis dengan `sql/queries.sql`):

| Kolom | Batas kelompok |
|---|---|
| `kelompok_usia` | di bawah 30; 30 sampai 39; 40 sampai 49; 50 ke atas |
| `kelompok_gaji` | gaji bulanan di bawah 3000; 3000 sampai 5999; 6000 sampai 9999; 10000 ke atas (USD) |
| `kelompok_masa_kerja` | masa kerja di perusahaan 0 sampai 2; 3 sampai 5; 6 sampai 10; 11 tahun ke atas |
| `kelompok_jarak` | jarak rumah 1 sampai 4; 5 sampai 9; 10 sampai 14; 15 km ke atas |

Setiap kolom kelompok punya kolom pasangan berakhiran `_urutan` (1, 2, 3, 4) untuk mengurutkan kategori di visual: di Power BI pilih kolom kelompok, lalu Sort by Column memakai kolom urutannya.

Kolom bendera: `attrition_flag` bernilai 1 bila karyawan resign dan 0 bila bertahan; `overtime_flag` bernilai 1 bila karyawan lembur dan 0 bila tidak. Kolom atribut teks di fakta (`job_satisfaction`, `environment_satisfaction`, `work_life_balance`, `gender`, `marital_status`, `business_travel`, `tingkat_pendidikan`) adalah label asli data mentah, dipakai sebagai slicer dan sumbu kategori.

## Verifikasi angka (dihitung dari CSV kit ini)

Angka berikut dihitung ulang dari `fact_karyawan.csv` hasil `build_kit.py`, bukan disalin dari README. Semua cocok dengan temuan proyek:

| Ukuran | Nilai acuan |
|---|---|
| Total karyawan | 1.470 |
| Total resign | 237 |
| Persen attrition keseluruhan | 16,1% |
| Karyawan lembur | 416 (28,3%) |
| Persen attrition lembur | 30,5% (127 dari 416) |
| Persen attrition tidak lembur | 10,4% (110 dari 1.054) |
| Rasio risiko lembur | 2,9 kali yang tidak lembur |
| Rata-rata gaji bulanan | USD 6.503 (median USD 4.919) |
| Rata-rata gaji karyawan resign | USD 4.787 |
| Rata-rata gaji karyawan bertahan | USD 6.833 |
| Rata-rata usia | 36,9 tahun (resign 33,6 tahun) |
| Rata-rata masa kerja di perusahaan | 7,0 tahun (resign 5,1 tahun) |
| Rata-rata total tahun kerja | 11,3 tahun |
| Rata-rata jarak rumah | 9,2 km |

Attrition per segmen kunci (persen resign di dalam segmen):

| Segmen | Karyawan | Resign | Persen attrition |
|---|---|---|---|
| Departemen Sales | 446 | 92 | 20,6% |
| Departemen Human Resources | 63 | 12 | 19,0% |
| Departemen Research & Development | 961 | 133 | 13,8% |
| Peran Sales Representative | 83 | 33 | 39,8% |
| Peran Laboratory Technician | 259 | 62 | 23,9% |
| Peran Human Resources | 52 | 12 | 23,1% |
| Peran Research Director | 80 | 2 | 2,5% |
| Gaji bulanan di bawah 3000 | 395 | 113 | 28,6% |
| Usia di bawah 30 tahun | 326 | 91 | 27,9% |
| Masa kerja 0 sampai 2 tahun | 342 | 102 | 29,8% |
| Work-life balance Bad | 80 | 25 | 31,3% |
| Kepuasan lingkungan Low | 284 | 72 | 25,4% |
| Status Single | 470 | 120 | 25,5% |
| Perjalanan dinas Travel Frequently | 277 | 69 | 24,9% |
| Jarak rumah 15 km ke atas | 355 | 73 | 20,6% |

Visual WAJIB menampilkan angka di atas pada konteks yang sama. Jika berbeda, cek: visual memakai `fact_karyawan` dan filter halaman tidak menyisakan segmen lain tanpa disadari.

## Measures (tabel `fact_karyawan`)

Semua nama measure berupa teks polos. Tanda sama dengan hanya muncul satu kali, sebagai pemisah nama dan rumus DAX standar Power BI.

```dax
Total Karyawan =
COUNTROWS ( fact_karyawan )

Total Attrition =
SUM ( fact_karyawan[attrition_flag] )

Total Bertahan =
[Total Karyawan] - [Total Attrition]

Persen Attrition =
DIVIDE ( [Total Attrition], [Total Karyawan] ) * 100

Total Lembur =
SUM ( fact_karyawan[overtime_flag] )

Persen Lembur =
DIVIDE ( [Total Lembur], [Total Karyawan] ) * 100

Persen Attrition Lembur =
CALCULATE ( [Persen Attrition], fact_karyawan[overtime_flag] = 1 )

Persen Attrition Tidak Lembur =
CALCULATE ( [Persen Attrition], fact_karyawan[overtime_flag] = 0 )

Selisih Attrition Lembur vs Tidak Lembur =
[Persen Attrition Lembur] - [Persen Attrition Tidak Lembur]

Rasio Risiko Lembur =
DIVIDE ( [Persen Attrition Lembur], [Persen Attrition Tidak Lembur] )

Persen Attrition Resign Saja =
CALCULATE ( [Persen Attrition], fact_karyawan[attrition_flag] = 1 )

Rata-rata Gaji Bulanan =
AVERAGE ( fact_karyawan[monthly_income] )

Median Gaji Bulanan =
MEDIAN ( fact_karyawan[monthly_income] )

Rata-rata Gaji Resign =
CALCULATE ( [Rata-rata Gaji Bulanan], fact_karyawan[attrition_flag] = 1 )

Rata-rata Gaji Bertahan =
CALCULATE ( [Rata-rata Gaji Bulanan], fact_karyawan[attrition_flag] = 0 )

Rata-rata Usia =
AVERAGE ( fact_karyawan[age] )

Rata-rata Masa Kerja =
AVERAGE ( fact_karyawan[years_at_company] )

Rata-rata Total Tahun Kerja =
AVERAGE ( fact_karyawan[total_working_years] )

Rata-rata Jarak Rumah =
AVERAGE ( fact_karyawan[distance_from_home] )
```

Catatan: measure `Persen Attrition Resign Saja` selalu bernilai 100 pada konteks apa pun karena konteksnya hanya berisi karyawan resign; measure ini disediakan hanya sebagai alat uji relasi saat membangun halaman, bukan untuk ditampilkan di dashboard. Abaikan atau hapus setelah verifikasi.

## Aturan pakai

1. Satu-satunya tabel fakta adalah `fact_karyawan`. Semua measure membaca tabel ini; jangan membuat measure dari tabel dimensi.
2. Persen attrition selalu `Total Attrition` dibagi `Total Karyawan` pada konteks filter yang sama. Jangan menghitung persen dari rata-rata persen per segmen, hasilnya akan berbeda karena ukuran segmen tidak sama.
3. Perbandingan lembur dan tidak lembur memakai konteks filter lewat `overtime_flag`, bukan dua visual terpisah yang difilter manual, supaya slicer departemen dan peran tetap berlaku ke keduanya.
4. Urutkan visual kelompok (usia, gaji, masa kerja, jarak) memakai kolom `_urutan` pasangannya, bukan urutan abjad label.
5. Uji tiap measure pada satu segmen dulu sebelum membangun halaman penuh. Contoh: filter peran Sales Representative harus memberi Total Karyawan 83, Total Attrition 33, dan Persen Attrition 39,8.
6. Format tampilan: persen 1 desimal dengan koma (contoh 16,1); gaji tanpa desimal dengan pemisah ribuan titik (contoh USD 6.503); rata-rata usia dan masa kerja 1 desimal.
