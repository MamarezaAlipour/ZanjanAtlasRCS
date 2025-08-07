from data_loader import load_accident_data, load_geo_data
from map_utils import create_map, add_geojson, add_snow_markers, add_logo, add_count_box, add_paygah_markers

def generate_all_years_snow_map(excel_path, logo_path, shp_path):
    df = load_accident_data(excel_path)
    df_snow = df[df['نوع حادثه'] == 'برف و کولاک']
    gdf = load_geo_data(shp_path)
    incident_type = df_snow['نوع حادثه'].unique()[0] if not df_snow.empty else ''
    map_zanjan = create_map([36.6769, 48.4850], 8)
    add_geojson(map_zanjan, gdf)
    add_snow_markers(map_zanjan, df_snow)
    add_logo(map_zanjan, logo_path)
    add_count_box(map_zanjan, incident_type, len(df_snow), "از سال 1393 تا 1403")
    add_paygah_markers(map_zanjan, "./paygah.xlsx", "./paygah_icon.png")
    map_zanjan.save("atlas_zanjan_Snow_AllYears.html")