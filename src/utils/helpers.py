# Utility functions for data generation
import uuid
import random
from datetime import datetime, timedelta, date
from typing import List, Tuple
import numpy as np

def generate_uuid() -> str:
    """Generate a UUID v4 string for IDs"""
    return str(uuid.uuid4())

def generate_gid_like_id() -> str:
    """Generate an ID similar to Asana's GID format (numeric string)"""
    return str(random.randint(1000000000000000, 9999999999999999))

def generate_email(first_name: str, last_name: str, domain: str) -> str:
    """Generate realistic email from name and domain"""
    # Common patterns: firstname.lastname@domain, flastname@domain, firstnamelastname@domain
    patterns = [
        f"{first_name.lower()}.{last_name.lower()}@{domain}",
        f"{first_name[0].lower()}{last_name.lower()}@{domain}",
        f"{first_name.lower()}{last_name.lower()}@{domain}"
    ]
    return random.choice(patterns)

def generate_random_datetime(start_date: datetime, end_date: datetime) -> datetime:
    """Generate random datetime between two dates"""
    time_delta = end_date - start_date
    random_seconds = random.randint(0, int(time_delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

def generate_weighted_due_date(created_at: datetime, today: date) -> Tuple[date, bool]:
    """
    Generate due dates with realistic distribution:
    25% within 1 week
    40% within 1 month
    20% 1-3 months out
    10% no due date (returns None)
    5% overdue
    """
    rand = random.random()
    created_date = created_at.date()
    
    if rand < 0.10:  # 10% no due date
        return None, False
    elif rand < 0.15:  # 5% overdue
        days_overdue = random.randint(1, 90)
        due_date = created_date - timedelta(days=days_overdue)
        return due_date, True
    elif rand < 0.40:  # 25% within 1 week
        days_ahead = random.randint(1, 7)
        due_date = created_date + timedelta(days=days_ahead)
        return due_date, False
    elif rand < 0.80:  # 40% within 1 month
        days_ahead = random.randint(1, 30)
        due_date = created_date + timedelta(days=days_ahead)
        return due_date, False
    else:  # 20% 1-3 months out
        days_ahead = random.randint(30, 90)
        due_date = created_date + timedelta(days=days_ahead)
        return due_date, False

def avoid_weekend(target_date: date, avoid_weekend: bool = True) -> date:
    """If avoid_weekend is True and target_date is weekend, move to Monday"""
    if not avoid_weekend:
        return target_date
    
    weekday = target_date.weekday()
    if weekday == 5:  # Saturday
        return target_date + timedelta(days=2)
    elif weekday == 6:  # Sunday
        return target_date + timedelta(days=1)
    return target_date

def generate_creation_time(base_date: datetime) -> datetime:
    """
    Generate creation timestamps with realistic distribution:
    Higher creation rates Mon-Wed, lower Thu-Fri
    """
    # Add random hours and minutes within the day
    hours = random.randint(8, 18)  # Business hours 8 AM - 6 PM
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)
    
    # Adjust probability based on day of week
    weekday = base_date.weekday()
    if weekday in [4, 5]:  # Thursday (4), Friday (5)
        if random.random() < 0.4:  # 40% chance to move to earlier day
            days_back = random.randint(1, 3)
            base_date = base_date - timedelta(days=days_back)
    
    return base_date.replace(hour=hours, minute=minutes, second=seconds)

def generate_completion_time(created_at: datetime, completion_probability: float = 0.7) -> Tuple[datetime, bool]:
    """
    Generate completion timestamp with log-normal distribution.
    Returns (completed_at timestamp, is_completed boolean)
    """
    if random.random() > completion_probability:
        return None, False
    
    # Log-normal distribution for cycle time (in days)
    # Median of 3 days, most tasks 1-14 days
    shape = 0.8
    scale = 1.0
    cycle_days = np.random.lognormal(scale, shape)
    cycle_days = min(cycle_days, 14)  # Cap at 14 days
    cycle_days = max(cycle_days, 1)   # At least 1 day
    
    completed_at = created_at + timedelta(days=cycle_days)
    return completed_at, True

def is_realistic_date_range(created_at: datetime, completed_at: datetime) -> bool:
    """Validate that task was completed after creation"""
    return completed_at > created_at

def get_weekday_name(date_obj: date) -> str:
    """Get the weekday name of a date"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[date_obj.weekday()]

def generate_time_range(start_date: datetime, days_range: int = 180) -> Tuple[datetime, datetime]:
    """Generate a realistic time range for company operations"""
    end_date = start_date + timedelta(days=days_range)
    return start_date, end_date

def distribution_probability(rand_val: float, thresholds: List[Tuple[float, str]]) -> str:
    """
    Select value based on probability distribution
    thresholds: List of (cumulative_probability, value) tuples
    """
    for threshold, value in thresholds:
        if rand_val <= threshold:
            return value
    return thresholds[-1][1]

def ensure_temporal_consistency(created_at: datetime, due_date: date, completed_at: datetime) -> bool:
    """Ensure temporal consistency of task dates"""
    if due_date is not None:
        if completed_at is not None:
            return created_at.date() <= due_date and due_date <= completed_at.date()
        else:
            return created_at.date() <= due_date
    elif completed_at is not None:
        return created_at <= completed_at
    return True

def batch_insert_values(records: List, batch_size: int = 1000):
    """Generator to batch records for efficient insertion"""
    for i in range(0, len(records), batch_size):
        yield records[i:i + batch_size]
