import pandas as pd
import geopandas as gpd
import folium
from folium import Element

def add_deceased_circles_black(map_obj, df, value_column, value_label="فوتی‌ها", extra_popup_columns=None):
    if extra_popup_columns is None:
        extra_popup_columns = []
    for _, row in df.iterrows():
        try:
            value = float(row[value_column])
        except (ValueError, TypeError):
            value = 0
        if value > 0:
            popup_parts = [f"{value_label}: {int(value)}"]
            for col in extra_popup_columns:
                popup_parts.append(f"{col}: {row.get(col, '')}")
            popup_text = "<br>".join(popup_parts)
            folium.Circle(
                location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
                radius=50 + value * 10,
                color='black',
                fill=True,
                fill_color='black',
                fill_opacity=0.5,
                popup=popup_text
            ).add_to(map_obj)

def generate_all_years_deceased_jaddeh_circle_map(excel_path, logo_path, shp_path):
    df = pd.read_excel(excel_path)
    df = df[df['نوع حادثه'] == 'جاده ای']
    df = df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)', 'مجموع کل فوتی'])
    df['مجموع کل فوتی'] = pd.to_numeric(df['مجموع کل فوتی'], errors='coerce').fillna(0)

    gdf = gpd.read_file(shp_path)
    map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
    folium.GeoJson(gdf).add_to(map_zanjan)

    add_deceased_circles_black(
        map_zanjan,
        df,
        "مجموع کل فوتی",
        value_label="فوتی‌ها",
        extra_popup_columns=["شرح حادثه", "تاريخ وقوع حادثه"]
    )

    logo_html = f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
        <img src="{logo_path}" alt="logo" width="85">
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(logo_html))

    total_deceased = int(df["مجموع کل فوتی"].sum())
    count_html = f"""
    <style>
    @font-face {{
        font-family: 'BTitr';
        src: url('BTitr.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    .titr-box {{
        font-family: 'BTitr', Tahoma, Arial, sans-serif !important;
    }}
    </style>
    <div class="titr-box" style="position: fixed; bottom: 20px; left: 20px; z-index:9999;
                background: rgba(255,255,255,0.9); border-radius: 8px; padding: 10px 18px;
                font-size: 18px; color: #222; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        مجموع کل فوتی حوادث جاده‌ای از سال 1393 تا 1403: {total_deceased}
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(count_html))

    map_zanjan.save("atlas_zanjan_Deceased_Jaddeh_Circle_AllYears.html")