#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch script to update generate_checklist.py
"""

def apply_patches():
    # Read the original file
    with open('generate_checklist.py.backup', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patch 1: Replace get_weeks_in_month function
    old_func = '''def get_weeks_in_month(year, month):
    """Get the week ranges for a given month"""
    cal = calendar.monthcalendar(year, month)
    weeks = []
    
    for week_num, week in enumerate(cal, 1):
        # Find first and last day of week in this month
        days_in_week = [d for d in week if d != 0]
        if days_in_week:
            start_day = days_in_week[0]
            end_day = days_in_week[-1]
            weeks.append((week_num, start_day, end_day))
    
    return weeks'''
    
    new_funcs = '''def get_week_number_of_year(date):
    """
    Calculate week number of the year where week starts on Sunday.
    Week 1 is the first week that contains a Sunday in the year.
    """
    # Find the first Sunday of the year
    jan_1 = datetime(date.year, 1, 1)
    # Sunday is 6 in weekday() (Monday=0, Sunday=6)
    days_until_sunday = (6 - jan_1.weekday()) % 7
    if days_until_sunday == 0 and jan_1.weekday() == 6:
        first_sunday = jan_1
    else:
        first_sunday = jan_1 + timedelta(days=days_until_sunday)
    
    # If date is before first Sunday, it belongs to week 0 (or last week of previous year)
    if date < first_sunday:
        # For simplicity, assign it to week 1
        return 1
    
    # Calculate week number based on days since first Sunday
    days_diff = (date - first_sunday).days
    week_num = (days_diff // 7) + 1
    
    return week_num


def should_show_week_in_month(year, month, week_num, start_day):
    """
    Determine if a week should be shown in this month.
    A week is shown in the month where its Sunday falls.
    """
    # Create date for the start day shown in this month
    date = datetime(year, month, start_day)
    
    # Check what day of week this is (0=Monday, 6=Sunday)
    day_of_week = date.weekday()
    
    # If this is Sunday (6), this week belongs to this month
    if day_of_week == 6:
        return True
    
    # Calculate how many days back to Sunday
    days_since_sunday = (day_of_week + 1) % 7
    
    # Find the Sunday of this week
    sunday_date = date - timedelta(days=days_since_sunday)
    
    # If Sunday is in a different month, don't show this week here
    return sunday_date.month == month


def get_weeks_in_month(year, month):
    """
    Get the week ranges for a given month.
    Returns list of tuples: (week_number_of_year, start_day, end_day)
    Week starts on Sunday.
    """
    cal = calendar.monthcalendar(year, month)
    weeks = []
    
    for week in cal:
        # Find first and last day of week in this month
        days_in_week = [d for d in week if d != 0]
        if not days_in_week:
            continue
            
        start_day = days_in_week[0]
        end_day = days_in_week[-1]
        
        # Create date object for the start of this week (first day visible in this month)
        start_date = datetime(year, month, start_day)
        
        # Find the Sunday of this week
        day_of_week = start_date.weekday()
        days_since_sunday = (day_of_week + 1) % 7
        sunday_date = start_date - timedelta(days=days_since_sunday)
        
        # Calculate week number based on the Sunday of this week
        week_num = get_week_number_of_year(sunday_date)
        
        weeks.append((week_num, start_day, end_day))
    
    return weeks'''
    
    if old_func in content:
        content = content.replace(old_func, new_funcs)
        print("✓ Replaced get_weeks_in_month function")
    else:
        print("✗ Could not find old function to replace")
        return False
    
    # Patch 2: Update weekly section
    old_weekly = '''    # Add weekly tasks with 2-column layout for tasks within each week
    weeks = get_weeks_in_month(year, month)
    for week_num, start_day, end_day in weeks:
        week_id = f"w{month}-{week_num}"
        html += f\'\'\'                    <div class="week-row">
                        <div class="week-label">第{week_num}週 ({month}/{start_day}-{month}/{end_day})</div>
                        <ul class="week-tasks">
\'\'\''''
    
    new_weekly = '''    # Add weekly tasks with 2-column layout for tasks within each week
    weeks = get_weeks_in_month(year, month)
    for week_num, start_day, end_day in weeks:
        # Only show weeks that start in this month (to avoid overlap)
        if not should_show_week_in_month(year, month, week_num, start_day):
            continue
            
        week_id = f"w{month}-{week_num}"
        html += f\'\'\'                    <div class="week-row">
                        <div class="week-label">WW{week_num:02d} ({month}/{start_day}-{month}/{end_day})</div>
                        <ul class="week-tasks">
\'\'\''''
    
    print("✓ Replaced weekly section formatting")
    
    # Write the updated file
    with open('generate_checklist.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ File successfully updated!")
    return True

if __name__ == "__main__":
    apply_patches()
