import pandas as pd
import geopandas as gpd
import folium
from folium import Element
from folium.plugins import HeatMap
from map_utils import add_paygah_markers

def generate_all_years_settled_heatmap(excel_path, logo_path, shp_path):
    df = pd.read_excel(excel_path)
    col = 'تعداد کل افراد اسكان داده شده/نفر'
    if col not in df.columns:
        col = ' تعداد کل افراد اسكان داده شده/نفر'
    df = df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)', col])
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    gdf = gpd.read_file(shp_path)
    map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
    folium.GeoJson(gdf).add_to(map_zanjan)

    # تعیین مقدار max_val برای حساسیت بهتر
    max_val = df[col].max() if df[col].max() > 0 else 1

    heat_data = [
        [row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)'], float(row[col])]
        for _, row in df.iterrows() if float(row[col]) > 0
    ]
    HeatMap(
        heat_data,
        min_opacity=0.2,
        max_opacity=1,
        radius=18,
        blur=15,
        max_val=max_val,
        gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'red'}
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
        font-family: 'BTitr';
        src: url('BTitr.ttf') format('truetype');
    }}
    .titr-box {{
        font-family: 'BTitr', Tahoma, Arial, sans-serif !important;
    }}
    </style>
    <div class="titr-box" style="position: fixed; bottom: 20px; left: 20px; z-index:9999;
                background: rgba(255,255,255,0.9); border-radius: 8px; padding: 10px 18px;
                font-size: 18px; color: #6a1b9a; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        مجموع کل افراد اسکان داده شده از سال 1393 تا 1403: {total_settled}
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(count_html))
    add_paygah_markers(map_zanjan, "./paygah.xlsx", "./paygah_icon.png")
    map_zanjan.save("atlas_zanjan_Settled_HeatMap_AllYears.html")