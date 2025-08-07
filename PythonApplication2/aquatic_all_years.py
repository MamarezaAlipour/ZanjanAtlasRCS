from data_loader import load_accident_data
from map_utils import create_map, add_geojson, add_logo, add_count_box, add_aquatic_markers, add_paygah_markers
import geopandas as gpd

def generate_all_years_aquatic_map(excel_path, logo_path, shp_path):
    df = load_accident_data(excel_path)
    df_aquatic = df[df['نوع حادثه'] == 'محیط های آبی']
    gdf = gpd.read_file(shp_path)  # خواندن فایل shp به جای gpkg
    incident_type = df_aquatic['نوع حادثه'].unique()[0] if not df_aquatic.empty else ''
    map_zanjan = create_map([36.6769, 48.4850], 8)
    add_geojson(map_zanjan, gdf)
    add_aquatic_markers(map_zanjan, df_aquatic)
    add_logo(map_zanjan, logo_path)
    add_count_box(map_zanjan, incident_type, len(df_aquatic), "از سال 1393 تا 1403")
    # افزودن نشانگرهای پایگاه
    add_paygah_markers(map_zanjan, "./paygah.xlsx", "./paygah_icon.png")
    map_zanjan.save("atlas_zanjan_Aquatic_AllYears.html")