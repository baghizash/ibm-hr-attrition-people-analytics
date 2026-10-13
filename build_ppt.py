#!/usr/bin/env python3
"""Build Portofolio-Analisis-HR-Attrition.pptx (16:9, 10 slides, ID, no hyphens).
Style mirrors build_ppt.py from the Olist project."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

NAVY = RGBColor(0x1E, 0x3A, 0x8A)
TEAL = RGBColor(0x0D, 0x94, 0x88)
DARK = RGBColor(0x1F, 0x29, 0x37)
GRAY = RGBColor(0x6B, 0x72, 0x80)
LIGHTBLUE = RGBColor(0x93, 0xC5, 0xFD)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CHARTS = "/home/hatch/workspace/hr-attrition/charts"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


def solid_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def textbox(slide, left, top, width, height):
    tx = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tx.text_frame
    tf.word_wrap = True
    return tf


def add_par(tf, text, size, color, bold=False, italic=False, first=False, align=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_after = Pt(8)
    if align is not None:
        p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return p


def add_bullet(tf, text, size=17, first=False):
    p = add_par(tf, text, size, DARK, first=first)
    pPr = p._p.get_or_add_pPr()
    pPr.append(pPr.makeelement(qn("a:buChar"), {"char": "\u2022"}))
    pPr.set("marL", "171450")
    pPr.set("indent", "-171450")
    p.space_after = Pt(10)
    p.space_before = Pt(2)
    return p


def content_title(slide, text):
    tf = textbox(slide, 0.7, 0.3, 11.9, 0.9)
    add_par(tf, text, 30, NAVY, bold=True, first=True)
    bar = slide.shapes.add_shape(1, Inches(0.7), Inches(1.15), Inches(1.5), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL
    bar.line.fill.background()


def content_slide(title, bullets, chart=None, caption=None, full_width=False):
    s = prs.slides.add_slide(blank)
    solid_bg(s, WHITE)
    content_title(s, title)
    bw = 11.9 if full_width else 5.6
    tf = textbox(s, 0.7, 1.5, bw, 5.2)
    for i, b in enumerate(bullets):
        add_bullet(tf, b, first=(i == 0))
    if chart:
        s.shapes.add_picture(f"{CHARTS}/{chart}.png", Inches(6.8), Inches(1.5),
                             width=Inches(5.8), height=Inches(3.48))
        ctf = textbox(s, 6.8, 5.15, 5.8, 0.5)
        add_par(ctf, caption, 12, GRAY, italic=True, first=True, align=PP_ALIGN.CENTER)
    return s


# ---------- Slide 1: Judul ----------
s = prs.slides.add_slide(blank)
solid_bg(s, NAVY)
tf = textbox(s, 1.0, 1.6, 11.3, 2.2)
add_par(tf, "Analisis HR Attrition dengan SQL dan Python", 40, WHITE, bold=True, first=True)
tf = textbox(s, 1.0, 3.8, 11.3, 1.2)
add_par(tf, "Studi Kasus: IBM HR Analytics Employee Attrition Dataset", 20, WHITE, first=True)
tf = textbox(s, 1.0, 5.6, 11.3, 1.0)
add_par(tf, "BAGHIZ ASSHIDDIQIE ARASYA", 24, LIGHTBLUE, bold=True, first=True)
tf = textbox(s, 1.0, 6.3, 11.3, 0.8)
add_par(tf, "Data Analyst Portfolio Project", 14, GRAY, first=True)

# ---------- Slide 2: Latar Belakang ----------
content_slide("Latar Belakang", [
    "Dataset IBM HR Analytics: 1.470 karyawan dengan 35 kolom data demografi, pekerjaan, kompensasi, dan kepuasan",
    "Pertanyaan utama: kenapa karyawan resign dan siapa yang paling berisiko pergi",
    "Attrition rate keseluruhan 16,1 persen atau 237 karyawan, angka yang cukup tinggi untuk diabaikan",
    "Tujuan analisis: menemukan faktor pendorong resign lalu menyusun rekomendasi retensi yang konkret",
], full_width=True)

# ---------- Slide 3: Data dan Metodologi ----------
content_slide("Data dan Metodologi", [
    "Data dimuat ke SQLite lalu dianalisis dengan query SQL asli: agregasi, grouping, dan perbandingan antar segmen",
    "Pandas dipakai untuk eksplorasi lanjutan dan pembuatan 12 chart visual",
    "Attrition didefinisikan sebagai kolom Attrition bernilai Yes; rate dihitung sebagai Yes dibagi total karyawan",
    "Segmen yang dianalisis: departemen, job role, lembur, band gaji, kelompok umur, jarak rumah, kepuasan, masa kerja, demografi, dan frekuensi dinas",
], full_width=True)

# ---------- Slide 4: Temuan 1, role berisiko ----------
content_slide("Temuan 1: Role Paling Berisiko Resign", [
    "Sales Representative mencatat attrition 39,8 persen, hampir 2,5 kali rata rata perusahaan",
    "Laboratory Technician 23,9 persen dan staf Human Resources 23,1 persen menyusul di posisi berikutnya",
    "Departemen Sales tertinggi 20,6 persen, lalu Human Resources 19,0 persen, Research and Development 13,8 persen",
    "Sebaliknya Research Director hanya 2,5 persen dan Manager 4,9 persen, sangat stabil",
], chart="03_attrition_jobrole", caption="Attrition rate per job role")

# ---------- Slide 5: Temuan 2, lembur ----------
content_slide("Temuan 2: Lembur Melipatgandakan Risiko", [
    "Karyawan yang lembur resign 30,5 persen, dibanding yang tidak lembur hanya 10,4 persen",
    "Artinya karyawan lembur berisiko hampir 3 kali lipat untuk pergi",
    "Dari 416 karyawan lembur, 127 di antaranya resign, porsi yang sangat besar",
    "Ini sinyal kuat burnout, terutama di tim Sales dan laboratorium yang lemburnya tinggi",
], chart="04_attrition_overtime", caption="Attrition rate: lembur vs tidak lembur")

# ---------- Slide 6: Temuan 3, gaji umur masa kerja ----------
content_slide("Temuan 3: Gaji Rendah, Muda, dan Baru", [
    "Gaji di bawah 3.000 resign 28,6 persen, jauh di atas band gaji lain yang berkisar 9 sampai 13 persen",
    "Karyawan di bawah 30 tahun resign 27,9 persen, lalu turun bertahap sampai 9,7 persen di usia 40an",
    "Masa kerja 0 sampai 2 tahun resign 29,8 persen, lalu turun ke 8,1 persen setelah 11 tahun",
    "Pola jelas: karyawan muda bergaji rendah di dua tahun pertama adalah kelompok paling rentan",
], chart="05_attrition_income_band", caption="Attrition rate per band gaji bulanan")

# ---------- Slide 7: Temuan 4, kepuasan ----------
content_slide("Temuan 4: Kepuasan Rendah, Resign Tinggi", [
    "Work life balance buruk mencatat attrition 31,3 persen, faktor tunggal tertinggi dalam analisis kepuasan",
    "Kepuasan lingkungan rendah 25,4 persen dibanding sangat tinggi 13,5 persen",
    "Kepuasan kerja rendah 22,8 persen dibanding sangat tinggi 11,3 persen",
    "Survei kepuasan rutin bisa menjadi sistem peringatan dini sebelum karyawan benar benar pergi",
], chart="10_attrition_worklife_balance", caption="Attrition rate per tingkat work life balance")

# ---------- Slide 8: Temuan 5, jarak dinas status ----------
content_slide("Temuan 5: Jarak, Dinas, dan Status", [
    "Jarak rumah 15 km atau lebih resign 20,6 persen, naik bertahap dari 13,6 persen untuk jarak dekat",
    "Karyawan yang sering dinas resign 24,9 persen, dibanding tidak pernah dinas hanya 8,0 persen",
    "Status single resign 25,5 persen, dua kali lipat dibanding menikah 12,5 persen",
    "Stagnasi juga berbahaya: 6 tahun atau lebih tanpa promosi resign 16,3 persen, naik lagi setelah sempat turun",
], chart="12_attrition_demografi_travel", caption="Attrition: demografi dan frekuensi dinas")

# ---------- Slide 9: Rekomendasi ----------
content_slide("Rekomendasi Retensi", [
    "Bangun program onboarding 2 tahun pertama yang terstruktur: buddy, mentor, dan check in karier berkala",
    "Kelola lembur dengan ketat plus cuti pengganti, prioritaskan tim Sales dan laboratorium",
    "Tinjau ulang gaji, bonus, dan jalur promosi untuk Sales Representative dan Laboratory Technician",
    "Tawarkan fleksibilitas hybrid, tunjangan transportasi, dan rotasi jadwal dinas untuk yang jaraknya jauh",
    "Jadikan survei kepuasan sebagai pemicu intervensi dini per tim sebelum terlambat",
], full_width=True)

# ---------- Slide 10: Penutup ----------
s = prs.slides.add_slide(blank)
solid_bg(s, NAVY)
tf = textbox(s, 1.0, 1.8, 11.3, 1.2)
add_par(tf, "Kesimpulan", 36, WHITE, bold=True, first=True)
tf = textbox(s, 1.0, 3.0, 11.3, 3.0)
add_bullet(tf, "Lembur, gaji rendah, dan masa kerja pendek adalah tiga pendorong resign terbesar", size=18, first=True)
for b in [
    "Fokus retensi pada Sales Representative, karyawan muda, dan dua tahun pertama",
    "Tech stack: SQL di SQLite, Python dengan pandas, matplotlib, dan seaborn",
]:
    p = add_bullet(tf, b, size=18)
    for r in p.runs:
        r.font.color.rgb = WHITE
for p in tf.paragraphs:
    for r in p.runs:
        r.font.color.rgb = WHITE
tf = textbox(s, 1.0, 6.2, 11.3, 0.8)
add_par(tf, "BAGHIZ ASSHIDDIQIE ARASYA", 20, LIGHTBLUE, bold=True, first=True)

prs.save("/home/hatch/workspace/your_files/Portofolio-Analisis-HR-Attrition.pptx")
print("saved")
