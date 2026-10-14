"""
Menghasilkan 12 chart PNG untuk analisis HR Employee Attrition.
Sumber data : data/hr_attrition.db (tabel employees)
Keluaran    : charts/*.png
Cara pakai  : python scripts/make_charts.py
"""
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# ---- palet warna konsisten ----
TEAL = "#1F7A8C"    # utama
TEAL_DK = "#14505C"  # aksen gelap
ORANGE = "#E86A33"  # sorotan risiko tinggi
GREY = "#B0BEC5"    # netral
BG = "#F7F9FA"
TXT = "#2B3A42"

BASE_DIR = Path(__file__).resolve().parent.parent
DB = BASE_DIR / "data" / "hr_attrition.db"
OUT = BASE_DIR / "charts"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "text.color": TXT,
    "axes.labelcolor": TXT,
    "xtick.color": TXT,
    "ytick.color": TXT,
})


def query(sql):
    with sqlite3.connect(DB) as con:
        return pd.read_sql_query(sql, con)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("tulis:", name)


def bar(ax, labels, values, title, xlabel, colors=None, annotate=True):
    colors = colors or [TEAL] * len(labels)
    bars = ax.bar(labels, values, color=colors, edgecolor="white", width=0.62)
    ax.set_title(title, pad=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Attrition (%)")
    ax.set_ylim(0, max(values) * 1.22 if max(values) else 1)
    ax.spines[["top", "right"]].set_visible(False)
    if annotate:
        for b, v in zip(bars, values):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.4,
                    f"{v:.1f}%", ha="center", va="bottom", fontsize=10,
                    fontweight="bold")


# ---------- 01. attrition keseluruhan (donut) ----------
df = query("""SELECT COUNT(*) total, SUM(Attrition='Yes') resign FROM employees""")
total, resign = int(df.loc[0, "total"]), int(df.loc[0, "resign"])
fig, ax = plt.subplots(figsize=(6, 6))
wedges, _ = ax.pie([resign, total - resign], colors=[ORANGE, TEAL],
                   startangle=90, wedgeprops=dict(width=0.42, edgecolor="white"))
ax.text(0, 0.08, f"{100*resign/total:.1f}%", ha="center", fontsize=26, fontweight="bold")
ax.text(0, -0.18, "resign", ha="center", fontsize=12)
ax.set_title(f"Tingkat Attrition Keseluruhan\n{resign} dari {total} karyawan resign", pad=18)
ax.legend([f"Resign: {resign}", f"Bertahan: {total-resign}"], loc="lower center",
          bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False)
save(fig, "01_attrition_overall.png")

# ---------- 02. attrition per department ----------
df = query("""SELECT Department, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate
              FROM employees GROUP BY Department ORDER BY rate DESC""")
fig, ax = plt.subplots(figsize=(7.5, 4.6))
bar(ax, df["Department"], df["rate"], "Attrition per Departemen",
    "Departemen", colors=[ORANGE if v == df["rate"].max() else TEAL for v in df["rate"]])
save(fig, "02_attrition_department.png")

# ---------- 03. attrition per job role (barh) ----------
df = query("""SELECT JobRole, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate,
                     COUNT(*) n FROM employees GROUP BY JobRole ORDER BY rate""")
fig, ax = plt.subplots(figsize=(9, 5.2))
colors = [ORANGE if r >= 20 else TEAL for r in df["rate"]]
bars = ax.barh(df["JobRole"], df["rate"], color=colors, edgecolor="white")
ax.set_title("Attrition per Job Role (diurutkan, dengan jumlah karyawan)", pad=14)
ax.set_xlabel("Attrition (%)")
ax.spines[["top", "right"]].set_visible(False)
for b, v, n in zip(bars, df["rate"], df["n"]):
    ax.text(v + 0.6, b.get_y() + b.get_height() / 2, f"{v:.1f}%  (n={n})",
            va="center", fontsize=9.5)
ax.set_xlim(0, df["rate"].max() * 1.45)
save(fig, "03_attrition_jobrole.png")

# ---------- 04. overtime ----------
df = query("""SELECT OverTime, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate,
                     COUNT(*) n FROM employees GROUP BY OverTime ORDER BY OverTime DESC""")
labels = ["Tidak lembur (No)", "Lembur (Yes)"]
fig, ax = plt.subplots(figsize=(6.6, 4.6))
bar(ax, labels, df["rate"], "Attrition: Lembur vs Tidak Lembur", "",
    colors=[TEAL, ORANGE])
for t, n in zip(ax.get_xticklabels(), df["n"]):
    t.set_text(f"{t.get_text()}\n(n={n})")
save(fig, "04_attrition_overtime.png")

# ---------- 05. band gaji ----------
df = query("""SELECT CASE WHEN MonthlyIncome<3000 THEN '< 3.000'
        WHEN MonthlyIncome<6000 THEN '3.000-6.000'
        WHEN MonthlyIncome<10000 THEN '6.000-10.000' ELSE '> 10.000' END band,
        ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate, COUNT(*) n
        FROM employees GROUP BY band ORDER BY MIN(MonthlyIncome)""")
fig, ax = plt.subplots(figsize=(7.5, 4.6))
colors = [ORANGE if r == df["rate"].max() else TEAL for r in df["rate"]]
bar(ax, df["band"], df["rate"], "Attrition per Band Gaji Bulanan (USD)", "Band gaji",
    colors=colors)
ax.tick_params(axis="x", labelsize=10)
save(fig, "05_attrition_income_band.png")

# ---------- 06. kelompok umur ----------
df = query("""SELECT CASE WHEN Age<30 THEN '< 30' WHEN Age<40 THEN '30-39'
        WHEN Age<50 THEN '40-49' ELSE '50+' END umur,
        ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate, COUNT(*) n
        FROM employees GROUP BY umur ORDER BY MIN(Age)""")
fig, ax = plt.subplots(figsize=(7.5, 4.6))
colors = [ORANGE if r == df["rate"].max() else TEAL for r in df["rate"]]
bar(ax, df["umur"], df["rate"], "Attrition per Kelompok Umur", "Umur (tahun)",
    colors=colors)
save(fig, "06_attrition_age_group.png")

# ---------- 07. jarak rumah-kantor ----------
df = query("""SELECT CASE WHEN DistanceFromHome<5 THEN '1-4' WHEN DistanceFromHome<10 THEN '5-9'
        WHEN DistanceFromHome<15 THEN '10-14' ELSE '15+' END jarak,
        ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate, COUNT(*) n
        FROM employees GROUP BY jarak ORDER BY MIN(DistanceFromHome)""")
fig, ax = plt.subplots(figsize=(7.5, 4.6))
bar(ax, df["jarak"], df["rate"], "Attrition per Jarak Rumah ke Kantor", "Jarak (km)",
    colors=[TEAL] * 4)
save(fig, "07_attrition_distance.png")

# ---------- 08. job satisfaction ----------
order_js = ["Low", "Medium", "High", "Very High"]
df = query("""SELECT JobSatisfaction, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate
              FROM employees GROUP BY JobSatisfaction""").set_index("JobSatisfaction").loc[order_js].reset_index()
fig, ax = plt.subplots(figsize=(7.5, 4.6))
bar(ax, df["JobSatisfaction"], df["rate"], "Attrition per Kepuasan Kerja",
    "Kepuasan kerja", colors=[ORANGE, TEAL, TEAL, TEAL])
save(fig, "08_attrition_job_satisfaction.png")

# ---------- 09. environment satisfaction ----------
order_es = ["Low", "Medium", "High", "Very High"]
df = query("""SELECT EnvironmentSatisfaction, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate
              FROM employees GROUP BY EnvironmentSatisfaction""").set_index("EnvironmentSatisfaction").loc[order_es].reset_index()
fig, ax = plt.subplots(figsize=(7.5, 4.6))
bar(ax, df["EnvironmentSatisfaction"], df["rate"], "Attrition per Kepuasan Lingkungan Kerja",
    "Kepuasan lingkungan kerja", colors=[ORANGE, TEAL, TEAL, TEAL])
save(fig, "09_attrition_env_satisfaction.png")

# ---------- 10. work-life balance ----------
order_wlb = ["Bad", "Good", "Better", "Best"]
df = query("""SELECT WorkLifeBalance, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate
              FROM employees GROUP BY WorkLifeBalance""").set_index("WorkLifeBalance").loc[order_wlb].reset_index()
fig, ax = plt.subplots(figsize=(7.5, 4.6))
bar(ax, df["WorkLifeBalance"], df["rate"], "Attrition per Work-Life Balance",
    "Work-life balance", colors=[ORANGE, TEAL, TEAL, TEAL])
save(fig, "10_attrition_worklife_balance.png")

# ---------- 11. tenure: 3 subplot ----------
fig, axes = plt.subplots(1, 3, figsize=(13, 4.6), sharey=True)
q1 = """SELECT CASE WHEN YearsAtCompany<3 THEN '0-2' WHEN YearsAtCompany<6 THEN '3-5'
        WHEN YearsAtCompany<11 THEN '6-10' ELSE '11+' END g,
        ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate
        FROM employees GROUP BY g ORDER BY MIN(YearsAtCompany)"""
q2 = """SELECT CASE WHEN YearsInCurrentRole<3 THEN '0-2' WHEN YearsInCurrentRole<6 THEN '3-5'
        ELSE '6+' END g, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate
        FROM employees GROUP BY g ORDER BY MIN(YearsInCurrentRole)"""
q3 = """SELECT CASE WHEN YearsSinceLastPromotion<3 THEN '0-2' WHEN YearsSinceLastPromotion<6 THEN '3-5'
        ELSE '6+' END g, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate
        FROM employees GROUP BY g ORDER BY MIN(YearsSinceLastPromotion)"""
for ax, sql, title, xl in zip(axes, [q1, q2, q3],
        ["Attrition per Masa Kerja\n(YearsAtCompany)", "Attrition per Lama di Posisi\n(YearsInCurrentRole)",
         "Attrition per Jarak Promosi\n(YearsSinceLastPromotion)"],
        ["Masa kerja (tahun)", "Lama di posisi (tahun)", "Sejak promosi (tahun)"]):
    d = query(sql)
    bar(ax, d["g"], d["rate"], title, xl,
        colors=[ORANGE if r == d["rate"].max() else TEAL for r in d["rate"]])
    ax.set_ylabel("Attrition (%)")
fig.suptitle("Attrition per Ukuran Masa Kerja", fontsize=15, fontweight="bold", y=1.03)
save(fig, "11_attrition_tenure.png")

# ---------- 12. demografi + travel (2x2) ----------
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Attrition per Profil Demografi dan Pola Perjalanan Dinas",
             fontsize=15, fontweight="bold", y=1.0)

d = query("""SELECT Gender, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate
             FROM employees GROUP BY Gender""")
bar(axes[0, 0], d["Gender"], d["rate"], "per Gender", "Gender")

d = query("""SELECT MaritalStatus, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate
             FROM employees GROUP BY MaritalStatus ORDER BY rate DESC""")
bar(axes[0, 1], d["MaritalStatus"], d["rate"], "per Status Perkawinan",
    "Status perkawinan", colors=[ORANGE if r == d["rate"].max() else TEAL for r in d["rate"]])

d = query("""SELECT BusinessTravel, ROUND(100.0*SUM(Attrition='Yes')/COUNT(*),1) rate
             FROM employees GROUP BY BusinessTravel ORDER BY rate DESC""")
labels_bt = {"Travel_Frequently": "Sering dinas", "Travel_Rarely": "Jarang dinas",
             "Non-Travel": "Tidak dinas"}
bar(axes[1, 0], [labels_bt.get(x, x) for x in d["BusinessTravel"]], d["rate"],
    "per Pola Perjalanan Dinas", "Pola perjalanan dinas",
    colors=[ORANGE if r == d["rate"].max() else TEAL for r in d["rate"]])

# panel ke-4: ringkasan segmen berisiko tertinggi
axes[1, 1].axis("off")
ringkas = [
    ("Lembur (Yes)", 30.5), ("Masa kerja 0-2 thn", 29.8),
    ("Gaji < 3.000", 28.6), ("Umur < 30", 27.9),
    ("Single", 25.5), ("Sering dinas", 24.9),
]
axes[1, 1].text(0.05, 0.95, "Segmen berisiko tertinggi", fontsize=13,
                fontweight="bold", transform=axes[1, 1].transAxes)
for i, (label, v) in enumerate(ringkas):
    axes[1, 1].text(0.05, 0.84 - i * 0.13, f"• {label}: {v:.1f}%",
                    fontsize=11, transform=axes[1, 1].transAxes)
save(fig, "12_attrition_demografi_travel.png")

print("Selesai: 12 chart.")
