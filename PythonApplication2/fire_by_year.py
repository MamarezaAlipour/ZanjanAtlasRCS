from data_loader import load_accident_data, load_geo_data
from map_utils import create_map, add_geojson, add_fire_markers, add_logo, add_count_box, add_paygah_markers

def generate_yearly_fire_maps(excel_path, logo_path, shp_path):
    df = load_accident_data(excel_path)
    df_fire = df[df['نوع حادثه'] == 'آتش سوزی جنگل و مرتع']
    df_fire['سال'] = df_fire['تاريخ وقوع حادثه'].astype(str).str[:4]
    gdf = load_geo_data(shp_path)
    incident_type = df_fire['نوع حادثه'].unique()[0] if not df_fire.empty else ''
    for year in range(1393, 1404):
        map_zanjan = create_map([36.6769, 48.4850], 8)
        add_geojson(map_zanjan, gdf)
        df_year = df_fire[df_fire['سال'] == str(year)]
        add_fire_markers(map_zanjan, df_year)
        add_logo(map_zanjan, logo_path)
        add_count_box(map_zanjan, incident_type, len(df_year), f"سال {year}")
        add_paygah_markers(map_zanjan, "./paygah.xlsx", "./paygah_icon.png")
        map_zanjan.save(f"atlas_zanjan_Fire_{year}.html")