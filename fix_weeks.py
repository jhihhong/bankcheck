#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix the week date display in generate_checklist.py
"""

def fix_file():
    # Read the file
    with open('generate_checklist.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find and replace the get_weeks_in_month function
    in_function = False
    function_start = -1
    function_end = -1
    indent_level = 0
    
    for i, line in enumerate(lines):
        if 'def get_weeks_in_month(year, month):' in line:
            in_function = True
            function_start = i
            continue
        
        if in_function:
            # Check for next function definition (ends current function)
            if line.startswith('def ') and not line.startswith('    '):
                function_end = i
                break
    
    if function_start >= 0 and function_end >= 0:
        # New function implementation
        new_function = '''def get_weeks_in_month(year, month):
    """Get the week ranges for a given month with full date display"""
    cal = calendar.monthcalendar(year, month)
    weeks = []
    
    for week_num, week in enumerate(cal, 1):
        # Find first and last day of week in this month
        days_in_week = [d for d in week if d != 0]
        if days_in_week:
            first_day = days_in_week[0]
            last_day = days_in_week[-1]
            
            # Create actual date objects
            start_date = datetime(year, month, first_day)
            end_date = datetime(year, month, last_day)
            
            # Check if this week starts before first day of month (previous month)
            start_weekday = start_date.weekday()  # Monday=0, Sunday=6
            if first_day == 1 and start_weekday > 0:
                # This week actually started in previous month
                actual_start = start_date - timedelta(days=start_weekday)
            else:
                actual_start = start_date
            
            # Check if this week extends beyond last day of month (next month)
            end_weekday = end_date.weekday()
            last_day_of_month = calendar.monthrange(year, month)[1]
            if last_day == last_day_of_month and end_weekday < 6:
                # This week extends to next month
                actual_end = end_date + timedelta(days=(6 - end_weekday))
            else:
                actual_end = end_date
            
            weeks.append((
                week_num, 
                actual_start.month, 
                actual_start.day,
                actual_end.month,
                actual_end.day
            ))
    
    return weeks

'''
        
        # Replace the function
        lines = lines[:function_start] + [new_function] + lines[function_end:]
        print(f"✓ Replaced function from line {function_start+1} to {function_end}")
    else:
        print("✗ Could not find function boundaries")
        return False
    
    # Now find and replace the for loop that uses the function
    for i, line in enumerate(lines):
        if 'for week_num, start_day, end_day in weeks:' in line:
            # Replace this line
            indent = len(line) - len(line.lstrip())
            new_line = ' ' * indent + 'for week_num, start_month, start_day, end_month, end_day in weeks:\n'
            lines[i] = new_line
            print(f"✓ Updated for loop at line {i+1}")
            
            # Find and replace the week_label line (should be a few lines after)
            for j in range(i+1, min(i+10, len(lines))):
                if 'week-label' in lines[j] and '{month}/{start_day}-{month}/{end_day}' in lines[j]:
                    lines[j] = lines[j].replace(
                        f'({month}/{{start_day}}-{{month}}/{{end_day}})',
                        f'({{start_month}}/{{start_day}}-{{end_month}}/{{end_day}})'
                    )
                    print(f"✓ Updated week label at line {j+1}")
                    break
            break
    
    # Write the file
    with open('generate_checklist.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✓ File successfully updated!")
    return True

if __name__ == "__main__":
    fix_file()
