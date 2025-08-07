import geopandas as gpd

# خواندن Shapefile
shp_gdf = gpd.read_file("Export_Output_4.shp")

# افزودن به فایل GPKG (به عنوان یک لایه جدید)
shp_gdf.to_file("gadm41_IRN.gpkg", layer='export_output_3', driver="GPKG")