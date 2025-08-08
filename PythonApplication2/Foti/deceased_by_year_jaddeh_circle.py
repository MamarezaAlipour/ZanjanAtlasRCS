import pandas as pd
import geopandas as gpd
import folium
from folium import Element
from .deceased_all_years_jaddeh_circle import add_deceased_circles_black
from map_utils import add_paygah_markers

def generate_yearly_deceased_jaddeh_circle_maps(excel_path, logo_path, shp_path):
    df = pd.read_excel(excel_path)
    df = df[df['نوع حادثه'] == 'جاده ای']
    df = df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)', 'مجموع کل فوتی'])
    df['مجموع کل فوتی'] = pd.to_numeric(df['مجموع کل فوتی'], errors='coerce').fillna(0)
    df['سال'] = df['تاريخ وقوع حادثه'].astype(str).str[:4]

    gdf = gpd.read_file(shp_path)
    for year in range(1393, 1403):
        map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
        folium.GeoJson(gdf).add_to(map_zanjan)
        df_year = df[df['سال'] == str(year)]
        add_deceased_circles_black(
            map_zanjan,
            df_year,
            "مجموع کل فوتی",
            value_label="فوتی‌ها",
            extra_popup_columns=["شرح حادثه", "تاريخ وقوع حادثه"]
        )

        # Adding paygah markers
        add_paygah_markers(map_zanjan, "./Data/paygah.xlsx", "./Data/paygah_icon.png")

        logo_html = f"""
        <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
            <img src="{logo_path}" alt="logo" width="85">
        </div>
        """
        map_zanjan.get_root().html.add_child(Element(logo_html))

        total_deceased_year = int(df_year["مجموع کل فوتی"].sum())
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
                    font-size: 18px; color: #222; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
            مجموع کل فوتی حوادث جاده‌ای سال {year}: {total_deceased_year}
        </div>
        """
        map_zanjan.get_root().html.add_child(Element(count_html))

        map_zanjan.save(f"atlas_zanjan_Deceased_Jaddeh_Circle_{year}.html")