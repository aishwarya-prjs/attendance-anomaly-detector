import pandas as pd
import numpy as np
from datetime import datetime

class AttendanceProcessor:
    def __init__(self, standard_login_hour=9, standard_work_hours=9):
        self.standard_login_minutes = standard_login_hour * 60
        self.standard_work_minutes = standard_work_hours * 60

    def time_to_minutes(self, time_str):
        """Converts HH:MM:SS format to minutes since midnight."""
        try:
            h, m, s = map(int, time_str.split(':'))
            return h * 60 + m + s/60
        except:
            return np.nan

    def process(self, df):
        """Complete processing pipeline."""
        df = df.copy()
        
        # 1. Convert date/time
        df['date'] = pd.to_datetime(df['date'])
        df['login_minutes'] = df['login_time'].apply(self.time_to_minutes)
        df['logout_minutes'] = df['logout_time'].apply(self.time_to_minutes)
        
        # 2. Drop missing rows (initial ones + failed time conversions)
        df.dropna(inplace=True)
        
        # 3. Handle cases where logout is past midnight
        # If logout < login, assume it's the next day
        df.loc[df['logout_minutes'] < df['login_minutes'], 'logout_minutes'] += 24 * 60
        
        # 4. Core Features
        df['total_work_minutes'] = df['logout_minutes'] - df['login_minutes']
        df['day_of_week'] = df['date'].dt.dayofweek # 0=Mon, 6=Sun
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        # 5. Deviation Features
        df['login_deviation'] = df['login_minutes'] - self.standard_login_minutes
        df['work_duration_deviation'] = df['total_work_minutes'] - self.standard_work_minutes
        
        # 6. Categorical Encoding
        # We'll return dummy variables separately for training but keep the original for display
        df_encoded = pd.get_dummies(df, columns=['department'], prefix='dept')
        
        return df, df_encoded

if __name__ == "__main__":
    # Test loading
    test_df = pd.read_csv('/home/vk-linux/Desktop/attendance/data/attendance_sample.csv')
    processor = AttendanceProcessor()
    raw_df, processed_df = processor.process(test_df)
    print("Features extracted successfully!")
    print(processed_df.head())
