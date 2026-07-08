import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta
RAW_PATH = Path("data/raw")
RAW_PATH.mkdir(parents=True, exist_ok=True)
random.seed(42)
customers = []
for i in range(1, 1001):
   customers.append({
       "customer_id": i,
       "customer_name": f"Customer {i}",
       "email": f"customer{i}@example.com",
       "industry": random.choice(["Healthcare", "Finance", "Manufacturing", "Retail", "Technology"]),
       "company_size": random.choice(["Small", "Mid-Market", "Enterprise"]),
       "country": random.choice(["US", "Canada", "UK", "Germany", "India"]),
       "signup_date": (datetime.today() - timedelta(days=random.randint(30, 1000))).date(),
       "plan_type": random.choice(["Free", "Pro", "Business", "Enterprise"]),
       "is_active": random.choice([True, True, True, False])
   })
pd.DataFrame(customers).to_csv(RAW_PATH / "customers.csv", index=False)
events = []
for i in range(1, 10000):
   events.append({
       "event_id": i,
       "customer_id": random.randint(1, 1000),
       "event_type": random.choice(["login", "dashboard_view", "api_call", "report_export", "model_run"]),
       "event_timestamp": datetime.today() - timedelta(days=random.randint(0, 180)),
       "session_duration_seconds": random.randint(10, 7200)
   })
pd.DataFrame(events).to_csv(RAW_PATH / "product_events.csv", index=False)
tickets = []
for i in range(1, 3000):
   tickets.append({
       "ticket_id": i,
       "customer_id": random.randint(1, 1000),
       "priority": random.choice(["Low", "Medium", "High", "Critical"]),
       "status": random.choice(["Open", "Resolved", "Pending", "Escalated"]),
       "category": random.choice(["Billing", "Product Bug", "Access", "Performance", "Data Quality"]),
       "created_at": datetime.today() - timedelta(days=random.randint(0, 180)),
       "resolution_hours": random.randint(1, 200)
   })
pd.DataFrame(tickets).to_csv(RAW_PATH / "support_tickets.csv", index=False)
invoices = []
for i in range(1, 5000):
   invoices.append({
       "invoice_id": i,
       "customer_id": random.randint(1, 1000),
       "invoice_date": datetime.today() - timedelta(days=random.randint(0, 365)),
       "amount": round(random.uniform(100, 25000), 2),
       "payment_status": random.choice(["Paid", "Pending", "Failed"])
   })
pd.DataFrame(invoices).to_csv(RAW_PATH / "invoices.csv", index=False)
print("Sample enterprise SaaS data generated successfully.")