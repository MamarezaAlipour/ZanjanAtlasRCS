from data_loader import load_accident_data, load_geo_data
from map_utils import create_map, add_geojson, add_fire_markers, add_logo, add_count_box, add_paygah_markers

def generate_all_years_fire_map(excel_path, logo_path, shp_path):
    df = load_accident_data(excel_path)
    df_fire = df[df['نوع حادثه'] == 'آتش سوزی جنگل و مرتع']
    gdf = load_geo_data(shp_path)
    incident_type = df_fire['نوع حادثه'].unique()[0] if not df_fire.empty else ''
    map_zanjan = create_map([36.6769, 48.4850], 8)
    add_geojson(map_zanjan, gdf)
    add_fire_markers(map_zanjan, df_fire)
    add_logo(map_zanjan, logo_path)
    add_count_box(map_zanjan, incident_type, len(df_fire), "از سال 1393 تا 1403")
    add_paygah_markers(map_zanjan, "./Data/paygah.xlsx", "./Data/paygah_icon.png")
    map_zanjan.save("atlas_zanjan_Fire_AllYears.html")