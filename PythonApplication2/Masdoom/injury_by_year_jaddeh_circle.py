import pandas as pd
import geopandas as gpd
import folium
from folium import Element
from map_utils import add_value_circles, add_paygah_markers

def generate_yearly_injury_jaddeh_circle_maps(excel_path, logo_path, shp_path):
    df = pd.read_excel(excel_path)
    df_jaddeh = df[df['نوع حادثه'] == 'جاده ای']
    df_jaddeh = df_jaddeh.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)', 'تعداد کل مصدومین در حادثه /نفر'])
    df_jaddeh['تعداد کل مصدومین در حادثه /نفر'] = pd.to_numeric(df_jaddeh['تعداد کل مصدومین در حادثه /نفر'], errors='coerce').fillna(0)
    df_jaddeh['سال'] = df_jaddeh['تاريخ وقوع حادثه'].astype(str).str[:4]

    shp_gdf = gpd.read_file(shp_path)

    for year in range(1393, 1404):
        map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
        folium.GeoJson(shp_gdf, name="Shapefile Layer").add_to(map_zanjan)

        df_year = df_jaddeh[df_jaddeh['سال'] == str(year)]
        add_value_circles(
            map_zanjan,
            df_year,
            "تعداد کل مصدومین در حادثه /نفر",
            value_label="مصدومین",
            extra_popup_columns=["شرح حادثه", "تاريخ وقوع حادثه"]
        )

        logo_html = f"""
        <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
            <img src="{logo_path}" alt="logo" width="85">
        </div>
        """
        map_zanjan.get_root().html.add_child(Element(logo_html))

        total_injuries_year = int(df_year['تعداد کل مصدومین در حادثه /نفر'].sum())
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
            مجموع مصدومین جاده ای سال {year}: {total_injuries_year}
        </div>
        """
        map_zanjan.get_root().html.add_child(Element(count_html))

        from map_utils import add_paygah_markers

        # فرض بر این است که paygah.xlsx و paygah_icon.png در مسیر پروژه هستند
        add_paygah_markers(map_zanjan, "./Data/paygah.xlsx", "./Data/paygah_icon.png")

        map_zanjan.save(f"atlas_zanjan_Jaddeh_Injury_Circle_{year}.html")
