import csv
from datetime import datetime
from typing import List
from models import MarketDataPoint

def load_market_data(filepath: str) -> List[MarketDataPoint]:
    data = []

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
            price_value = float(row['Close'])
            
            point = MarketDataPoint(
                timestamp=dt,
                symbol=row['Symbol'],
                price=price_value
            )
            data.append(point)
            
    return data