import pandas as pd
import geopandas as gpd
import folium
from folium import Element
from folium.plugins import HeatMap
from map_utils import add_paygah_markers

def generate_all_years_jaddeh_heatmap(excel_path, logo_path, shp_path):
    df = pd.read_excel(excel_path)
    df_jaddeh = df[df['نوع حادثه'] == 'جاده ای']
    df_jaddeh = df_jaddeh.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)'])

    shp_gdf = gpd.read_file(shp_path)
    map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
    folium.GeoJson(shp_gdf, name="Shapefile Layer").add_to(map_zanjan)

    heat_data = [
        [row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']]
        for _, row in df_jaddeh.iterrows()
    ]
    HeatMap(
        heat_data,
        min_opacity=0.3,
        max_opacity=0.8,
        radius=18,
        blur=15,
        gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'red'}
    ).add_to(map_zanjan)

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
                font-size: 18px; color: #d32f2f; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        تعداد کل حوادث جاده ای از سال 1393 تا 1403: {len(df_jaddeh)}
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(count_html))

    add_paygah_markers(map_zanjan, "./Data/paygah.xlsx", "./Data/paygah_icon.png")

    map_zanjan.save("atlas_zanjan_Jaddeh_HeatMap_AllYears.html")