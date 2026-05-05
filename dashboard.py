import pandas as pd
import json

def load_data():
    df = pd.read_csv('containers.csv')
    return df

def generate_dashboard(df):
    # Prepare data for charts
    status_counts = df['status'].value_counts().to_dict()
    carrier_avg_dwell = df.groupby('carrier')['dwell_time_hours'].mean().round(1).to_dict()
    row_counts = df['yard_row'].value_counts().sort_index().to_dict()
    
    # Critical containers
    critical = df[df['dwell_time_hours'] > 72].sort_values('dwell_time_hours', ascending=False).head(10)
    critical_html = ""
    for _, row in critical.iterrows():
        critical_html += f"""
        <tr>
            <td>{row['container_id']}</td>
            <td>{row['carrier']}</td>
            <td>{row['origin']}</td>
            <td>{row['destination']}</td>
            <td class="alert">{row['dwell_time_hours']}h</td>
            <td><span class="badge {row['status']}">{row['status']}</span></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Port Yard Intelligence System</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #0a0e1a; color: #e0e6f0; }}
        header {{ background: #0d1b2a; padding: 20px 40px; border-bottom: 2px solid #1e3a5f; display: flex; justify-content: space-between; align-items: center; }}
        header h1 {{ color: #4fc3f7; font-size: 1.5rem; letter-spacing: 2px; }}
        header span {{ color: #78909c; font-size: 0.85rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; padding: 30px 40px 0; }}
        .card {{ background: #0d1b2a; border: 1px solid #1e3a5f; border-radius: 10px; padding: 20px; }}
        .card h3 {{ color: #78909c; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px; }}
        .card .number {{ font-size: 2.5rem; font-weight: bold; color: #4fc3f7; }}
        .card .label {{ font-size: 0.8rem; color: #546e7a; margin-top: 5px; }}
        .card.alert-card .number {{ color: #ef5350; }}
        .card.warn-card .number {{ color: #ffa726; }}
        .card.ok-card .number {{ color: #66bb6a; }}
        .charts {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; padding: 20px 40px; }}
        .chart-card {{ background: #0d1b2a; border: 1px solid #1e3a5f; border-radius: 10px; padding: 20px; }}
        .chart-card h3 {{ color: #4fc3f7; font-size: 0.9rem; margin-bottom: 15px; letter-spacing: 1px; }}
        .table-section {{ padding: 0 40px 40px; }}
        .table-section h2 {{ color: #4fc3f7; margin-bottom: 15px; font-size: 1rem; letter-spacing: 1px; }}
        table {{ width: 100%; border-collapse: collapse; background: #0d1b2a; border-radius: 10px; overflow: hidden; }}
        th {{ background: #1e3a5f; padding: 12px 15px; text-align: left; font-size: 0.75rem; letter-spacing: 1px; color: #90caf9; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #1e3a5f; font-size: 0.85rem; }}
        tr:hover {{ background: #1a2a3a; }}
        .alert {{ color: #ef5350; font-weight: bold; }}
        .badge {{ padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }}
        .badge.delayed {{ background: #b71c1c; color: #ffcdd2; }}
        .badge.waiting {{ background: #e65100; color: #ffe0b2; }}
        .badge.processing {{ background: #1565c0; color: #bbdefb; }}
        .badge.ready {{ background: #1b5e20; color: #c8e6c9; }}
        .footer {{ text-align: center; padding: 20px; color: #37474f; font-size: 0.75rem; }}
    </style>
</head>
<body>
    <header>
        <h1>⚓ SMART PORT YARD INTELLIGENCE SYSTEM</h1>
        <span>Port of Casablanca · Live Operations Dashboard</span>
    </header>

    <div class="grid">
        <div class="card">
            <h3>Total Containers</h3>
            <div class="number">{len(df)}</div>
            <div class="label">In yard</div>
        </div>
        <div class="card alert-card">
            <h3>Delayed</h3>
            <div class="number">{status_counts.get('delayed', 0)}</div>
            <div class="label">Require immediate action</div>
        </div>
        <div class="card warn-card">
            <h3>Dwell &gt; 48h</h3>
            <div class="number">{len(df[df['dwell_time_hours'] > 48])}</div>
            <div class="label">Exceeding threshold</div>
        </div>
        <div class="card ok-card">
            <h3>Ready</h3>
            <div class="number">{status_counts.get('ready', 0)}</div>
            <div class="label">Cleared for pickup</div>
        </div>
    </div>

    <div class="charts">
        <div class="chart-card">
            <h3>CONTAINER STATUS</h3>
            <canvas id="statusChart"></canvas>
        </div>
        <div class="chart-card">
            <h3>AVG DWELL TIME BY CARRIER (hours)</h3>
            <canvas id="carrierChart"></canvas>
        </div>
        <div class="chart-card">
            <h3>YARD ROW OCCUPANCY</h3>
            <canvas id="rowChart"></canvas>
        </div>
    </div>

    <div class="table-section">
        <h2>⚠ CRITICAL ALERTS — CONTAINERS EXCEEDING 72 HOURS</h2>
        <table>
            <thead>
                <tr>
                    <th>Container ID</th>
                    <th>Carrier</th>
                    <th>Origin</th>
                    <th>Destination</th>
                    <th>Dwell Time</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {critical_html}
            </tbody>
        </table>
    </div>

    <div class="footer">
        Smart Port Yard Intelligence System · Built by Anas Zraidi · Port of Casablanca
    </div>

    <script>
        Chart.defaults.color = '#78909c';
        Chart.defaults.borderColor = '#1e3a5f';

        new Chart(document.getElementById('statusChart'), {{
            type: 'doughnut',
            data: {{
                labels: {list(status_counts.keys())},
                datasets: [{{ 
                    data: {list(status_counts.values())},
                    backgroundColor: ['#ef5350', '#ffa726', '#42a5f5', '#66bb6a'],
                    borderWidth: 0
                }}]
            }},
            options: {{ plugins: {{ legend: {{ position: 'bottom' }} }} }}
        }});

        new Chart(document.getElementById('carrierChart'), {{
            type: 'bar',
            data: {{
                labels: {list(carrier_avg_dwell.keys())},
                datasets: [{{ 
                    data: {list(carrier_avg_dwell.values())},
                    backgroundColor: '#4fc3f7',
                    borderRadius: 5
                }}]
            }},
            options: {{ plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});

        new Chart(document.getElementById('rowChart'), {{
            type: 'bar',
            data: {{
                labels: {list(row_counts.keys())},
                datasets: [{{ 
                    data: {list(row_counts.values())},
                    backgroundColor: '#26a69a',
                    borderRadius: 5
                }}]
            }},
            options: {{ plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});
    </script>
</body>
</html>"""

    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Dashboard generated: dashboard.html")

if __name__ == "__main__":
    df = load_data()
    generate_dashboard(df)