from data_loader import load_accident_data, load_geo_data
from map_utils import create_map, add_geojson, add_logo, add_count_box, add_value_circles, add_paygah_markers

def generate_all_years_injury_map(excel_path, logo_path, shp_path):
    df = load_accident_data(excel_path)
    gdf = load_geo_data(shp_path)
    map_zanjan = create_map([36.6769, 48.4850], 8)
    add_geojson(map_zanjan, gdf)
    add_value_circles(map_zanjan, df, "تعداد کل مصدومین در حادثه /نفر", value_label="مصدومین", extra_popup_columns=["شرح حادثه", "تاريخ وقوع حادثه"])
    add_logo(map_zanjan, logo_path)
    total_injuries = df["تعداد کل مصدومین در حادثه /نفر"].sum()
    add_count_box(map_zanjan, "مصدومین", int(total_injuries), "از سال 1393 تا 1403")
    # فرض بر این است که paygah.xlsx و paygah_icon.png در مسیر پروژه هستند
    add_paygah_markers(map_zanjan, "./paygah.xlsx", "./paygah_icon.png")
    map_zanjan.save("atlas_zanjan_Injury_AllYears.html")