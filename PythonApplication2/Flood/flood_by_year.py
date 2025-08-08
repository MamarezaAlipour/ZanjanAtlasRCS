from data_loader import load_accident_data
import geopandas as gpd
from map_utils import create_map, add_geojson, add_flood_markers, add_logo, add_count_box, add_paygah_markers

def generate_yearly_flood_maps(excel_path, logo_path, shp_path):
    df = load_accident_data(excel_path)
    df_flood = df[df['نوع حادثه'] == 'سیل و آبگرفتگی']
    df_flood['سال'] = df_flood['تاريخ وقوع حادثه'].astype(str).str[:4]
    gdf = gpd.read_file(shp_path)
    incident_type = df_flood['نوع حادثه'].unique()[0] if not df_flood.empty else ''
    for year in range(1393, 1404):
        map_zanjan = create_map([36.6769, 48.4850], 8)
        add_geojson(map_zanjan, gdf)
        df_year = df_flood[df_flood['سال'] == str(year)]
        add_flood_markers(map_zanjan, df_year)
        add_logo(map_zanjan, logo_path)
        add_count_box(map_zanjan, incident_type, len(df_year), f"سال {year}")
        # فرض بر این است که paygah.xlsx و paygah_icon.png در مسیر پروژه هستند
        add_paygah_markers(map_zanjan, "./Data/paygah.xlsx", "./Data/paygah_icon.png")
        map_zanjan.save(f"atlas_zanjan_Flood_{year}.html")