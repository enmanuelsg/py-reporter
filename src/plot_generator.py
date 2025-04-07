import pandas as pd
import matplotlib.pyplot as plt


def generate_plots_inline(df):
    df['c_date'] = pd.to_datetime(df['c_date'])

    # Plot 1: Daily Revenue
    daily = df.groupby('c_date')['revenue'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(daily['c_date'], daily['revenue'], marker='o')
    ax1.set_title('Daily Sum of Revenue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Revenue')
    ax1.tick_params(axis='x', rotation=90)
    ax1.grid(True)

    # Plot 2: Revenue Distribution Pie Chart
    revenue_by_category = df.groupby('category')['revenue'].sum()
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ax2.pie(
        revenue_by_category,
        labels=revenue_by_category.index,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 8}
    )
    ax2.set_title('Revenue Distribution by Category', fontsize=10)
    ax2.axis('equal')

    return fig1, fig2
