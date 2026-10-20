# Dashboard Layout — IBM HR Attrition / People Analytics (4 halaman, 16:9)

Palet (sama dengan palet 12 chart proyek ini): marine blue `#0E4D7A` (primer), marine gelap `#0B2A44` (teks dan judul), bright red `#E5322D` (sorotan risiko tinggi dan attrition), butter yellow `#F4C95D` (aksen sekunder), abu netral `#A8B6BE`, latar krem `#F7F4EE`.
Font: Segoe UI. Satu ide per halaman, judul rata kiri, angka kunci besar. Semua visual membaca satu-satunya tabel fakta `fact_karyawan` plus dimensinya.

## Halaman 1 — Ringkasan Eksekutif

- **KPI cards (5)**: Total Karyawan **1.470**; Total Attrition **237**; Persen Attrition **16,1%**; Persen Lembur **28,3%** (416 karyawan); Rata-rata Gaji Bulanan **USD 6.503**.
- **Donut chart**: komposisi resign vs bertahan (measure Total Attrition dan Total Bertahan; merah untuk resign, marine untuk bertahan). Angka tengah: 16,1%.
- **Bar chart**: Persen Attrition per departemen dari `dim_departemen[departemen]`. Acuan: Sales 20,6%, Human Resources 19,0%, Research & Development 13,8%. Bar tertinggi berwarna merah.
- **Clustered bar**: Persen Attrition Lembur 30,5% vs Persen Attrition Tidak Lembur 10,4%, dengan kartu kecil Selisih Attrition Lembur vs Tidak Lembur **20,1 poin persen** dan Rasio Risiko Lembur **2,9 kali**.
- **Slicers**: Departemen, Peran.
- Catatan kaki: "Sumber: IBM HR Analytics Employee Attrition & Performance, 1.470 karyawan."

## Halaman 2 — Segmen Risiko: Peran, Gaji, Usia, Masa Kerja

- **Bar chart horizontal**: Persen Attrition per peran dari `dim_peran[peran]`, urut menurun. Acuan teratas: Sales Representative 39,8%, Laboratory Technician 23,9%, Human Resources 23,1%; terbawah Research Director 2,5%. Peran 20% ke atas berwarna merah.
- **Bar chart**: Persen Attrition per `kelompok_gaji` (urut memakai `kelompok_gaji_urutan`). Acuan: di bawah 3000 sebesar 28,6%; 3000 sampai 5999 sebesar 12,7%; 6000 sampai 9999 sebesar 12,0%; 10000 ke atas sebesar 8,9%.
- **Bar chart**: Persen Attrition per `kelompok_usia` (urut memakai `kelompok_usia_urutan`). Acuan: di bawah 30 tahun 27,9%; 30 sampai 39 sebesar 14,3%; 40 sampai 49 sebesar 9,7%; 50 ke atas sebesar 13,3%.
- **Bar chart**: Persen Attrition per `kelompok_masa_kerja` (urut memakai `kelompok_masa_kerja_urutan`). Acuan: 0 sampai 2 tahun 29,8%; 3 sampai 5 sebesar 13,8%; 6 sampai 10 sebesar 12,3%; 11 tahun ke atas sebesar 8,1%.
- **Slicers**: Departemen, Lembur (dari `overtime_flag`).
- Pesan halaman: risiko terkonsentrasi pada karyawan baru, muda, dan bergaji rendah.

## Halaman 3 — Kepuasan dan Kondisi Kerja

- **Bar chart**: Persen Attrition per `work_life_balance`. Acuan: Bad 31,3%, Best 17,6%, Good 16,9%, Better 14,2%.
- **Bar chart**: Persen Attrition per `environment_satisfaction`. Acuan: Low 25,4%, Medium 15,0%, High 13,7%, Very High 13,5%.
- **Bar chart**: Persen Attrition per `job_satisfaction`. Acuan: Low 22,8%, High 16,5%, Medium 16,4%, Very High 11,3%.
- **Bar chart**: Persen Attrition per `kelompok_jarak` (urut memakai `kelompok_jarak_urutan`). Acuan: 1 sampai 4 km sebesar 13,6%; 5 sampai 9 sebesar 15,0%; 10 sampai 14 sebesar 17,7%; 15 km ke atas sebesar 20,6%.
- **Dua bar kecil berdampingan**: Persen Attrition per `business_travel` (Travel Frequently 24,9%; Travel Rarely 15,0%; Non-Travel 8,0%) dan per `marital_status` (Single 25,5%; Married 12,5%; Divorced 10,1%).
- **Slicers**: Departemen, Peran, Bidang Pendidikan dari `dim_pendidikan[bidang_pendidikan]`.
- Pesan halaman: kepuasan lingkungan rendah dan work-life balance buruk adalah sinyal dini yang terlihat sebelum resign.

## Halaman 4 — Profil, Perbandingan Gaji, dan Metodologi

- **Tabel matriks**: baris `dim_peran[peran]`, kolom Total Karyawan, Total Attrition, Persen Attrition, Rata-rata Gaji Bulanan. Urut Persen Attrition menurun; baris total harus 1.470 karyawan, 237 resign, 16,1%.
- **KPI cards perbandingan**: Rata-rata Gaji Resign **USD 4.787** vs Rata-rata Gaji Bertahan **USD 6.833**; Rata-rata Usia keseluruhan **36,9 tahun**; Rata-rata Masa Kerja keseluruhan **7,0 tahun**.
- **Bar chart**: Persen Attrition per `dim_pendidikan[bidang_pendidikan]`. Acuan: Human Resources 25,9%, Technical Degree 24,2%, Marketing 22,0%, Life Sciences 14,7%, Medical 13,6%, Other 13,4%.
- **Tabel metodologi** (ketik manual): sumber data IBM HR Analytics (dataset publik untuk latihan people analytics); grain fakta 1 baris per karyawan; definisi resign adalah Attrition Yes; kelompok turunan mengikuti batas `sql/queries.sql`; keterbatasan: data satu potret waktu tanpa tanggal keluar, jadi dashboard ini membaca pola segmen, bukan tren waktu.
- **Ringkasan rekomendasi** (teks singkat): onboarding terstruktur 2 tahun pertama; kelola lembur terutama di Sales dan laboratorium; tinjau kompensasi peran Sales Representative dan Laboratory Technician.
- **Tombol navigasi** kembali ke Halaman 1.

## Aturan konsisten

- Judul halaman: 20pt bold, rata kiri, warna marine gelap `#0B2A44`.
- Angka KPI: 28pt bold marine `#0E4D7A`; angka risiko dan attrition memakai merah `#E5322D` hanya untuk nilai tertinggi atau nilai resign.
- Persen selalu 1 desimal dengan koma (contoh 16,1); gaji format USD tanpa desimal dengan pemisah ribuan titik (contoh USD 6.503).
- Kolom kelompok selalu diurutkan dengan kolom `_urutan` pasangannya (Sort by Column), tidak pernah urutan abjad.
- Tidak ada visual yang menghitung persen dari rata-rata persen segmen; semua persen berasal dari measure pada konteks filternya.
- Slicer yang sama memakai nama dan urutan yang sama di semua halaman: Departemen, lalu Peran, lalu filter khusus halaman.
