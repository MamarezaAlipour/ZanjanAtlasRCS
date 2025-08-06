import pandas as pd
import geopandas as gpd
import folium
from folium import Element

def generate_chain_accidents_map(excel_path, logo_path, shp_path):
    df = pd.read_excel(excel_path)
    # فقط تصادفات زنجیره‌ای
    chain_df = df[df['شرح حادثه'].str.contains('زنجیره', na=False)]
    chain_df = chain_df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)'])

    gdf = gpd.read_file(shp_path)
    map_zanjan = folium.Map(location=[36.6769, 48.4850], zoom_start=8)
    folium.GeoJson(gdf).add_to(map_zanjan)

    for _, row in chain_df.iterrows():
        popup_text = (
            f"<b>نوع حادثه:</b> {row['نوع حادثه']}<br>"
            f"<b>شرح حادثه:</b> {row['شرح حادثه']}<br>"
            f"<b>تاریخ وقوع:</b> {row['تاريخ وقوع حادثه']}<br>"
            f"<b>مصدومین:</b> {int(row['تعداد کل مصدومین در حادثه /نفر']) if pd.notnull(row['تعداد کل مصدومین در حادثه /نفر']) else '-'}<br>"
            f"<b>فوتی‌ها:</b> {int(row['مجموع کل فوتی']) if pd.notnull(row['مجموع کل فوتی']) else '-'}"
        )
        folium.Marker(
            location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
            popup=popup_text,
            icon=folium.Icon(color='darkpurple', icon='car', prefix='fa')
        ).add_to(map_zanjan)

    logo_html = f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
        <img src="{logo_path}" alt="logo" width="85">
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(logo_html))

    count = len(chain_df)
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
                font-size: 18px; color: #512da8; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        مجموع تصادفات زنجیره‌ای از سال 1393 تا 1403: {count}
    </div>
    """
    map_zanjan.get_root().html.add_child(Element(count_html))

    map_zanjan.save("atlas_zanjan_ChainAccidents_AllYears.html")