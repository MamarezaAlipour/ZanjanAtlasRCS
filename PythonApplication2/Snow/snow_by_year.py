from data_loader import load_accident_data, load_geo_data
from map_utils import create_map, add_geojson, add_snow_markers, add_logo, add_count_box, add_paygah_markers

def generate_yearly_snow_maps(excel_path, logo_path, shp_path):
    df = load_accident_data(excel_path)
    df_snow = df[df['نوع حادثه'] == 'برف و کولاک']
    df_snow['سال'] = df_snow['تاريخ وقوع حادثه'].astype(str).str[:4]
    gdf = load_geo_data(shp_path)
    incident_type = df_snow['نوع حادثه'].unique()[0] if not df_snow.empty else ''
    for year in range(1393, 1404):
        map_zanjan = create_map([36.6769, 48.4850], 8)
        add_geojson(map_zanjan, gdf)
        df_year = df_snow[df_snow['سال'] == str(year)]
        add_snow_markers(map_zanjan, df_year)
        add_logo(map_zanjan, logo_path)
        add_count_box(map_zanjan, incident_type, len(df_year), f"سال {year}")
        
        # فرض بر این است که paygah.xlsx و paygah_icon.png در مسیر پروژه هستند
        add_paygah_markers(map_zanjan, "./Data/paygah.xlsx", "./Data/paygah_icon.png")
        
        map_zanjan.save(f"atlas_zanjan_Snow_{year}.html")