import pandas as pd
import geopandas as gpd

def load_accident_data(excel_path):
    df = pd.read_excel(excel_path)
    return df

def load_geo_data(shp_path):
    gdf = gpd.read_file(shp_path)
    return gdf