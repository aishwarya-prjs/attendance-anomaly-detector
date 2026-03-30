import pytest
import pandas as pd
import numpy as np
from src.processing import AttendanceProcessor

def test_time_to_minutes():
    processor = AttendanceProcessor()
    # Base cases
    assert processor.time_to_minutes("09:00:00") == 540
    assert processor.time_to_minutes("17:30:00") == 1050
    assert processor.time_to_minutes("00:00:00") == 0
    # Floating point seconds
    assert processor.time_to_minutes("01:01:30") == 60 + 1 + 0.5
    # Error handling
    assert np.isnan(processor.time_to_minutes("invalid"))

def test_process_pipeline_calculations():
    processor = AttendanceProcessor(standard_login_hour=9)
    data = {
        'employee_id': ['EMP1'],
        'login_time': ['09:00:00'],
        'logout_time': ['18:00:00'],
        'date': ['2026-01-05'], # Mon
        'department': ['IT']
    }
    df = pd.DataFrame(data)
    _, df_processed = processor.process(df)
    
    assert df_processed.iloc[0]['total_work_minutes'] == 540 # 9 hours
    assert df_processed.iloc[0]['login_deviation'] == 0 # On time
    assert df_processed.iloc[0]['is_weekend'] == 0 # Monday

def test_cross_midnight_logout():
    processor = AttendanceProcessor()
    # Login at 10 PM (1320 min), Logout at 2 AM (120 min)
    data = {
        'employee_id': ['EMP1'],
        'login_time': ['22:00:00'],
        'logout_time': ['02:00:00'],
        'date': ['2026-01-05'],
        'department': ['Security']
    }
    df = pd.DataFrame(data)
    _, df_processed = processor.process(df)
    
    # 4 hours shift = 240 minutes
    assert df_processed.iloc[0]['total_work_minutes'] == 240
    # In my logic, logout_minutes becomes 120 + 1440 = 1560
    assert df_processed.iloc[0]['logout_minutes'] == 1560

def test_weekend_flag():
    processor = AttendanceProcessor()
    data = {
        'employee_id': ['EMP1', 'EMP1'],
        'login_time': ['09:00:00', '09:00:00'],
        'logout_time': ['17:00:00', '17:00:00'],
        'date': ['2026-01-10', '2026-01-09'], # Sat, Fri
        'department': ['IT', 'IT']
    }
    df = pd.DataFrame(data)
    _, df_processed = processor.process(df)
    
    assert df_processed.iloc[0]['is_weekend'] == 1 # Saturday
    assert df_processed.iloc[1]['is_weekend'] == 0 # Friday

def test_handle_missing_data():
    processor = AttendanceProcessor()
    data = {
        'employee_id': ['EMP1', 'EMP2'],
        'login_time': ['09:00:00', np.nan], # Missing login
        'logout_time': ['17:00:00', '18:00:00'],
        'date': ['2026-01-05', '2026-01-05'],
        'department': ['IT', 'HR']
    }
    df = pd.DataFrame(data)
    _, df_processed = processor.process(df)
    
    # Should only have 1 valid row after dropping NaNs
    assert len(df_processed) == 1
    assert df_processed.iloc[0]['employee_id'] == 'EMP1'

def test_unknown_time_strings():
    processor = AttendanceProcessor()
    data = {
        'employee_id': ['EMP1'],
        'login_time': ['Not-A-Time'], 
        'logout_time': ['17:00:00'],
        'date': ['2026-01-05'],
        'department': ['IT']
    }
    df = pd.DataFrame(data)
    # The current time_to_minutes returns NaN for errors
    # The process method drops NaNs
    _, df_processed = processor.process(df)
    assert len(df_processed) == 0

def test_department_one_hot_encoding():
    processor = AttendanceProcessor()
    data = {
        'employee_id': ['E1', 'E2'],
        'login_time': ['09:00:00', '10:00:00'],
        'logout_time': ['17:00:00', '18:00:00'],
        'date': ['2026-01-05', '2026-01-05'],
        'department': ['Engineering', 'Marketing']
    }
    df = pd.DataFrame(data)
    _, df_processed = processor.process(df)
    
    # Check if department columns were created
    assert 'dept_Engineering' in df_processed.columns
    assert 'dept_Marketing' in df_processed.columns
    assert df_processed.iloc[0]['dept_Engineering'] == 1
    assert df_processed.iloc[1]['dept_Engineering'] == 0
