import pandas as pd
import geopandas as gpd
import folium
from folium import Element
from nejatfanni_utils import compute_nejatfani_count
from map_utils import add_paygah_markers

def generate_yearly_nejatfanni_circle_maps(nejatfanni_path, logo_path, shp_path):
    df = pd.read_excel(nejatfanni_path)
    df = compute_nejatfani_count(df)
    df['سال'] = df['تاريخ وقوع حادثه'].astype(str).str[:4]
    gdf = gpd.read_file(shp_path)
    for year in range(1393, 1404):
        map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
        folium.GeoJson(gdf).add_to(map_zanjan)
        df_year = df[df['سال'] == str(year)]
        for _, row in df_year.iterrows():
            popup_text = f"تعداد نجات فنی: {row['تعداد نجات فنی']}<br>شرح حادثه: {row['شرح حادثه']}<br>تاریخ وقوع: {row['تاريخ وقوع حادثه']}"
            folium.Circle(
                location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
                radius=50 + row['تعداد نجات فنی'] * 10,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.5,
                popup=popup_text
            ).add_to(map_zanjan)

        logo_html = f"""
        <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
            <img src="{logo_path}" alt="logo" width="85">
        </div>
        """
        map_zanjan.get_root().html.add_child(Element(logo_html))

        total_nejat_year = int(df_year['تعداد نجات فنی'].sum())
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
                    font-size: 18px; color: #1976d2; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
            مجموع رهاسازی در حوادث جاده‌ای سال {year}: {total_nejat_year}
        </div>
        """
        map_zanjan.get_root().html.add_child(Element(count_html))

        # Adding paygah markers to the map
        add_paygah_markers(map_zanjan, "./paygah.xlsx", "./paygah_icon.png")

        map_zanjan.save(f"atlas_zanjan_NejatFanni_Circle_{year}.html")