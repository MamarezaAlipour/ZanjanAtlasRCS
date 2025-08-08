import folium
from folium import Element
import pandas as pd

def create_map(center, zoom):
    return folium.Map(location=center, zoom_start=zoom)

def add_geojson(map_obj, gdf):
    folium.GeoJson(gdf).add_to(map_obj)

def add_markers(map_obj, df):
    for _, row in df.iterrows():
        popup_text = f"{row['شرح حادثه']}, {row['تاريخ وقوع حادثه']}"
        popup_html = f"""
        <style>
        @font-face {{
            font-family: 'BNazanin';
            src: url('Static/B-NAZANIN.TTF') format('truetype');
            font-weight: normal;
            font-style: normal;
        }}
        .nazanin-popup {{
            font-family: 'BNazanin', Tahoma, Arial, sans-serif !important;
            font-size: 16px;
            text-align: center;
        }}
        </style>
        <div class="nazanin-popup">{popup_text}</div>
        """
        folium.Marker(
            location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
            popup=folium.Popup(popup_html, max_width=350),
            icon=folium.Icon(color='blue')
        ).add_to(map_obj)

def add_logo(map_obj, logo_path):
    logo_html = f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index:9999;">
        <img src="{logo_path}" alt="logo" width="85">
    </div>
    """
    map_obj.get_root().html.add_child(Element(logo_html))

def add_count_box(map_obj, incident_type, count, year_text):
    count_html = f"""
    <style>
    @font-face {{
        font-family: 'BTitr';
        src: url('Static/BTitr.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    .titr-box {{
        font-family: 'BTitr', Tahoma, Arial, sans-serif !important;
    }}
    </style>
    <div class="titr-box" style="position: fixed; bottom: 20px; left: 20px; z-index:9999;
                background: rgba(255,255,255,0.9); border-radius: 8px; padding: 10px 18px;
                font-size: 18px; color: #d32f2f; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        تعداد حوادث {incident_type} {year_text}: {count}
    </div>
    """
    map_obj.get_root().html.add_child(Element(count_html))

def add_snow_markers(map_obj, df):
    for _, row in df.iterrows():
        popup_text = f"{row['شرح حادثه']}, {row['تاريخ وقوع حادثه']}"
        folium.Marker(
            location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
            popup=popup_text,
            icon=folium.Icon(color='lightblue', icon='snowflake', prefix='fa')
        ).add_to(map_obj)

def add_flood_markers(map_obj, df):
    for _, row in df.iterrows():
        popup_text = f"{row['شرح حادثه']}, {row['تاريخ وقوع حادثه']}"
        folium.Marker(
            location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
            popup=popup_text,
            icon=folium.Icon(color='green', icon='cloud-showers-water', prefix='fa')
        ).add_to(map_obj)

def add_mountain_markers(map_obj, df):
    for _, row in df.iterrows():
        popup_text = f"{row['شرح حادثه']}, {row['تاريخ وقوع حادثه']}"
        folium.Marker(
            location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
            popup=popup_text,
            icon=folium.Icon(color='orange', icon='mountain', prefix='fa')
        ).add_to(map_obj)

def add_fire_markers(map_obj, df):
    for _, row in df.iterrows():
        popup_text = f"{row['شرح حادثه']}, {row['تاريخ وقوع حادثه']}"
        folium.Marker(
            location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
            popup=popup_text,
            icon=folium.Icon(color='red', icon='fire', prefix='fa')
        ).add_to(map_obj)

def add_aquatic_markers(map_obj, df):
    for _, row in df.iterrows():
        popup_text = f"{row['شرح حادثه']}, {row['تاريخ وقوع حادثه']}"
        folium.Marker(
            location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
            popup=popup_text,
            icon=folium.Icon(color='cadetblue', icon='anchor', prefix='fa')
        ).add_to(map_obj)

# def add_injury_circles(map_obj, df, value_column):
#     for _, row in df.iterrows():
#         try:
#             value = float(row[value_column])
#         except (ValueError, TypeError):
#             value = 0
#         if value > 0:
#             popup_text = f"مصدومین: {int(value)}<br>شرح حادثه: {row['شرح حادثه']}<br>تاریخ وقوع: {row['تاريخ وقوع حادثه']}"
#             folium.Circle(
#                 location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
#                 radius=50 + value * 10,  # مقیاس شعاع بر اساس تعداد مصدومین
#                 color='crimson',
#                 fill=True,
#                 fill_color='crimson',
#                 fill_opacity=0.5,
#                 popup=popup_text
#             ).add_to(map_obj)

def add_value_circles(map_obj, df, value_column, value_label="مقدار", extra_popup_columns=None):
    """
    رسم دایره‌های متناسب با مقدار ستون عددی.
    - value_column: نام ستون عددی (مثلاً 'تعداد کل مصدومین در حادثه /نفر')
    - value_label: عنوان مقدار (مثلاً 'مصدومین' یا 'فوتی‌ها')
    - extra_popup_columns: لیست ستون‌هایی که می‌خواهید در پاپ‌آپ نمایش داده شوند (مثلاً ['شرح حادثه', 'تاريخ وقوع حادثه'])
    """
    if extra_popup_columns is None:
        extra_popup_columns = []
    for _, row in df.iterrows():
        try:
            value = float(row[value_column])
        except (ValueError, TypeError):
            value = 0
        if value > 0:
            popup_parts = [f"{value_label}: {int(value)}"]
            for col in extra_popup_columns:
                popup_parts.append(f"{col}: {row.get(col, '')}")
            popup_content = "<br>".join(popup_parts)
            popup_html = f"""
            <style>
            @font-face {{
                font-family: 'BNazanin';
                src: url('Static/B-NAZANIN.TTF') format('truetype');
                font-weight: normal;
                font-style: normal;
            }}
            .nazanin-popup {{
                font-family: 'BNazanin', Tahoma, Arial, sans-serif !important;
                font-size: 16px;
                text-align: center;
            }}
            </style>
            <div class="nazanin-popup">{popup_content}</div>
            """
            folium.Circle(
                location=[row['عرض جغرافیایی(N)'], row['طول جغرافیایی(E)']],
                radius=50 + value * 10,
                color='crimson',
                fill=True,
                fill_color='crimson',
                fill_opacity=0.5,
                popup=folium.Popup(popup_html, max_width=350)
            ).add_to(map_obj)

def add_legend(map_obj):
    legend_html = """
    <div style="position: fixed; bottom: 20px; right: 20px; z-index:9999;
                background: rgba(255,255,255,0.95); border-radius: 8px; padding: 12px 18px;
                font-size: 15px; color: #222; box-shadow: 0 2px 8px rgba(0,0,0,0.12); min-width: 220px;">
        <b>راهنمای نقشه</b><hr style="margin:4px 0 8px 0;">
        <div style="margin-bottom:6px;"><i class="fa fa-map-marker" style="color:blue"></i> جاده‌ای</div>
        <div style="margin-bottom:6px;"><i class="fa fa-snowflake-o" style="color:lightblue"></i> برف و کولاک</div>
        <div style="margin-bottom:6px;"><i class="fa fa-cloud" style="color:green"></i> سیل و آبگرفتگی</div>
        <div style="margin-bottom:6px;"><i class="fa fa-mountain" style="color:orange"></i> کوهستان</div>
        <div style="margin-bottom:6px;"><i class="fa fa-fire" style="color:red"></i> آتش‌سوزی جنگل و مرتع</div>
        <div style="margin-bottom:6px;"><i class="fa fa-anchor" style="color:cadetblue"></i> محیط‌های آبی</div>
        <div style="margin-bottom:6px;"><span style="display:inline-block;width:18px;height:18px;background:crimson;border-radius:50%;margin-right:4px;vertical-align:middle;"></span> دایره: تعداد مصدومین</div>
        <div style="margin-bottom:2px;"><span style="display:inline-block;width:18px;height:18px;background:linear-gradient(90deg,blue, lime, yellow, red);border-radius:4px;margin-right:4px;vertical-align:middle;"></span> ابر رنگی: تراکم مصدومین</div>
    </div>
    """
    map_obj.get_root().html.add_child(Element(legend_html))

def add_injury_heatmap_legend(map_obj):
    legend_html = """
    <div style="position: fixed; bottom: 20px; right: 20px; z-index:9999;
                background: rgba(255,255,255,0.95); border-radius: 8px; padding: 12px 18px;
                font-size: 15px; color: #222; box-shadow: 0 2px 8px rgba(0,0,0,0.12); min-width: 220px;">
        <b>راهنمای ابر رنگی مصدومین</b><hr style="margin:4px 0 8px 0;">
        <div style="margin-bottom:6px;">
            <span style="display:inline-block;width:24px;height:16px;
                background:linear-gradient(90deg,blue,lime,yellow,red);
                border-radius:4px;margin-right:6px;vertical-align:middle;"></span>
            <span>رنگ آبی: مصدومیت کم</span>
        </div>
        <div style="margin-bottom:6px;">
            <span style="display:inline-block;width:24px;height:16px;
                background:linear-gradient(90deg,lime,yellow,red);
                border-radius:4px;margin-right:6px;vertical-align:middle;"></span>
            <span>رنگ سبز و زرد: مصدومیت متوسط</span>
        </div>
        <div>
            <span style="display:inline-block;width:24px;height:16px;
                background:linear-gradient(90deg,yellow,red);
                border-radius:4px;margin-right:6px;vertical-align:middle;"></span>
            <span>رنگ قرمز: مصدومیت زیاد</span>
        </div>
    </div>
    """
    map_obj.get_root().html.add_child(Element(legend_html))

def add_paygah_markers(map_obj, paygah_path, icon_path):
    df = pd.read_excel(paygah_path)
    # فرض: ستون‌های 'N', 'E', 'نام پایگاه امداد و نجات'
    for _, row in df.iterrows():
        lat = row['N'] if 'N' in row else row['عرض جغرافیایی(N)']
        lon = row['E'] if 'E' in row else row['طول جغرافیایی(E)']
        name = row['نام پایگاه امداد و نجات']
        if pd.notnull(lat) and pd.notnull(lon) and pd.notnull(name):
            icon = folium.CustomIcon(
                icon_image=icon_path,
                icon_size=(40, 40),
                icon_anchor=(20, 20)
            )
            popup_html = f"""
            <style>
            @font-face {{
                font-family: 'BNazanin';
                src: url('Static/B-NAZANIN.TTF') format('truetype');
                font-weight: normal;
                font-style: normal;
            }}
            .nazanin-popup {{
                font-family: 'BNazanin', Tahoma, Arial, sans-serif !important;
                font-size: 16px;
                text-align: center;
            }}
            </style>
            <div class="nazanin-popup" style="min-width:200px;white-space:nowrap;">{name}</div>
            """
            folium.Marker(
                location=[float(lat), float(lon)],
                icon=icon,
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(map_obj)