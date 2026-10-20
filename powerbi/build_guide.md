# Panduan Membangun Dashboard — Power BI Desktop

## 1. Persiapan (5 menit)
1. Buka Power BI Desktop → Get Data → Text/CSV → impor keempat CSV di folder ini:
   `fact_karyawan.csv`, `dim_departemen.csv`, `dim_peran.csv`, `dim_pendidikan.csv`.
   (Kit ini bisa dibangun ulang kapan saja dari data mentah dengan menjalankan
   `~/workspace/mienv/bin/python powerbi/build_kit.py` dari folder proyek.)
2. Pastikan tipe data: `karyawan_id`, `attrition_flag`, `overtime_flag`, `monthly_income`,
   `age`, `years_at_company`, `total_working_years`, `distance_from_home`, dan keempat kolom
   berakhiran `_urutan` = Whole Number; kolom kunci dimensi (`departemen_id`, `peran_id`,
   `pendidikan_id`) dan semua label = Text.
3. Buka Model view. Buat relasi (semuanya satu-ke-banyak, single direction):
   - `dim_departemen[departemen_id]` → `fact_karyawan[departemen_id]`
   - `dim_peran[peran_id]` → `fact_karyawan[peran_id]`
   - `dim_pendidikan[pendidikan_id]` → `fact_karyawan[pendidikan_id]`
4. Atur Sort by Column untuk kategori berkelompok di `fact_karyawan`:
   `kelompok_usia` urut dengan `kelompok_usia_urutan`; `kelompok_gaji` dengan
   `kelompok_gaji_urutan`; `kelompok_masa_kerja` dengan `kelompok_masa_kerja_urutan`;
   `kelompok_jarak` dengan `kelompok_jarak_urutan`.
5. Sembunyikan kolom kunci id dan kolom `_urutan` dari Report view (klik kanan → Hide in report view) supaya panel field tetap bersih.

## 2. Measures (10 menit)
1. Salin seluruh blok DAX dari `measures_dax.md` ke dalam model (buat satu tabel measure khusus, misalnya `_Measures`).
2. Baca bagian "Catatan level" di `measures_dax.md` SEBELUM membuat visual: model ini satu fakta dengan grain 1 baris per karyawan, jadi tidak ada tabel fakta kedua yang boleh dicampur.
3. Uji cepat: buat card dengan `Total Karyawan`, `Total Attrition`, dan `Persen Attrition` tanpa filter apa pun → harus **1.470**, **237**, dan **16,1**. Tambahkan slicer Peran = Sales Representative → harus berubah menjadi **83**, **33**, dan **39,8**. Jika beda, cek relasi `dim_peran`.

## 3. Bangun 4 halaman (30–45 menit)
Ikuti `dashboard_layout.md` halaman per halaman:
- Halaman 1: ringkasan eksekutif (KPI, donut resign vs bertahan, attrition per departemen, lembur vs tidak lembur).
- Halaman 2: segmen risiko (peran, kelompok gaji, kelompok usia, kelompok masa kerja).
- Halaman 3: kepuasan dan kondisi kerja (work-life balance, kepuasan lingkungan, kepuasan kerja, jarak, perjalanan dinas, status perkawinan).
- Halaman 4: tabel matriks per peran, perbandingan gaji resign vs bertahan, metodologi, dan rekomendasi ringkas.
- Terapkan palet di `dashboard_layout.md` sejak halaman pertama: marine `#0E4D7A`, merah `#E5322D` hanya untuk risiko dan resign, latar `#F7F4EE`.

## 4. Verifikasi akhir (10 menit)
- [ ] Halaman 1 KPI: 1.470 karyawan; 237 resign; 16,1%; lembur 28,3%.
- [ ] Halaman 1: Sales 20,6%; Human Resources 19,0%; Research & Development 13,8%.
- [ ] Halaman 1: lembur 30,5% vs tidak lembur 10,4%; selisih 20,1 poin persen; rasio 2,9 kali.
- [ ] Halaman 2: Sales Representative 39,8%; gaji di bawah 3000 sebesar 28,6%; usia di bawah 30 tahun 27,9%; masa kerja 0 sampai 2 tahun 29,8%.
- [ ] Halaman 3: work-life balance Bad 31,3%; kepuasan lingkungan Low 25,4%; jarak 15 km ke atas 20,6%.
- [ ] Halaman 4: total tabel matriks 1.470 / 237 / 16,1%; rata-rata gaji resign USD 4.787 vs bertahan USD 6.833.
- [ ] Semua visual kelompok (usia, gaji, masa kerja, jarak) tampil dalam urutan kelompok yang benar, bukan urutan abjad.
- [ ] Simpan sebagai `HR-Attrition-Analytics.pbix` (file .pbix tidak di-push ke GitHub — GitHub tidak bisa me-render-nya; simpan screenshot dashboard sebagai gantinya bila perlu).

## Troubleshooting
- **Urutan kelompok kacau di sumbu (misalnya 11+ muncul sebelum 3 sampai 5)**: kolom kelompok belum diatur Sort by Column ke kolom `_urutan` pasangannya. Ulangi langkah Persiapan nomor 4.
- **Persen attrition tidak cocok dengan README**: pastikan visual memakai measure `Persen Attrition` (Total Attrition dibagi Total Karyawan pada konteks yang sama), bukan rata-rata kolom persen per segmen dan bukan rata-rata `attrition_flag` dari tabel dimensi.
- **Slicer Peran mengosongkan semua visual**: relasi `dim_peran[peran_id]` ke `fact_karyawan[peran_id]` belum dibuat atau arahnya terbalik; relasi harus satu-ke-banyak dari dimensi ke fakta, single direction.
- **Gaji tampil dengan desimal atau pemisah koma**: atur format `monthly_income` dan measure gaji ke Whole Number dengan pemisah ribuan, lalu tulis satuan USD pada judul visual.
- **Angka berubah setelah kit dibangun ulang**: jalankan lagi `build_kit.py`, muat ulang keempat CSV (Refresh), dan cek kartu uji cepat di langkah Measures nomor 3.
