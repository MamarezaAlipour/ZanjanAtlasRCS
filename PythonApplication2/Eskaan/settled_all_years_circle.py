import pandas as pd
import geopandas as gpd
import folium
from folium import Element
from map_utils import add_paygah_markers

def generate_all_years_settled_circle_map(excel_path, logo_path, shp_path):
    df = pd.read_excel(excel_path)
    # توجه: نام ستون را دقیق بنویسید (با یا بدون فاصله اول)
    col = 'تعداد کل افراد اسكان داده شده/نفر'
    if col not in df.columns:
        col = ' تعداد کل افراد اسكان داده شده/نفر'
    df = df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)', col])
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    gdf = gpd.read_file(shp_path)
    map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
    folium.GeoJson(gdf).add_to(map_zanjan)

    for _, row in df.iterrows():
        value = float(row[col])
        if value > 0:
            popup_html = f"""
            <style>
            @font-face {{
                font-family: 'BNazanin';
                src: url('Static/B-NAZANIN.TTF') format('truetype');
            }}
            .nazanin-popup {{
                font-family: 'BNazanin', Tahoma, Arial, sans-serif !important;
                font-size: 16px;
                text-align: center;
            }}
            </style>
            <div class="nazanin-popup">
                اسکان داده شده: {int(value)}<br>
                نوع حادثه: {row.get('نوع حادثه', '')}<br>
                تاریخ وقوع: {row.get('تاريخ وقوع حادثه', '')}
            </div>
            """
            folium.Circle(
                location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
                radius=50 + value * 10,  # مقیاس استاندارد مثل بقیه نقشه‌ها
                color='purple',
                fill=True,
                fill_color='purple',
                fill_opacity=0.5,
                popup=folium.Popup(popup_html, max_width=350)
            ).add_to(map_zanjan)

    logo_html = f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
        <img src="{logo_path}" alt="logo" width="85">
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(logo_html))

    total_settled = int(df[col].sum())
    count_html = f"""
    <style>
    @font-face {{
        font-family: "B Titr Bold";
        src: url("https://db.onlinewebfonts.com/t/a0ea7e7833cd4f7694a4913fccb9aacf.eot");
        src: url("https://db.onlinewebfonts.com/t/a0ea7e7833cd4f7694a4913fccb9aacf.eot?#iefix")format("embedded-opentype"),
        url("https://db.onlinewebfonts.com/t/a0ea7e7833cd4f7694a4913fccb9aacf.woff2")format("woff2"),
        url("https://db.onlinewebfonts.com/t/a0ea7e7833cd4f7694a4913fccb9aacf.woff")format("woff"),
        url("https://db.onlinewebfonts.com/t/a0ea7e7833cd4f7694a4913fccb9aacf.ttf")format("truetype"),
        url("https://db.onlinewebfonts.com/t/a0ea7e7833cd4f7694a4913fccb9aacf.svg#B Titr Bold")format("svg");
    }}
    .titr-box {{
        font-family: 'B Titr Bold', Tahoma, Arial, sans-serif !important;
    }}
    </style>
    <div class="titr-box" style="position: fixed; bottom: 20px; left: 20px; z-index:9999;
                background: rgba(255,255,255,0.9); border-radius: 8px; padding: 10px 18px;
                font-size: 18px; color: #6a1b9a; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        مجموع کل افراد اسکان داده شده از سال 1393 تا 1403: {total_settled}
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(count_html))
    add_paygah_markers(map_zanjan, "./Data/paygah.xlsx", "./Data/paygah_icon.png")
    map_zanjan.save("atlas_zanjan_Settled_Circle_AllYears.html")