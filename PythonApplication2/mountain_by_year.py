from data_loader import load_accident_data, load_geo_data
from map_utils import create_map, add_geojson, add_mountain_markers, add_logo, add_count_box

def generate_yearly_mountain_maps(excel_path, logo_path, shp_path):
    df = load_accident_data(excel_path)
    df_mountain = df[df['نوع حادثه'] == 'کوهستان']
    df_mountain['سال'] = df_mountain['تاريخ وقوع حادثه'].astype(str).str[:4]
    gdf = load_geo_data(shp_path)
    incident_type = df_mountain['نوع حادثه'].unique()[0] if not df_mountain.empty else ''
    for year in range(1393, 1404):
        map_zanjan = create_map([36.6769, 48.4850], 8)
        add_geojson(map_zanjan, gdf)
        df_year = df_mountain[df_mountain['سال'] == str(year)]
        add_mountain_markers(map_zanjan, df_year)
        add_logo(map_zanjan, logo_path)
        add_count_box(map_zanjan, incident_type, len(df_year), f"سال {year}")
        map_zanjan.save(f"atlas_zanjan_Mountain_{year}.html")