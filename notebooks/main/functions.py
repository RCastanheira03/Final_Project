import re
import pandas as pd
from datetime import datetime, timedelta


def convert_decimal_to_hhmmss(decimal_hours):
    # Handle missing or invalid values gracefully
    try:
        decimal_hours = float(decimal_hours)
    except (ValueError, TypeError):
        return None
    
    hours = int(decimal_hours)
    minutes = int((decimal_hours - hours) * 60)
    seconds = int(round(((decimal_hours - hours) * 60 - minutes) * 60))
    
    # Handle rounding that pushes minutes or seconds over 60
    if seconds == 60:
        seconds = 0
        minutes += 1
    if minutes == 60:
        minutes = 0
        hours += 1
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"



def normalize_time_string(time_str):
    try:
        # Split hours and minutes
        parts = str(time_str).split(':')
        if len(parts) < 2:
            return None  # Invalid format
        
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2]) if len(parts) > 2 else 0
        
        # Normalize overflows using total minutes
        total_minutes = hours * 60 + minutes + seconds / 60
        norm_hours = int(total_minutes // 60)
        norm_minutes = int(total_minutes % 60)
        norm_seconds = int(round((total_minutes * 60) % 60))
        
        # Handle rounding overflow
        if norm_seconds == 60:
            norm_seconds = 0
            norm_minutes += 1
        if norm_minutes == 60:
            norm_minutes = 0
            norm_hours += 1

        return f"{norm_hours:02d}:{norm_minutes:02d}:{norm_seconds:02d}"
    except Exception:
        return None


import re

def convert_hm_to_hhmmss(duration_str):
    try:
        # Clean input (strip spaces, lowercase)
        s = str(duration_str).strip().lower()
        
        # Use a flexible regex: capture numbers before 'h' and 'm'
        match = re.search(r'(\d+)\s*h\s*(\d+)\s*m', s)
        if not match:
            return None
        
        hours = int(match.group(1))
        minutes = int(match.group(2))
        
        # Normalize minutes overflow
        total_minutes = hours * 60 + minutes
        norm_hours = total_minutes // 60
        norm_minutes = total_minutes % 60
        
        return f"{norm_hours:02d}:{norm_minutes:02d}:00"
    except Exception:
        return None


def detect_outliers_iqr(group):
    Q1 = group['price'].quantile(0.25)
    Q3 = group['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return group[(group['price'] < lower_bound) | (group['price'] > upper_bound)]