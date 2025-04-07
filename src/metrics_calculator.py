import pandas as pd

def calculate_tables(df):
    df['c_date'] = pd.to_datetime(df['c_date'])

    max_date = df['c_date'].max()
    last_5_days = df[df['c_date'] >= max_date - pd.Timedelta(days=3)]

    # Tabla 1: Últimos 5 días
    tabla1 = (
        last_5_days.groupby('c_date')[['orders', 'revenue']]
        .sum()
        .reset_index()
        .sort_values('c_date')
        .to_dict(orient='records')
    )

    # Tabla 2: Por campaña
    tabla2 = (
        df.groupby('campaign_name')[['mark_spent', 'orders', 'revenue']]
        .sum()
        .reset_index()
        .to_dict(orient='records')
    )

    # Tabla 3: Por categoría
    tabla3 = (
        df.groupby('category')[['mark_spent', 'orders', 'revenue']]
        .sum()
        .reset_index()
        .to_dict(orient='records')
    )

    return {
        'tabla1': tabla1,
        'tabla2': tabla2,
        'tabla3': tabla3
    }
