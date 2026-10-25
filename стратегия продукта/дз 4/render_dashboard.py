# -*- coding: utf-8 -*-
"""Рендер дашборда «Сфера · Пульс» в PNG по данным Сфера_Пульс_графики.xlsx."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.ticker as mtick

XLSX = r"D:\Софья Зименкова\учёба\магистратура\study\стратегия продукта\дз 4\Сфера_Пульс_графики.xlsx"
OUT = r"D:\Софья Зименкова\учёба\магистратура\study\стратегия продукта\дз 4\dashboard_pulse.png"

# шрифт с кириллицей
for cand in ["Noto Sans", "Segoe UI", "Arial"]:
    try:
        font_manager.findfont(cand, fallback_to_default=False)
        plt.rcParams["font.family"] = cand
        break
    except Exception:
        continue
plt.rcParams["axes.unicode_minus"] = False

raw = pd.read_excel(XLSX, sheet_name="Данные")
p = raw[raw["Продукт"] == "Пульс"].sort_values("Месяц").reset_index(drop=True)
p["Маржа, %"] = (p["Выручка, ₽"] - p["Затраты всего, ₽"]) / p["Выручка, ₽"] * 100
months = [m[2:] for m in p["Месяц"]]  # YY-MM
x = range(24)

m24, m25 = p.iloc[:12], p.iloc[12:]
kpi = {
    "МАРЖА, ср. 2025": f"{m25['Маржа, %'].mean():+.1f}%".replace("-", "−"),
    "ПЛАН-ФАКТ 2025": f"{p['Выручка, ₽'][12:].sum()/p['План выручки, ₽'][12:].sum()*100:.1f}%",
    "РОСТ АУДИТОРИИ": f"+{p['MAU'].iloc[-1]/p['MAU'].iloc[0]*100-100:.0f}% за 24 мес.",
    "УДЕРЖАНИЕ M1": f"{m25['Retention M1, %'].mean()-m24['Retention M1, %'].mean():+.1f} п.п.".replace("-", "−"),
    "КОММИТЫ": f"{m25['GitLab: коммиты'].mean()/m24['GitLab: коммиты'].mean()*100-100:+.0f}%".replace("-", "−"),
    "ДЕПЛОИ В ПРОД": f"{m25['Деплоев в прод'].mean()/m24['Деплоев в прод'].mean()*100-100:+.0f}%".replace("-", "−"),
}
kpi_sub = {
    "МАРЖА, ср. 2025": "2024: −22,3% → весь 2025 в плюсе",
    "ПЛАН-ФАКТ 2025": "Σвыручка / Σплан за 12 мес.",
    "РОСТ АУДИТОРИИ": "MAU, янв-24 → дек-25",
    "УДЕРЖАНИЕ M1": "ср. 2025 против ср. 2024",
    "КОММИТЫ": "ср./мес, 2025 к 2024",
    "ДЕПЛОИ В ПРОД": "ср./мес, 2025 к 2024",
}

fig = plt.figure(figsize=(16.5, 11.5), dpi=150)
fig.patch.set_facecolor("#FFFFFF")
fig.suptitle("Сфера · Дашборд продукта «Пульс» · январь 2024 — декабрь 2025 · эффективен и развивается: ДА",
             fontsize=17, fontweight="bold", y=0.975, color="#1a1a2e")

# KPI-карточки
for i, (k, v) in enumerate(kpi.items()):
    ax = fig.add_axes([0.03 + i * 0.162, 0.845, 0.148, 0.10])
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor="#EEF3FB", edgecolor="#B9C8E4", lw=1))
    ax.text(0.5, 0.72, k, ha="center", va="center", fontsize=9.5, color="#44557A", fontweight="bold")
    ax.text(0.5, 0.40, v, ha="center", va="center", fontsize=15, color="#123B7A", fontweight="bold")
    ax.text(0.5, 0.13, kpi_sub[k], ha="center", va="center", fontsize=7.5, color="#6B7A99")

def style(ax, title):
    ax.set_title(title, fontsize=11, fontweight="bold", color="#1a1a2e", pad=8)
    ax.grid(True, axis="y", ls=":", alpha=0.45)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xticks(list(x)[::3])
    ax.set_xticklabels([months[i] for i in range(0, 24, 3)], fontsize=8)

# 1. Маржа
fig.subplots_adjust(left=0.05, right=0.97, top=0.80, bottom=0.06, hspace=0.75, wspace=0.28)
ax = fig.add_subplot(3, 2, 1); style(ax, "Маржа в % выручки")
ax.plot(x, p["Маржа, %"], color="#1B6E3C", lw=2.2, marker="o", ms=3, label="Маржа, %")
ax.axhline(0, color="#888", lw=0.8)
ax.legend(fontsize=8, loc="upper left")

# 2. Выручка против плана (бары план + линия факт)
ax = fig.add_subplot(3, 2, 2); style(ax, "Выручка против плана, млн ₽")
ax.bar(x, p["План выручки, ₽"] / 1e6, color="#C9D4E8", label="План, млн ₽")
ax.plot(x, p["Выручка, ₽"] / 1e6, color="#1B6E3C", lw=2.2, marker="o", ms=3, label="Факт, млн ₽")
ax.legend(fontsize=8, loc="upper left")

# 3. План-факт, %
ax = fig.add_subplot(3, 2, 3); style(ax, "Выполнение плана по месяцам, %")
ax.plot(x, p["Выручка, ₽"] / p["План выручки, ₽"] * 100, color="#123B7A", lw=2.2, marker="o", ms=3, label="План-факт, %")
ax.plot(x, [100] * 24, color="#C0392B", lw=1.2, ls="--", label="Цель 100%")
ax.set_ylim(90, 112)
ax.legend(fontsize=8, loc="lower right")

# 4. Аудитория: MAU + платящие (правая ось)
ax = fig.add_subplot(3, 2, 4); style(ax, "Аудитория: MAU и платящие")
ax.plot(x, p["MAU"], color="#123B7A", lw=2.2, marker="o", ms=3, label="MAU")
ax2 = ax.twinx(); ax2.spines["top"].set_visible(False)
ax2.plot(x, p["Платящие пользователи"], color="#E67E22", lw=2, marker="s", ms=3, label="Платящие (пр. ось)")
ax.legend(fontsize=8, loc="upper left"); ax2.legend(fontsize=8, loc="lower right")

# 5. Разработка: коммиты (левая) + деплои и разработчики (правая)
ax = fig.add_subplot(3, 2, 5); style(ax, "Разработка: коммиты (слева), деплои и разработчики (справа)")
ax.plot(x, p["GitLab: коммиты"], color="#123B7A", lw=2.2, marker="o", ms=3, label="Коммиты")
ax2 = ax.twinx(); ax2.spines["top"].set_visible(False)
ax2.plot(x, p["Деплоев в прод"], color="#1B6E3C", lw=2, marker="^", ms=3, label="Деплои в прод")
ax2.plot(x, p["Активных разработчиков"], color="#8E44AD", lw=2, marker="s", ms=3, label="Активные разработчики")
ax.legend(fontsize=8, loc="upper left"); ax2.legend(fontsize=8, loc="lower right")

# 6. Retention
ax = fig.add_subplot(3, 2, 6); style(ax, "Удержание: Retention M1, %")
ax.plot(x, p["Retention M1, %"], color="#1B6E3C", lw=2.2, marker="o", ms=3, label="Retention M1, %")
ax.legend(fontsize=8, loc="upper left")

fig.savefig(OUT, bbox_inches="tight", facecolor="#FFFFFF")
print("saved", OUT)
