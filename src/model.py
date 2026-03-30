import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AttendanceAnomalyDetector:
    def __init__(self, contamination=0.1):
        """
        contamination: The proportion of outliers in the data set. 
        0.1 = 10% expected anomalies (can be tuned via UI).
        """
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42
        )
        self.scaler = StandardScaler()

    def fit_predict(self, df_processed):
        """
        Fits the model and returns a boolean series of anomalies.
        Expects numerical features only.
        """
        # Define features for training
        features = [
            'login_minutes', 
            'logout_minutes', 
            'total_work_minutes', 
            'day_of_week', 
            'is_weekend', 
            'login_deviation', 
            'work_duration_deviation'
        ]
        
        # Select all department-related dummy columns
        dept_cols = [col for col in df_processed.columns if col.startswith('dept_')]
        features.extend(dept_cols)
        
        X = df_processed[features].values
        X_scaled = self.scaler.fit_transform(X)
        
        # 1 means inlier, -1 means outlier
        preds = self.model.fit_predict(X_scaled)
        
        # Convert -1 to 1 (anomaly), 1 to 0 (normal)
        return (preds == -1).astype(int)

    def explain_anomaly(self, row, normal_stats):
        """
        Generates a human-readable reason for why this row might be an anomaly.
        Compare features against the median/mean.
        """
        reasons = []
        
        # 1. Late Login Check
        if row['login_deviation'] > normal_stats['login_deviation'] + 60: # 1 hour late
            reasons.append("Logged in significantly later than usual.")
        elif row['login_deviation'] < normal_stats['login_deviation'] - 60:
            reasons.append("Logged in significantly earlier than usual.")
            
        # 2. Work Duration Check
        if row['total_work_minutes'] < normal_stats['total_work_minutes'] - 120:
            reasons.append("Significantly shorter work duration than normal behavior.")
        elif row['total_work_minutes'] > normal_stats['total_work_minutes'] + 180: # 3 hour extra
            reasons.append("Excessive work duration / Overtime.")
            
        # 3. Weekend Work
        if row['is_weekend'] == 1:
            reasons.append("Worked on a weekend (irregular pattern).")
            
        if not reasons:
            return "Irregular combination of activities detected."
            
        return " | ".join(reasons)
