from data_loader import load_accident_data, load_geo_data
from map_utils import create_map, add_geojson, add_markers, add_logo, add_count_box

def generate_all_years_map(excel_path, logo_path, shp_path):
    df = load_accident_data(excel_path)
    df_road = df[df['نوع حادثه'] == 'جاده ای']
    gdf = load_geo_data(shp_path)
    incident_type = df_road['نوع حادثه'].unique()[0] if not df_road.empty else ''
    map_zanjan = create_map([36.6769, 48.4850], 8)
    add_geojson(map_zanjan, gdf)
    add_markers(map_zanjan, df_road)
    add_logo(map_zanjan, logo_path)
    add_count_box(map_zanjan, incident_type, len(df_road), "از سال 1393 تا 1403")
    map_zanjan.save("atlas_zanjan_Jaddeh_AllYears.html")