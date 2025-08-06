import pandas as pd
import geopandas as gpd
import folium
from folium import Element
from folium.plugins import HeatMap
from map_utils import add_injury_heatmap_legend, add_value_circles

def generate_all_years_injury_jaddeh_map(excel_path, logo_path, shp_path):
    df = pd.read_excel(excel_path)
    df_jaddeh = df[df['نوع حادثه'] == 'جاده ای']
    df_jaddeh = df_jaddeh.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)', 'تعداد کل مصدومین در حادثه /نفر'])
    df_jaddeh['تعداد کل مصدومین در حادثه /نفر'] = pd.to_numeric(df_jaddeh['تعداد کل مصدومین در حادثه /نفر'], errors='coerce').fillna(0)

    gdf = gpd.read_file(shp_path)
    map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
    folium.GeoJson(gdf).add_to(map_zanjan)

    # HeatMap مصدومین جاده‌ای
    heat_data = [
        [row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)'], float(row['تعداد کل مصدومین در حادثه /نفر'])]
        for _, row in df_jaddeh.iterrows() if float(row['تعداد کل مصدومین در حادثه /نفر']) > 0
    ]
    HeatMap(
        heat_data,
        min_opacity=0.3,
        max_opacity=0.8,
        radius=25,
        blur=18,
        gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'red'}
    ).add_to(map_zanjan)

    # دایره‌های مصدومین جاده‌ای
    add_value_circles(map_zanjan, df_jaddeh, "تعداد کل مصدومین در حادثه /نفر", value_label="مصدومین", extra_popup_columns=["شرح حادثه", "تاريخ وقوع حادثه"])

    # لوگو و راهنمای HeatMap
    logo_html = f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
        <img src="{logo_path}" alt="logo" width="85">
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(logo_html))

    total_injuries_all = int(df_jaddeh['تعداد کل مصدومین در حادثه /نفر'].sum())
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
                font-size: 18px; color: #d32f2f; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        مجموع کل مصدومین جاده ای از سال 1393 تا 1403: {total_injuries_all}
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(count_html))

    add_injury_heatmap_legend(map_zanjan)

    map_zanjan.save("atlas_zanjan_Jaddeh_Injury_HeatMap_Circle_AllYears.html")