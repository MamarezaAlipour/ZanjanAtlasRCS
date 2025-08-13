import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

# محورهای اصلی استان با مختصات تقریبی (عرض، طول)
ROADS = [
    {"name": "زنجان-قزوین", "lat": 36.5, "lon": 49.0},
    {"name": "زنجان-تبریز", "lat": 36.7, "lon": 47.8},
    {"name": "زنجان-بیجار", "lat": 36.4, "lon": 48.5},
    {"name": "زنجان-خرمدره-ابهر", "lat": 36.3, "lon": 49.2},
    {"name": "زنجان-ماهنشان", "lat": 36.6, "lon": 47.5},
    {"name": "زنجان-سلطانیه-همدان", "lat": 36.4, "lon": 48.8},
    {"name": "زنجان-دندی-تکاب", "lat": 36.8, "lon": 47.2},
    {"name": "زنجان-طارم", "lat": 36.9, "lon": 49.0}
]

def find_nearest_road(lat, lon):
    min_dist = float('inf')
    nearest = None
    for road in ROADS:
        dist = np.sqrt((lat - road["lat"])**2 + (lon - road["lon"])**2)
        if dist < min_dist:
            min_dist = dist
            nearest = road["name"]
    return nearest

def generate_statistical_table(excel_path, output_excel_path=None):
    df = pd.read_excel(excel_path)
    df['سال'] = df['تاريخ وقوع حادثه'].astype(str).str[:4]

    table = df.groupby('سال').agg({
        'تاريخ وقوع حادثه': 'count',
        'تعداد کل مصدومین در حادثه /نفر': 'sum',
        'مجموع کل فوتی': 'sum',
        'درمان سرپايي توسط جمعیت/نفر': 'sum',
        'مصدومين انتقالي توسط جمعیت/نفر': 'sum'
    }).reset_index()

    table.rename(columns={
        'سال': 'سال',
        'تاريخ وقوع حادثه': 'تعداد کل حوادث',
        'تعداد کل مصدومین در حادثه /نفر': 'مصدومین',
        'مجموع کل فوتی': 'فوتی‌ها',
        'درمان سرپايي توسط جمعیت/نفر': 'درمان سرپایی',
        'مصدومين انتقالي توسط جمعیت/نفر': 'مصدومین انتقالی'
    }, inplace=True)

    print(table.to_markdown(index=False))

    if output_excel_path:
        table.to_excel(output_excel_path, index=False)

    return table

def generate_incident_type_frequency_table(excel_path, output_excel_path=None):
    df = pd.read_excel(excel_path)
    df['سال'] = df['تاريخ وقوع حادثه'].astype(str).str[:4]
    df = df[df['سال'].isin([str(y) for y in range(1393, 1404)])]
    freq_table = df.groupby('نوع حادثه').size().reset_index(name='تعداد')
    freq_table = freq_table.sort_values('تعداد', ascending=False)
    total = freq_table['تعداد'].sum()
    freq_table['درصد از کل حوادث'] = (freq_table['تعداد'] / total * 100).round(2)

    print(freq_table.to_markdown(index=False))

    if output_excel_path:
        freq_table.to_excel(output_excel_path, index=False)

    return freq_table

def generate_hotspot_table(excel_path, output_excel_path=None):
    df = pd.read_excel(excel_path)
    # فرض بر این است که ستون "محور حادثه" یا "محل حادثه" وجود دارد
    # اگر نام ستون متفاوت است، آن را جایگزین کنید
    axis_col = None
    for col in df.columns:
        if 'محور' in col or 'محل' in col:
            axis_col = col
            break
    if axis_col is None:
        print("ستون محور یا محل حادثه در فایل وجود ندارد.")
        return None

    hotspot_table = df.groupby(axis_col).agg({
        'تاريخ وقوع حادثه': 'count',
        'تعداد کل مصدومین در حادثه /نفر': 'sum',
        'مجموع کل فوتی': 'sum'
    }).reset_index()

    hotspot_table.rename(columns={
        axis_col: 'محور یا منطقه',
        'تاريخ وقوع حادثه': 'تعداد حادثه',
        'تعداد کل مصدومین در حادثه /نفر': 'تعداد مصدومین',
        'مجموع کل فوتی': 'تعداد فوتی‌ها'
    }, inplace=True)

    hotspot_table = hotspot_table.sort_values('تعداد حادثه', ascending=False)

    print(hotspot_table.to_markdown(index=False))

    if output_excel_path:
        hotspot_table.to_excel(output_excel_path, index=False)

    return hotspot_table

def generate_geospatial_hotspot_table(excel_path, n_clusters=8, output_excel_path=None):
    df = pd.read_excel(excel_path)
    df = df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)'])
    df['طول جغرافیایی(E)'] = pd.to_numeric(df['طول جغرافیایی(E)'], errors='coerce')
    df['عرض جغرافیایی(N)'] = pd.to_numeric(df['عرض جغرافیایی(N)'], errors='coerce')
    df = df.dropna(subset=['طول جغرافیایی(E)', 'عرض جغرافیایی(N)'])

    coords = df[['عرض جغرافیایی(N)', 'طول جغرافیایی(E)']].values
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['خوشه'] = kmeans.fit_predict(coords)

    # مرکز هر خوشه را به عنوان نماینده محور/منطقه در جدول نمایش می‌دهیم
    centers = kmeans.cluster_centers_
    hotspot_table = df.groupby('خوشه').agg({
        'تاريخ وقوع حادثه': 'count',
        'تعداد کل مصدومین در حادثه /نفر': 'sum',
        'مجموع کل فوتی': 'sum'
    }).reset_index()
    hotspot_table['مرکز خوشه (عرض, طول)'] = hotspot_table['خوشه'].apply(lambda i: f"{centers[i][0]:.4f}, {centers[i][1]:.4f}")

    hotspot_table.rename(columns={
        'تاريخ وقوع حادثه': 'تعداد حادثه',
        'تعداد کل مصدومین در حادثه /نفر': 'تعداد مصدومین',
        'مجموع کل فوتی': 'تعداد فروت‌ها'
    }, inplace=True)

    hotspot_table = hotspot_table.sort_values('تعداد حادثه', ascending=False)

    print(hotspot_table[['مرکز خوشه (عرض, طول)', 'تعداد حادثه', 'تعداد مصدومین', 'تعداد فوتی‌ها']].to_markdown(index=False))

    if output_excel_path:
        hotspot_table.to_excel(output_excel_path, index=False)

    return hotspot_table

def generate_geospatial_hotspot_table_with_road(excel_path, n_clusters=8, output_excel_path=None):
    df = pd.read_excel(excel_path)
    df = df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)'])
    df['طول جغرافیایی(E)'] = pd.to_numeric(df['طول جغرافیایی(E)'], errors='coerce')
    df['عرض جغرافیایی(N)'] = pd.to_numeric(df['عرض جغرافیایی(N)'], errors='coerce')
    df = df.dropna(subset=['طول جغرافیایی(E)', 'عرض جغرافیایی(N)'])

    coords = df[['عرض جغرافیایی(N)', 'طول جغرافیایی(E)']].values
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['خوشه'] = kmeans.fit_predict(coords)

    centers = kmeans.cluster_centers_
    hotspot_table = df.groupby('خوشه').agg({
        'تاريخ وقوع حادثه': 'count',
        'تعداد کل مصدومین در حادثه /نفر': 'sum',
        'مجموع کل فوتی': 'sum'
    }).reset_index()
    hotspot_table['مرکز خوشه (عرض, طول)'] = hotspot_table['خوشه'].apply(lambda i: f"{centers[i][0]:.4f}, {centers[i][1]:.4f}")
    hotspot_table['محور تخمینی'] = hotspot_table['خوشه'].apply(lambda i: find_nearest_road(centers[i][0], centers[i][1]))

    hotspot_table.rename(columns={
        'تاريخ وقوع حادثه': 'تعداد حادثه',
        'تعداد کل مصدومین در حادثه /نفر': 'تعداد مصدومین',
        'مجموع کل فوتی': 'تعداد فوتی‌ها'
    }, inplace=True)

    hotspot_table = hotspot_table.sort_values('تعداد حادثه', ascending=False)

    print(hotspot_table[['محور تخمینی', 'مرکز خوشه (عرض, طول)', 'تعداد حادثه', 'تعداد مصدومین', 'تعداد فوتی‌ها']].to_markdown(index=False))

    if output_excel_path:
        hotspot_table.to_excel(output_excel_path, index=False)

    return hotspot_table