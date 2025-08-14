import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# حجم تردد تخمینی برای محورهای اصلی (واحد: هزار خودرو در سال)
TRAFFIC_DATA = {
    "زنجان-قزوین": 2500,  # پرترددترین محور
    "زنجان-تبریز": 1800,
    "زنجان-بیجار": 1200,
    "زنجان-خرمدره-ابهر": 900,
    "زنجان-ماهنشان": 600,
    "زنجان-سلطانیه-همدان": 800,
    "زنجان-دندی-تکاب": 500,
    "زنجان-طارم": 400
}

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

def calculate_accident_traffic_ratio(excel_path, n_clusters=8, output_excel_path=None):
    df = pd.read_excel(excel_path)
    # فقط حوادث جاده‌ای
    df = df[df['نوع حادثه'] == 'جاده ای']
    df = df.dropna(subset=['عرض جغرافیایی(N)', 'طول جغرافیایی(E)'])
    df['طول جغرافیایی(E)'] = pd.to_numeric(df['طول جغرافیایی(E)'], errors='coerce')
    df['عرض جغرافیایی(N)'] = pd.to_numeric(df['عرض جغرافیایی(N)'], errors='coerce')
    df = df.dropna(subset=['طول جغرافیایی(E)', 'عرض جغرافیایی(N)'])

    coords = df[['عرض جغرافیایی(N)', 'طول جغرافیایی(E)']].values
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['خوشه'] = kmeans.fit_predict(coords)

    centers = kmeans.cluster_centers_
    accident_table = df.groupby('خوشه').agg({
        'تاريخ وقوع حادثه': 'count',
        'تعداد کل مصدومین در حادثه /نفر': 'sum',
        'مجموع کل فوتی': 'sum'
    }).reset_index()

    accident_table['محور تخمینی'] = accident_table['خوشه'].apply(
        lambda i: find_nearest_road(centers[i][0], centers[i][1])
    )
    accident_table['حجم تردد سالانه'] = accident_table['محور تخمینی'].map(TRAFFIC_DATA)
    accident_table['نسبت تصادف به تردد'] = (
        accident_table['تاريخ وقوع حادثه'] / accident_table['حجم تردد سالانه'] * 1000
    ).round(2)

    accident_table.rename(columns={
        'تاريخ وقوع حادثه': 'تعداد تصادف',
        'تعداد کل مصدومین در حادثه /نفر': 'تعداد مصدومین',
        'مجموع کل فوتی': 'تعداد فوتی‌ها'
    }, inplace=True)

    # مرتب‌سازی بر اساس نسبت تصادف به تردد (خطرناک‌ترین محور)
    accident_table = accident_table.sort_values('نسبت تصادف به تردد', ascending=False)

    print("جدول نسبت تصادف به حجم تردد (شاخص خطر واقعی محورها):")
    print(accident_table[['محور تخمینی', 'تعداد تصادف', 'حجم تردد سالانه', 
                         'نسبت تصادف به تردد', 'تعداد مصدومین', 'تعداد فوتی‌ها']].to_markdown(index=False))

    if output_excel_path:
        accident_table.to_excel(output_excel_path, index=False)

    return accident_table