import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import arabic_reshaper
from bidi.algorithm import get_display
import jdatetime
import folium
import geopandas as gpd
import numpy as np

font_path = "./b-nazanin.ttf"
font_prop = font_manager.FontProperties(fname=font_path)

def fa(text):
    return get_display(arabic_reshaper.reshape(text))

plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]

FONT_SIZE = 16  # اندازه فونت دلخواه

def plot_incident_count_by_year(excel_path):
    df = pd.read_excel(excel_path)
    df['سال'] = df['تاريخ وقوع حادثه'].astype(str).str[:4]
    year_counts = df.groupby('سال').size()
    plt.figure(figsize=(8,5))
    ax = year_counts.plot(kind='bar', color='#1976d2')
    plt.title(fa('تعداد کل حوادث به تفکیک سال'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.xlabel(fa('سال'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.ylabel(fa('تعداد حوادث'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    # نمایش مقدار بالای هر ستون
    for i, v in enumerate(year_counts):
        ax.text(i, v + 2, str(v), ha='center', va='bottom', fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.tight_layout()
    plt.show()

def plot_injury_deceased_trend(excel_path):
    df = pd.read_excel(excel_path)
    df['سال'] = df['تاريخ وقوع حادثه'].astype(str).str[:4]
    deceased = df.groupby('سال')['مجموع کل فوتی'].sum()
    plt.figure(figsize=(8,5))
    plt.plot(deceased.index, deceased.values, marker='s', color='black')
    for x, y in zip(deceased.index, deceased.values):
        plt.text(x, y + 2, str(int(y)), ha='center', va='bottom', fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.title(fa('روند سالانه فوتی‌ها'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.xlabel(fa('سال'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.ylabel(fa('تعداد فوتی‌ها'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_injury_trend(excel_path):
    df = pd.read_excel(excel_path)
    df['سال'] = df['تاريخ وقوع حادثه'].astype(str).str[:4]
    injury = df.groupby('سال')['تعداد کل مصدومین در حادثه /نفر'].sum()
    plt.figure(figsize=(8,5))
    plt.plot(injury.index, injury.values, marker='o', color='orange')
    for x, y in zip(injury.index, injury.values):
        plt.text(x, y + 2, str(int(y)), ha='center', va='bottom', fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.title(fa('روند سالانه مصدومین'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.xlabel(fa('سال'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.ylabel(fa('تعداد مصدومین'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_incident_type_pie(excel_path):
    df = pd.read_excel(excel_path)
    incident_counts = df['نوع حادثه'].value_counts()
    labels = [fa(str(i)) for i in incident_counts.index]
    values = incident_counts.values

    plt.figure(figsize=(7,7))
    wedges, texts, autotexts = plt.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.tab20.colors,
        textprops={'fontproperties': font_prop, 'fontsize': FONT_SIZE}
    )
    # نمایش مقدار دقیق هر بخش کنار لیبل
    for i, (w, v) in enumerate(zip(wedges, values)):
        ang = (w.theta2 + w.theta1) / 2.
        x = 0.85 * np.cos(np.deg2rad(ang))
        y = 0.85 * np.sin(np.deg2rad(ang))
        plt.text(x, y, str(v), ha='center', va='center', fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.title(fa('سهم هر نوع حادثه از کل حوادث'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

def plot_spatial_scatter(excel_path):
    df = pd.read_excel(excel_path)
    df['طول جغرافیایی(E)'] = pd.to_numeric(df['طول جغرافیایی(E)'], errors='coerce')
    df['عرض جغرافیایی(N)'] = pd.to_numeric(df['عرض جغرافیایی(N)'], errors='coerce')
    df = df.dropna(subset=['طول جغرافیایی(E)', 'عرض جغرافیایی(N)'])
    plt.figure(figsize=(8,7))
    plt.scatter(df['طول جغرافیایی(E)'], df['عرض جغرافیایی(N)'],
                s=20, c='red', alpha=0.5)
    plt.title(fa('پراکندگی مکانی نقاط حادثه‌خیز'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.xlabel(fa('طول جغرافیایی(E)'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.ylabel(fa('عرض جغرافیایی(N)'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def get_weekday(jalali_date_str):
    try:
        parts = [int(x) for x in jalali_date_str.replace("-", "/").split("/")]
        if len(parts) == 3:
            date = jdatetime.date(parts[0], parts[1], parts[2])
            weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']
            return weekdays[date.weekday()]
    except Exception:
        return ""
    return ""

def plot_jaddeh_weekday_bar(excel_path):
    df = pd.read_excel(excel_path)
    df_jaddeh = df[df['نوع حادثه'] == 'جاده ای'].copy()
    df_jaddeh['روز هفته'] = df_jaddeh['تاريخ وقوع حادثه'].astype(str).apply(get_weekday)
    weekday_order = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']
    weekday_counts = df_jaddeh['روز هفته'].value_counts().reindex(weekday_order)
    weekday_counts.index = [fa(day) for day in weekday_order]
    plt.figure(figsize=(8,5))
    ax = weekday_counts.plot(kind='bar', color='#d32f2f')
    plt.title(fa('تعداد حوادث جاده‌ای به تفکیک روزهای هفته'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.xlabel(fa('روز هفته'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.ylabel(fa('تعداد حوادث جاده‌ای'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    # نمایش مقدار بالای هر ستون
    for i, v in enumerate(weekday_counts):
        ax.text(i, v + 2, str(v), ha='center', va='bottom', fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.tight_layout()
    plt.show()

def plot_spatial_scatter_osm(excel_path, output_html="spatial_scatter_osm.html"):
    df = pd.read_excel(excel_path)
    df['طول جغرافیایی(E)'] = pd.to_numeric(df['طول جغرافیایی(E)'], errors='coerce')
    df['عرض جغرافیایی(N)'] = pd.to_numeric(df['عرض جغرافیایی(N)'], errors='coerce')
    df = df.dropna(subset=['طول جغرافیایی(E)', 'عرض جغرافیایی(N)'])

    # مرکز نقشه را میانگین نقاط قرار بده
    lat_center = df['عرض جغرافیایی(N)'].mean()
    lon_center = df['طول جغرافیایی(E)'].mean()
    m = folium.Map(location=[lat_center, lon_center], zoom_start=8, tiles='OpenStreetMap')

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
            radius=4,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.7,
        ).add_to(m)

    # ذخیره خروجی به صورت HTML
    m.save(output_html)
    print(f"نقشه پراکندگی مکانی نقاط حادثه‌خیز با پس‌زمینه OSM در فایل {output_html} ذخیره شد.")

def generate_spatial_scatter_osm(excel_path, logo_path, shp_path, output_html="atlas_zanjan_SpatialScatterOSM.html"):
    df = pd.read_excel(excel_path)
    df = df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)'])
    df['طول جغرافیایی(E)'] = pd.to_numeric(df['طول جغرافیایی(E)'], errors='coerce')
    df['عرض جغرافیایی(N)'] = pd.to_numeric(df['عرض جغرافیایی(N)'], errors='coerce')
    df = df.dropna(subset=['طول جغرافیایی(E)', 'عرض جغرافیایی(N)'])

    lat_center = df['عرض جغرافیایی(N)'].mean()
    lon_center = df['طول جغرافیایی(E)'].mean()
    map_zanjan = folium.Map(location=[lat_center, lon_center], zoom_start=8, tiles='OpenStreetMap')

    # اضافه کردن لایه نقشه (Shapefile یا GeoJSON)
    try:
        gdf = gpd.read_file(shp_path)
        folium.GeoJson(gdf, name="Shapefile Layer").add_to(map_zanjan)
    except Exception as e:
        print(f"خطا در افزودن نقشه: {e}")

    for _, row in df.iterrows():
        popup_text = (
            f"<b>شرح حادثه:</b> {row['شرح حادثه'] if 'شرح حادثه' in row else ''}<br>"
            f"<b>تاریخ وقوع:</b> {row['تاريخ وقوع حادثه'] if 'تاريخ وقوع حادثه' in row else ''}"
        )
        folium.Circle(
            location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
            radius=80,
            color='crimson',
            fill=True,
            fill_color='crimson',
            fill_opacity=0.5,
            popup=popup_text
        ).add_to(map_zanjan)

    logo_html = f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
        <img src="{logo_path}" alt="logo" width="85">
    </div>
    """
    map_zanjan.get_root().html.add_child(folium.Element(logo_html))

    count_html = f"""
    <style>
    @font-face {{
        font-family: "B Titr Bold";
        src: url("https://db.onlinewebfonts.com/t/a0ea7e7833cd4f7694a4913fccb9aacf.ttf")format("truetype");
    }}
    .titr-box {{
        font-family: 'B Titr Bold', Tahoma, Arial, sans-serif !important;
    }}
    </style>
    <div class="titr-box" style="position: fixed; bottom: 20px; left: 20px; z-index:9999;
                background: rgba(255,255,255,0.9); border-radius: 8px; padding: 10px 18px;
                font-size: 18px; color: #d32f2f; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        تعداد کل نقاط حادثه‌خیز: {len(df)}
    </div>
    """
    map_zanjan.get_root().html.add_child(folium.Element(count_html))

    map_zanjan.save(output_html)

def plot_transferred_trend(excel_path):
    df = pd.read_excel(excel_path)
    df['سال'] = df['تاريخ وقوع حادثه'].astype(str).str[:4]
    transferred = df.groupby('سال')['مصدومين انتقالي توسط جمعیت/نفر'].sum()
    plt.figure(figsize=(8,5))
    plt.plot(transferred.index, transferred.values, marker='D', color='#1976d2')
    for x, y in zip(transferred.index, transferred.values):
        plt.text(x, y + 2, str(int(y)), ha='center', va='bottom', fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.title(fa('روند سالانه مصدومین انتقالی توسط جمعیت'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.xlabel(fa('سال'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.ylabel(fa('مصدومین انتقالی'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_treated_trend(excel_path):
    df = pd.read_excel(excel_path)
    df['سال'] = df['تاريخ وقوع حادثه'].astype(str).str[:4]
    treated = df.groupby('سال')['درمان سرپايي توسط جمعیت/نفر'].sum()
    plt.figure(figsize=(8,5))
    plt.plot(treated.index, treated.values, marker='^', color='#388e3c')
    for x, y in zip(treated.index, treated.values):
        plt.text(x, y + 2, str(int(y)), ha='center', va='bottom', fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.title(fa('روند سالانه درمان سرپایی توسط جمعیت'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.xlabel(fa('سال'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.ylabel(fa('درمان سرپایی'), fontproperties=font_prop, fontsize=FONT_SIZE)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_total_aided_trend(excel_path):
    df = pd.read_excel(excel_path)
    df['سال'] = df['تاريخ وقوع حادثه'].astype(str).str[:4]
    if 'تعداد کل افراد امدادرسانی شده' in df.columns:
        total_aided = df.groupby('سال')['تعداد کل افراد امدادرسانی شده'].sum()
        plt.figure(figsize=(8,5))
        plt.plot(total_aided.index, total_aided.values, marker='o', color='#fbc02d')
        for x, y in zip(total_aided.index, total_aided.values):
            plt.text(x, y + 2, str(int(y)), ha='center', va='bottom', fontproperties=font_prop, fontsize=FONT_SIZE)
        plt.title(fa('روند سالانه کل افراد امدادرسانی شده'), fontproperties=font_prop, fontsize=FONT_SIZE)
        plt.xlabel(fa('سال'), fontproperties=font_prop, fontsize=FONT_SIZE)
        plt.ylabel(fa('کل افراد امدادرسانی شده'), fontproperties=font_prop, fontsize=FONT_SIZE)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
    else:
        print("ستون 'تعداد کل افراد امدادرسانی شده' در فایل وجود ندارد.")