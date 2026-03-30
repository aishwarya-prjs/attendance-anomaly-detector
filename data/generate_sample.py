import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_attendance_data(n_employees=10, n_days=30):
    departments = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance']
    start_date = datetime(2026, 1, 1)
    
    data = []
    
    for emp_id in range(101, 101 + n_employees):
        dept = random.choice(departments)
        
        for day_idx in range(n_days):
            current_date = start_date + timedelta(days=day_idx)
            
            # Skip weekends? No, let's keep them and mark them as potential anomalies if they work irregularly.
            # But let's mainly simulate workdays.
            if current_date.weekday() >= 5:
                if random.random() > 0.05: # 5% chance to work on weekend
                    continue
                
            # Normal working hours: 09:00 - 18:00 (approx)
            login_hour = random.gauss(9, 0.5) # Mean 9AM, Std Dev 30 mins
            work_duration = random.gauss(9, 1) # Mean 9 hours, Std Dev 1 hour
            
            # Add occasional anomalies
            if random.random() < 0.05: # 5% chance of anomaly
                anomaly_type = random.choice(['late', 'short', 'overtime', 'early_out'])
                if anomaly_type == 'late':
                    login_hour = random.uniform(13, 15) # Afternoon login
                elif anomaly_type == 'short':
                    work_duration = random.uniform(2, 4) # Very short shift
                elif anomaly_type == 'overtime':
                    work_duration = random.uniform(12, 16) # Long shift
                elif anomaly_type == 'early_out':
                    work_duration = random.uniform(3, 5)

            logout_hour = login_hour + work_duration
            
            # Format times
            login_time = (datetime.min + timedelta(hours=login_hour)).strftime('%H:%M:%S')
            logout_time = (datetime.min + timedelta(hours=logout_hour)).strftime('%H:%M:%S')
            
            data.append({
                'employee_id': f'EMP{emp_id}',
                'login_time': login_time,
                'logout_time': logout_time,
                'date': current_date.strftime('%Y-%m-%d'),
                'department': dept
            })
            
    df = pd.DataFrame(data)
    df.to_csv('/home/vk-linux/Desktop/attendance/data/attendance_sample.csv', index=False)
    print("Sample attendance data generated at: data/attendance_sample.csv")

if __name__ == "__main__":
    generate_attendance_data()
