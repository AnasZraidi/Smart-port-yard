import pandas as pd

def load_data():
    df = pd.read_csv('containers.csv')
    df['arrival_time'] = pd.to_datetime(df['arrival_time'])
    return df

def analyze(df):
    print("=" * 50)
    print("   SMART PORT YARD — OPERATIONS REPORT")
    print("=" * 50)

    print(f"\n TOTAL CONTAINERS IN YARD: {len(df)}")

    print(f"\n STATUS BREAKDOWN:")
    for status, count in df['status'].value_counts().items():
        print(f"   {status}: {count}")

    print(f"\n DWELL TIME ALERTS (over 48 hours):")
    delayed = df[df['dwell_time_hours'] > 48].sort_values('dwell_time_hours', ascending=False)
    if len(delayed) == 0:
        print("   No containers exceeding 48 hours.")
    else:
        for _, row in delayed.iterrows():
            print(f"   {row['container_id']} | {row['carrier']} | {row['dwell_time_hours']}h | {row['status']}")

    print(f"\n CARRIER PERFORMANCE:")
    carrier_stats = df.groupby('carrier').agg(
        total=('container_id', 'count'),
        avg_dwell=('dwell_time_hours', 'mean'),
        delayed=('status', lambda x: (x == 'delayed').sum())
    ).round(1)
    print(carrier_stats.to_string())

    print(f"\n YARD OCCUPANCY BY ROW:")
    row_counts = df['yard_row'].value_counts().sort_index()
    for row, count in row_counts.items():
        bar = '█' * count
        print(f"   Row {row}: {bar} ({count})")

    print(f"\n AVG DWELL TIME: {df['dwell_time_hours'].mean():.1f} hours")
    print(f" MAX DWELL TIME: {df['dwell_time_hours'].max():.1f} hours")
    print(f" TOTAL WEIGHT IN YARD: {df['weight_tons'].sum():.1f} tons")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    df = load_data()
    analyze(df)