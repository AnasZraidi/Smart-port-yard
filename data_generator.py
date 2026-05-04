import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_containers(num_containers=50):
    containers = []
    
    statuses = ['waiting', 'processing', 'ready', 'delayed']
    sizes = ['20ft', '40ft', '40ft HC']
    origins = ['Shanghai', 'Rotterdam', 'Hamburg', 'Algeciras', 'Valencia', 'Marseille']
    destinations = ['Casablanca', 'Tangier', 'Agadir', 'Kenitra', 'Mohammedia']
    carriers = ['Maersk', 'MSC', 'CMA CGM', 'Hapag-Lloyd', 'Evergreen']
    yard_rows = ['A', 'B', 'C', 'D', 'E']

    for i in range(num_containers):
        arrival = datetime.now() - timedelta(hours=random.randint(1, 120))
        container = {
            'container_id': f"CONT{str(i+1).zfill(4)}",
            'size': random.choice(sizes),
            'origin': random.choice(origins),
            'destination': random.choice(destinations),
            'carrier': random.choice(carriers),
            'arrival_time': arrival,
            'dwell_time_hours': round((datetime.now() - arrival).total_seconds() / 3600, 1),
            'yard_row': random.choice(yard_rows),
            'yard_slot': random.randint(1, 20),
            'stack_level': random.randint(1, 4),
            'status': random.choice(statuses),
            'weight_tons': round(random.uniform(5, 28), 1)
        }
        containers.append(container)
    
    return pd.DataFrame(containers)

if __name__ == "__main__":
    df = generate_containers(50)
    df.to_csv('containers.csv', index=False)
    print(f"Generated {len(df)} containers")
    print(df.head())