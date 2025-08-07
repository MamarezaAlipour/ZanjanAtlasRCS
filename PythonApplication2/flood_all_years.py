from data_loader import load_accident_data, load_geo_data
from map_utils import create_map, add_geojson, add_flood_markers, add_logo, add_count_box, add_paygah_markers

def generate_all_years_flood_map(excel_path, logo_path, shp_path):
    df = load_accident_data(excel_path)
    df_flood = df[df['نوع حادثه'] == 'سیل و آبگرفتگی']
    gdf = load_geo_data(shp_path)
    incident_type = df_flood['نوع حادثه'].unique()[0] if not df_flood.empty else ''
    map_zanjan = create_map([36.6769, 48.4850], 8)
    add_geojson(map_zanjan, gdf)
    add_flood_markers(map_zanjan, df_flood)
    add_logo(map_zanjan, logo_path)
    add_count_box(map_zanjan, incident_type, len(df_flood), "از سال 1393 تا 1403")
    add_paygah_markers(map_zanjan, "./paygah.xlsx", "./paygah_icon.png")
    map_zanjan.save("atlas_zanjan_Flood_AllYears.html")