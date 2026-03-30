import pytest
import pandas as pd
import numpy as np
from src.model import AttendanceAnomalyDetector

def test_model_fit_predict():
    detector = AttendanceAnomalyDetector(contamination=0.1)
    # Create dummy processed data
    # Standard: 9-to-6 Mon-Fri
    data = {
        'login_minutes': [540]*90 + [720]*10, # 90 normal, 10 late (12 PM)
        'logout_minutes': [1080]*90 + [1200]*10, # 90 normal, 10 end at 8 PM
        'total_work_minutes': [540]*90 + [480]*10,
        'day_of_week': [0]*100, # All Monday
        'is_weekend': [0]*100,
        'login_deviation': [0]*90 + [180]*10,
        'work_duration_deviation': [0]*90 + [-60]*10,
        'dept_IT': [1]*100
    }
    df = pd.DataFrame(data)
    anomalies = detector.fit_predict(df)
    
    # 1. Output should be numpy array of 0s and 1s
    assert len(anomalies) == 100
    assert set(np.unique(anomalies)).issubset({0, 1})
    
    # 2. At least some anomalies should be found
    assert sum(anomalies) > 0

def test_explain_anomaly_short_duration():
    detector = AttendanceAnomalyDetector()
    normal_stats = {'login_deviation': 0, 'total_work_minutes': 540} # 9 hour avg
    
    # Case: Normal login but logout in 2 hours
    anomaly_row = {
        'login_deviation': 0,
        'total_work_minutes': 120, # 2 hours
        'is_weekend': 0
    }
    reason = detector.explain_anomaly(anomaly_row, normal_stats)
    assert "Significantly shorter work duration than normal behavior." in reason

def test_explain_anomaly_late_login():
    detector = AttendanceAnomalyDetector()
    normal_stats = {'login_deviation': 0, 'total_work_minutes': 540} 
    
    # Case: Login 3 hours late
    anomaly_row = {
        'login_deviation': 180, 
        'total_work_minutes': 360, # 6 hours
        'is_weekend': 0
    }
    reason = detector.explain_anomaly(anomaly_row, normal_stats)
    assert "Logged in significantly later than usual." in reason

def test_explain_anomaly_weekend():
    detector = AttendanceAnomalyDetector()
    normal_stats = {'login_deviation': 0, 'total_work_minutes': 540} 
    
    # Case: Weekend work
    anomaly_row = {
        'login_deviation': 0, 
        'total_work_minutes': 540,
        'is_weekend': 1
    }
    reason = detector.explain_anomaly(anomaly_row, normal_stats)
    assert "Worked on a weekend (irregular pattern)." in reason

def test_contamination_parameter():
    # A higher contamination should pick up more anomalies
    data = {
        'login_minutes': [540]*90 + [720]*10,
        'logout_minutes': [1080]*90 + [1200]*10,
        'total_work_minutes': [540]*90 + [480]*10,
        'day_of_week': [0, 1, 2, 3, 4] * 20, 
        'is_weekend': [0]*100,
        'login_deviation': [0]*90 + [180]*10,
        'work_duration_deviation': [0]*90 + [-60]*10,
        'dept_IT': [1]*100
    }
    df = pd.DataFrame(data)
    
    detector_low = AttendanceAnomalyDetector(contamination=0.01)
    detector_high = AttendanceAnomalyDetector(contamination=0.15)
    
    anomalies_low = detector_low.fit_predict(df)
    anomalies_high = detector_high.fit_predict(df)
    
    # 15% should flag more anomalies than 1%
    assert sum(anomalies_high) > sum(anomalies_low)

def test_explain_multiple_reasons():
    detector = AttendanceAnomalyDetector()
    normal_stats = {'login_deviation': 0, 'total_work_minutes': 540} 
    
    # Case: Both late login AND short duration
    anomaly_row = {
        'login_deviation': 300, # 5 hours late
        'total_work_minutes': 120, # 2 hour work
        'is_weekend': 0
    }
    reason = detector.explain_anomaly(anomaly_row, normal_stats)
    assert "|" in reason # Should combine reasons with pipe
    assert "Logged in significantly later than usual." in reason
    assert "Significantly shorter work duration than normal behavior." in reason
