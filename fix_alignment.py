#!/usr/bin/env python3
"""
Script to fix checkbox and text alignment in the checklist HTML
by wrapping label and subtasks in a div for proper flexbox layout.
"""

import re

def fix_task_items(content):
    """Fix task-item structure to work with flexbox"""
    
    # Pattern to match task-item with label and optional subtask-list
    pattern = r'(<li class="task-item">)\s*(<input[^>]+>)\s*(<label[^>]+>.*?</label>)\s*((?:<ul class="subtask-list">.*?</ul>)?)\s*(</li>)'
    
    def replace_func(match):
        opening = match.group(1)
        checkbox = match.group(2)
        label = match.group(3)
        subtasks = match.group(4)
        closing = match.group(5)
        
        # Properly indent the output
        result = f'''{opening}
                            {checkbox}
                            <div>
                                {label}'''
        
        if subtasks.strip():
            result += f'''
                                {subtasks}'''
        
        result += f'''
                            </div>
                        {closing}'''
        
        return result
    
    content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
    return content

def fix_week_task_items(content):
    """Fix week-task-item structure to work with flexbox"""
    
    # Pattern to match week-task-item with label and optional week-subtask-list
    pattern = r'(<li class="week-task-item">)\s*(<input[^>]+>)\s*(<label[^>]+>.*?</label>)\s*((?:<ul class="week-subtask-list">.*?</ul>)?)\s*(</li>)'
    
    def replace_func(match):
        opening = match.group(1)
        checkbox = match.group(2)
        label = match.group(3)
        subtasks = match.group(4)
        closing = match.group(5)
        
        # Properly indent the output
        result = f'''{opening}
                                {checkbox}
                                <div>
                                    {label}'''
        
        if subtasks.strip():
            result += f'''
                                    {subtasks}'''
        
        result += f'''
                                </div>
                            {closing}'''
        
        return result
    
    content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
    return content

def main():
    # Read the HTML file
    with open('checklist_2026_full.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix task items
    content = fix_task_items(content)
    content = fix_week_task_items(content)
    
    # Write back to file
    with open('checklist_2026_full.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed alignment structure in checklist_2026_full.html")

if __name__ == '__main__':
    main()
