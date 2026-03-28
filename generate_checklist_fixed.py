#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a beautiful checklist for 2026 (March to December)
Based on doc.md requirements
"""

import calendar
from datetime import datetime, timedelta

# Task definitions from doc.md
DAILY_TASKS = [
    {
        "task": "查核前一營業日【理專關聯戶與客戶帳務交易查核日報表】RPT_D016500",
        "subtasks": []
    },
    {
        "task": "查核財富管理客戶自行帳戶監控日報(電話錄音版) WMD0002",
        "subtasks": [
            "無該當者，在「WMD0002 無該當免列印記錄表」勾稽",
            "有該當者，應逐筆致電關懷客戶並錄音，在 WMD0002 記錄備查"
        ]
    },
    {
        "task": "每日出勤檢視 (PeopleSoft)",
        "subtasks": []
    }
]

WEEKLY_TASKS = [
    {
        "task": "抽查櫃員現金二次",
        "subtasks": ["（　/　）：", "（　/　）："]
    },
    {
        "task": "抽查外匯現金一次",
        "subtasks": ["（　/　）："]
    },
    {
        "task": "抽查金庫現金500元以上一次",
        "subtasks": ["（　/　）："]
    }
]

MONTHLY_TASKS = [
    {
        "deadline": "【不定期抽查兩次】", 
        "task": "行員保管物品自行查核工作底稿",
        "subtasks": ["（　/　）,（　/　）"]
    },
    {"deadline": "【每月一次】", "task": "存戶未領回文件備查簿", "subtasks": []},
    {"deadline": "【每月一次】", "task": "G0655 領用單摺查核", "subtasks": []},
    {"deadline": "【每月5號前】", "task": "請經理填報內部人上月持股變動情形", "subtasks": []},
    {
        "deadline": "【每月5號前】", 
        "task": "自行查核指派表", 
        "subtasks": ["路徑：內網→電子表單→稽核處→請經理放行"]
    },
    {"deadline": "【每月5號前】", "task": "自行查核彙報表", "subtasks": []},
    {"deadline": "【每月5號前列印】", "task": "營業單位 FO/FA 自行存款異動檢核表 RPT_M23400", "subtasks": []},
    {"deadline": "【每月5號前列印】", "task": "疑似理財專員挪用客戶款項態樣查核月報表 PRT_M039700", "subtasks": []},
    {
        "deadline": "【每月9號前登錄】", 
        "task": "前一月份新理財客戶之關係人員員編", 
        "subtasks": ["路徑：內網→電子表單→財管處→新理財客戶關係引介名單"]
    },
    {
        "deadline": "【每月10號前填報】", 
        "task": "前一月份理專疑似挪用客戶款項行為檢核表(word)", 
        "subtasks": ["路徑：內網→電子表單→財管處→請經理放行"]
    },
    {
        "deadline": "阿蓓要確認【10號前】", 
        "task": "營業單位抽查理專保管客戶物品查核表(兩位負責人)", 
        "subtasks": ["（　/　）"]
    },
    {"deadline": "【10號前】", "task": "理專疑似挪用客戶檢核表(需送財管、總行)", "subtasks": []},
    {
        "deadline": "", 
        "task": "金融卡自檢兩次", 
        "subtasks": ["（　/　）,（　/　）"]
    },
    {"deadline": "【月底前, 25號後】", "task": "W20 工作底稿(smart credit)", "subtasks": []},
    { 
        "deadline": "【月底】", 
        "task": "內部管理綜合報告表", 
        "subtasks": ["路徑：內網→電子表單→人力資源處內部管理綜合報告表，請經理放行"]
    },
    {
        "deadline": "【月底】", 
        "task": "保管金庫(室)鑰匙，密碼負責人指派表", 
        "subtasks": ["路徑：內網→電子表單→作業處→金庫鑰匙"]
    },
    {"deadline": "【月底】", "task": "C0210 檢查出納、證照查詢及開戶審核等人數是否符合，與 CXM0003 放在自查當附件", "subtasks": []},
    {
        "deadline": "【月底】", 
        "task": "工作站防毒版本查詢", 
        "subtasks": ["路徑：內網→資產盤點→設定管理→檢核作業→防毒版本查詢→大於 1M 打勾→工作站異常全選→查詢"]
    },
    {
        "deadline": "", 
        "task": "新舊股回收控管表", 
        "subtasks": ["路徑：內網→電子表單→信託處"]
    },
]

SPECIAL_TASKS = {
    1: ["理專高風險投資聲明書", "最適員額、內控聲明書"],
    3: ["安全維護檢查報告表"],
    4: ["最適員額、內控聲明書"],
    6: ["安全維護檢查報告表"],
    7: ["理專高風險投資聲明書", "最適員額、內控聲明書"],
    9: ["安全維護檢查報告表"],
    10: ["最適員額、內控聲明書"],
    12: ["安全維護檢查報告表"]
}

MONTH_NAMES = {
    3: "3月", 4: "4月", 5: "5月", 6: "6月",
    7: "7月", 8: "8月", 9: "9月", 10: "10月",
    11: "11月", 12: "12月"
}

def get_week_number_of_year(date):
    """
    Calculate week number of the year where week starts on Sunday.
    Week 1 is the first week that contains a Sunday in the year.
    """
    jan_1 = datetime(date.year, 1, 1)
    days_until_sunday = (6 - jan_1.weekday()) % 7
    if days_until_sunday == 0 and jan_1.weekday() == 6:
        first_sunday = jan_1
    else:
        first_sunday = jan_1 + timedelta(days=days_until_sunday)
    if date < first_sunday:
        return 1
    days_diff = (date - first_sunday).days
    week_num = (days_diff // 7) + 1
    return week_num


def should_show_week_in_month(year, month, week_num, start_day):
    """
    Determine if a week should be shown in this month.
    A week is shown in the month where its Sunday falls.
    """
    date = datetime(year, month, start_day)
    day_of_week = date.weekday()
    if day_of_week == 6:
        return True
    days_since_sunday = (day_of_week + 1) % 7
    sunday_date = date - timedelta(days=days_since_sunday)
    return sunday_date.month == month


def get_weeks_in_month(year, month):
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
    
    return weeks

def generate_month_html(year, month):
    """Generate HTML for a single month"""
    month_name = MONTH_NAMES[month]
    month_id = f"m{month}"
    
    # Start month section
    html = f'''
        <!-- {month_name} {year} -->
        <div class="month-section" id="month-{month}">
            <div class="month-header-container">
                <div class="month-header">📋 工作檢核表 2026 - {year}年 {month_name}</div>
                <button class="print-button" onclick="printMonth({month})">🖨️ 列印本月</button>
            </div>
            <div class="grid-container">
                <!-- Daily Tasks Column -->
                <div class="column">
                    <div class="column-title">每日任務</div>
                    <ul class="monthly-tasks">
'''
    
    # Add daily tasks with monthly checkbox
    task_id = 1
    for task_item in DAILY_TASKS:
        task = task_item["task"] if isinstance(task_item, dict) else task_item
        subtasks = task_item.get("subtasks", []) if isinstance(task_item, dict) else []
        
        html += f'''                        <li class="task-item">
                            <input type="checkbox" id="{month_id}-daily-{task_id}">
                            <label for="{month_id}-daily-{task_id}">{task}</label>
'''
        # Add subtasks if any
        if subtasks:
            html += '''                            <ul class="subtask-list">
'''
            for subtask in subtasks:
                html += f'''                                <li class="subtask-item">- {subtask}</li>
'''
            html += '''                            </ul>
'''
        
        html += '''                        </li>
'''
        task_id += 1
    
    html += '''                    </ul>
                </div>
                
                <!-- Weekly Column (now in middle) -->
                <div class="column weekly-column">
                    <div class="column-title">每週任務</div>
'''
    
    # Add weekly tasks with 2-column layout for tasks within each week
    weeks = get_weeks_in_month(year, month)
    for week_num, start_day, end_day in weeks:
        # Only show weeks that start in this month (to avoid overlap)
        if not should_show_week_in_month(year, month, week_num, start_day):
            continue
            
        week_id = f"w{month}-{week_num}"
        html += f'''                    <div class="week-row">
                        <div class="week-label">WW{week_num:02d} ({month}/{start_day}-{month}/{end_day})</div>
                        <ul class="week-tasks">
'''
        for idx, task_item in enumerate(WEEKLY_TASKS, 1):
            task = task_item["task"] if isinstance(task_item, dict) else task_item
            subtasks = task_item.get("subtasks", []) if isinstance(task_item, dict) else []
            
            html += f'''                            <li class="week-task-item">
                                <input type="checkbox" id="{week_id}-{idx}">
                                <label for="{week_id}-{idx}">{task}</label>
'''
            # Add subtasks if any
            if subtasks:
                html += '''                                <ul class="week-subtask-list">
'''
                for subtask in subtasks:
                    html += f'''                                    <li class="week-subtask-item">{subtask}</li>
'''
                html += '''                                </ul>
'''
            html += '''                            </li>
'''
        html += '''                        </ul>
                    </div>
'''
    
    html += '''                </div>
                
                <!-- Monthly Column (now on right) -->
                <div class="column">
                    <div class="column-title">每月任務</div>
                    <ul class="monthly-tasks">
'''
    
    # Add monthly tasks
    task_id = 1
    for task_item in MONTHLY_TASKS:
        deadline = task_item["deadline"]
        task = task_item["task"]
        subtasks = task_item.get("subtasks", [])
        deadline_html = f'<span class="deadline-indicator">{deadline}</span>' if deadline else ''
        html += f'''                        <li class="task-item">
                            <input type="checkbox" id="{month_id}-{task_id}">
                            <label for="{month_id}-{task_id}">{deadline_html}{task}</label>
'''
        # Add subtasks if any
        if subtasks:
            html += '''                            <ul class="subtask-list">
'''
            for subtask in subtasks:
                html += f'''                                <li class="subtask-item">- {subtask}</li>
'''
            html += '''                            </ul>
'''
        
        html += '''                        </li>
'''
        task_id += 1
    
    # Add special tasks if any
    if month in SPECIAL_TASKS:
        for special_task in SPECIAL_TASKS[month]:
            html += f'''                        <li class="task-item special-task">
                            <input type="checkbox" id="{month_id}-{task_id}">
                            <label for="{month_id}-{task_id}"><span class="special-indicator">⭐</span>{special_task}</label>
                        </li>
'''
            task_id += 1
    
    html += '''                    </ul>
                </div>
            </div>
        </div>
'''
    
    return html

def generate_full_html():
    """Generate complete HTML file"""
    
    html_header = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>工作檢核表 2026年 (3月-12月)</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft JhengHei', 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
        }
        
        .month-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            position: relative;
        }
        
        .month-header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .month-header {
            font-size: 1.8em;
            color: #667eea;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            font-weight: bold;
            flex: 1;
        }
        
        .print-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-left: 20px;
        }
        
        .print-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        }
        
        .print-button:active {
            transform: translateY(0);
        }
        
        .grid-container {
            display: grid;
            grid-template-columns: 450px 500px 1fr;
            gap: 20px;
        }
        
        .column {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }
        
        .column-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #495057;
            margin-bottom: 15px;
            text-align: center;
            padding: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
        }
        
        .monthly-tasks, .weekly-tasks {
            list-style: none;
        }
        
        .task-item {
            padding: 10px;
            margin: 0 0;
            background: white;
            border-radius: 6px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            display: flex;
            transition: all 0.3s ease;
        }
        
        .task-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
        }
        
        .task-item input[type="checkbox"] {
            flex-shrink: 0;
            width: 20px;
            height: 20px;
            margin-right: 10px;
            cursor: pointer;
            accent-color: #667eea;
            vertical-align: middle;
        }
        
        .task-item label {
            cursor: pointer;
            font-size: 0.95em;
            vertical-align: middle;
        }
        
        .subtask-list {
            list-style: none;
            padding: 8px 0 0 0;
        }
        
        .subtask-item {
            padding: 4px 0 4px 4px;
            font-size: 0.85em;
            color: #6c757d;
            line-height: 1.6;
        }
        
        .special-task {
            background: #fff3cd !important;
            border-left-color: #ffc107 !important;
        }
        
        .special-indicator {
            color: #ff6b6b;
            font-weight: bold;
            margin-right: 5px;
        }
        
        .deadline-indicator {
            color: #667eea;
            font-weight: bold;
            font-size: 0.9em;
            margin-right: 5px;
        }
        
        .weekly-column {
            grid-column: span 1;
        }
        
        .week-row {
            padding: 12px;
            margin: 8px 0;
            background: white;
            border-radius: 6px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .week-label {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 8px;
            font-size: 1em;
        }
        
        .week-tasks {
            list-style: none;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }
        
        .week-task-item {
            padding: 0px;
            display: flex;
        }
        
        .week-tasks li {
            padding: 0px;
            display: flex;
        }
        
        .week-tasks input[type="checkbox"] {
            flex-shrink: 0;
            width: 18px;
            height: 18px;
            margin-right: 8px;
            cursor: pointer;
            accent-color: #667eea;
            vertical-align: middle;
        }
        
        .week-tasks label {
            cursor: pointer;
            font-size: 0.9em;
            vertical-align: middle;
        }
        
        .week-subtask-list {
            list-style: none;
            padding: 4px 0 0 0;
        }
        
        .week-subtask-item {
            padding: 2px 0;
            font-size: 0.8em;
            color: #6c757d;
            line-height: 1.4;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .month-section {
                page-break-after: always;
                box-shadow: none;
            }
            
            .print-button {
                display: none;
            }
            
            /* Hide other months when printing */
            .month-section:not(.printing) {
                display: none !important;
            }
            
            .month-section.printing {
                display: block !important;
            }
            
            @page {
                size: A4 landscape;
                margin: 1cm;
            }
        }
        
        @media (max-width: 1400px) {
            .grid-container {
                grid-template-columns: 450px 500px 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
'''
    
    html_footer = '''
    </div>
    
    <script>
        // Print specific month
        function printMonth(monthNum) {
            // Hide all months
            const allMonths = document.querySelectorAll('.month-section');
            allMonths.forEach(section => {
                section.classList.remove('printing');
            });
            
            // Show only the selected month
            const targetMonth = document.getElementById('month-' + monthNum);
            if (targetMonth) {
                targetMonth.classList.add('printing');
                
                // Trigger print
                window.print();
                
                // Remove printing class after print dialog closes
                setTimeout(() => {
                    targetMonth.classList.remove('printing');
                }, 100);
            }
        }
        
        // Save checkbox states to localStorage
        document.addEventListener('change', function(e) {
            if (e.target.type === 'checkbox') {
                localStorage.setItem(e.target.id, e.target.checked);
            }
        });
        
        // Load checkbox states from localStorage
        window.addEventListener('load', function() {
            document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
                const saved = localStorage.getItem(checkbox.id);
                if (saved === 'true') {
                    checkbox.checked = true;
                }
            });
        });
        
        // Strike through completed tasks
        document.addEventListener('change', function(e) {
            if (e.target.type === 'checkbox') {
                const label = e.target.nextElementSibling;
                if (e.target.checked) {
                    label.style.textDecoration = 'line-through';
                    label.style.opacity = '0.6';
                } else {
                    label.style.textDecoration = 'none';
                    label.style.opacity = '1';
                }
            }
        });
        
        // Apply saved styles on load
        window.addEventListener('load', function() {
            document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
                if (checkbox.checked) {
                    const label = checkbox.nextElementSibling;
                    label.style.textDecoration = 'line-through';
                    label.style.opacity = '0.6';
                }
            });
        });
    </script>
</body>
</html>'''
    
    # Generate all months
    full_html = html_header
    for month in range(3, 13):  # March to December
        full_html += generate_month_html(2026, month)
    full_html += html_footer
    
    return full_html

if __name__ == "__main__":
    html_content = generate_full_html()
    
    with open("checklist_2026_full.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ 已成功生成完整的檢核表: checklist_2026_full.html")
    print("📅 涵蓋月份: 2026年3月 - 12月")
    print("📋 包含每日、每週、每月任務及特殊項目")
