import pandas as pd
import geopandas as gpd
import folium
from folium import Element
from folium.plugins import HeatMap
from .nejatfanni_utils import compute_nejatfani_count
from map_utils import add_paygah_markers

def generate_all_years_nejatfanni_heatmap(nejatfanni_path, logo_path, shp_path):
    df = pd.read_excel(nejatfanni_path)
    df = compute_nejatfani_count(df)
    gdf = gpd.read_file(shp_path)
    map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
    folium.GeoJson(gdf).add_to(map_zanjan)

    heat_data = [
        [row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)'], row['تعداد نجات فنی']]
        for _, row in df.iterrows()
    ]
    HeatMap(
        heat_data,
        min_opacity=0.3,
        max_opacity=0.8,
        radius=25,
        blur=18,
        gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'red'}
    ).add_to(map_zanjan)

    logo_html = f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
        <img src="{logo_path}" alt="logo" width="85">
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(logo_html))

    total_nejat = int(df['تعداد نجات فنی'].sum())
    count_html = f"""
    <style>
    @font-face {{
        font-family: 'BTitr';
        src: url('Static/BTitr.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    .titr-box {{
        font-family: 'BTitr', Tahoma, Arial, sans-serif !important;
    }}
    </style>
    <div class="titr-box" style="position: fixed; bottom: 20px; left: 20px; z-index:9999;
                background: rgba(255,255,255,0.9); border-radius: 8px; padding: 10px 18px;
                font-size: 18px; color: #1976d2; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        مجموع رهاسازی در حوادث جاده‌ای از سال 1393 تا 1403: {total_nejat}
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(count_html))

    # فرض بر این است که paygah.xlsx و paygah_icon.png در مسیر پروژه هستند
    add_paygah_markers(map_zanjan, "./Data/paygah.xlsx", "./Data/paygah_icon.png")

    map_zanjan.save("atlas_zanjan_NejatFanni_HeatMap_AllYears.html")