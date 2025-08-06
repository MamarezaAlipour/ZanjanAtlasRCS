import pandas as pd
import geopandas as gpd
import folium
from folium import Element
from map_utils import add_value_circles

def generate_all_years_injury_circle_map(excel_path, logo_path, shp_path):
    df = pd.read_excel(excel_path)
    df = df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)', 'تعداد کل مصدومین در حادثه /نفر'])
    df['تعداد کل مصدومین در حادثه /نفر'] = pd.to_numeric(df['تعداد کل مصدومین در حادثه /نفر'], errors='coerce').fillna(0)

    gdf = gpd.read_file(shp_path)
    map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
    folium.GeoJson(gdf).add_to(map_zanjan)

    add_value_circles(
        map_zanjan,
        df,
        "تعداد کل مصدومین در حادثه /نفر",
        value_label="مصدومین",
        extra_popup_columns=["نوع حادثه", "شرح حادثه", "تاريخ وقوع حادثه"]
    )

    logo_html = f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
        <img src="{logo_path}" alt="logo" width="85">
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(logo_html))

    total_injury = int(df["تعداد کل مصدومین در حادثه /نفر"].sum())
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
        مجموع کل مصدومین در همه حوادث از سال 1393 تا 1403: {total_injury}
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(count_html))

    map_zanjan.save("atlas_zanjan_Injury_Circle_AllYears.html")