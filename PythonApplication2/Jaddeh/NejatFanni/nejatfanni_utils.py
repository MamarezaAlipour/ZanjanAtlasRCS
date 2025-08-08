import pandas as pd

def compute_nejatfani_count(df):
    # فقط حوادث جاده‌ای
    df = df[df['نوع حادثه'] == 'جاده ای'].copy()
    # اطمینان از عددی بودن
    df['ست سبک نجات'] = pd.to_numeric(df['ست سبک نجات'], errors='coerce').fillna(0)
    df['ست هیدرولیک نجات'] = pd.to_numeric(df['ست هیدرولیک نجات'], errors='coerce').fillna(0)
    # محاسبه تعداد نجات فنی طبق منطق
    def nejatfani_row(row):
        if row['ست سبک نجات'] > 0 and row['ست هیدرولیک نجات'] > 0:
            return int(row['ست سبک نجات'])  # اگر هر دو غیرصفر، مقدار ست سبک نجات
        elif row['ست سبک نجات'] > 0:
            return int(row['ست سبک نجات'])
        elif row['ست هیدرولیک نجات'] > 0:
            return int(row['ست هیدرولیک نجات'])
        else:
            return 0
    df['تعداد نجات فنی'] = df.apply(nejatfani_row, axis=1)
    # فقط ردیف‌هایی که نجات فنی دارند
    df = df[df['تعداد نجات فنی'] > 0]
    return df