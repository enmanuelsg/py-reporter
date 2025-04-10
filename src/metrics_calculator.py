import pandas as pd

def calculate_tables(df):
    df['c_date'] = pd.to_datetime(df['c_date'])
    max_date = df['c_date'].max()
    last_5_days = df[df['c_date'] >= max_date - pd.Timedelta(days=3)]

    table1 = (
        last_5_days.groupby('c_date')[['orders', 'revenue']]
        .sum()
        .reset_index()
        .sort_values('c_date')
        .to_dict(orient='records')
    )

    table2 = (
        df.groupby('campaign_name')[['mark_spent', 'orders', 'revenue']]
        .sum()
        .reset_index()
        .to_dict(orient='records')
    )

    table3 = (
        df.groupby('category')[['mark_spent', 'orders', 'revenue']]
        .sum()
        .reset_index()
        .to_dict(orient='records')
    )

    return {
        'tabla1': table1,
        'tabla2': table2,
        'tabla3': table3
    }
