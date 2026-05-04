from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from groq import Groq

import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_data():
    df = pd.read_csv('containers.csv')
    return df

def build_summary(df):
    total = len(df)
    delayed = len(df[df['status'] == 'delayed'])
    avg_dwell = round(df['dwell_time_hours'].mean(), 1)
    max_dwell = df['dwell_time_hours'].max()
    worst_container = df.loc[df['dwell_time_hours'].idxmax(), 'container_id']
    worst_carrier = df.loc[df['dwell_time_hours'].idxmax(), 'carrier']
    total_weight = round(df['weight_tons'].sum(), 1)
    overdue = df[df['dwell_time_hours'] > 48]
    overdue_count = len(overdue)

    carrier_delays = df.groupby('carrier')['status'].apply(
        lambda x: (x == 'delayed').sum()
    ).sort_values(ascending=False)
    worst_carrier_name = carrier_delays.idxmax()

    summary = f"""
    Port Yard Status Summary:
    - Total containers in yard: {total}
    - Delayed containers: {delayed}
    - Containers exceeding 48h dwell time: {overdue_count}
    - Average dwell time: {avg_dwell} hours
    - Maximum dwell time: {max_dwell} hours (Container {worst_container}, {worst_carrier})
    - Total cargo weight: {total_weight} tons
    - Carrier with most delays: {worst_carrier_name}
    """
    return summary

def generate_report(summary):
    prompt = f"""
    You are an AI operations assistant for a port yard management system.
    Based on the following port yard data, write a professional operations report 
    for the port manager. Be specific, highlight urgent issues, and recommend actions.
    
    {summary}
    
    Write the report in a clear, professional tone. Include:
    1. Executive Summary
    2. Critical Alerts
    3. Carrier Performance Notes
    4. Recommended Actions
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    df = load_data()
    summary = build_summary(df)
    print("Generating AI report...")
    report = generate_report(summary)
    print("\n" + "=" * 50)
    print("   AI-GENERATED PORT OPERATIONS REPORT")
    print("=" * 50)
    print(report)
    
    with open("operations_report.txt", "w") as f:
        f.write(report)
    print("\nReport saved to operations_report.txt")