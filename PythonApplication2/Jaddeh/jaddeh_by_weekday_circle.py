import pandas as pd
import geopandas as gpd
import folium
from folium import Element
import jdatetime
from map_utils import add_paygah_markers

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

def generate_jaddeh_weekday_circle_maps(excel_path, logo_path, shp_path):
    df = pd.read_excel(excel_path)
    df = df[df['نوع حادثه'] == 'جاده ای']
    df = df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)'])
    df['روز هفته'] = df['تاريخ وقوع حادثه'].astype(str).apply(get_weekday)

    gdf = gpd.read_file(shp_path)
    weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']

    for weekday in weekdays:
        df_day = df[df['روز هفته'] == weekday]
        map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
        folium.GeoJson(gdf).add_to(map_zanjan)

        for _, row in df_day.iterrows():
            popup_text = (
                f"<b>تاریخ وقوع حادثه:</b> {row['تاريخ وقوع حادثه'] if pd.notnull(row['تاريخ وقوع حادثه']) else '-'}<br>"
                f"<b>شرح حادثه:</b> {row['شرح حادثه']}<br>"
                f"<b>تعداد کل مصدومین:</b> {int(row['تعداد کل مصدومین در حادثه /نفر']) if pd.notnull(row['تعداد کل مصدومین در حادثه /نفر']) else '-'}<br>"
                f"<b>مصدومین انتقالی:</b> {int(row['مصدومين انتقالي توسط جمعیت/نفر']) if pd.notnull(row['مصدومين انتقالي توسط جمعیت/نفر']) else '-'}<br>"
                f"<b>درمان سرپایی:</b> {int(row['درمان سرپايي توسط جمعیت/نفر']) if pd.notnull(row['درمان سرپايي توسط جمعیت/نفر']) else '-'}<br>"
                f"<b>مجموع کل فوتی:</b> {int(row['مجموع کل فوتی']) if pd.notnull(row['مجموع کل فوتی']) else '-'}"
            )
            folium.Circle(
                location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
                radius=60,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.5,
                popup=popup_text
            ).add_to(map_zanjan)

        # افزودن نشانگرهای پایگاه
        add_paygah_markers(map_zanjan, "./Data/paygah.xlsx", "./Data/paygah_icon.png")

        logo_html = f"""
        <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
            <img src="{logo_path}" alt="logo" width="85">
        </div>
        """
        map_zanjan.get_root().html.add_child(Element(logo_html))

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
            تعداد حوادث جاده‌ای روز {weekday} از 1393 تا 1403: {len(df_day)}
        </div>
        """
        map_zanjan.get_root().html.add_child(Element(count_html))

        map_zanjan.save(f"atlas_zanjan_Jaddeh_Circle_{weekday}.html")