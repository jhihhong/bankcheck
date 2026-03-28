#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a beautiful periodic checklist for 2026
Based on doc2.md requirements (Quarterly, Semi-annual, Annual tasks)
"""

# Task definitions from doc2.md

# Quarterly tasks - occur in specific months
QUARTERLY_TASKS = [
    {
        "months": [1, 4, 7, 10],
        "deadline": "【每季10日前填報】",
        "task": "單位最適員額調查表(people: 1/1, 4/1, 7/1, 10/1)",
        "subtasks": [],
        "reference": ""
    },
    {
        "months": [3, 6, 9, 12],
        "deadline": "【每季月底前填送】",
        "task": "留職停薪人員關懷訪察表",
        "subtasks": [],
        "reference": ""
    },
    {
        "months": [3, 6, 9, 12],
        "deadline": "【當月月底填報】",
        "task": "安全維護檢查報告(總務)",
        "subtasks": [],
        "reference": ""
    },
    {
        "months": [1, 4, 7, 10],
        "deadline": "【每季結束5日內】",
        "task": "內部控制聲明書",
        "subtasks": ["路徑：內網→電子表單→稽核處"],
        "reference": ""
    }
]

# Semi-annual tasks
SEMI_ANNUAL_TASKS = [
    {
        "months": [1, 7],
        "deadline": "【上半年及下半年各一次】",
        "task": "員工特休排假表",
        "subtasks": [],
        "reference": ""
    },
    {
        "months": [1, 7],
        "deadline": "【10日前填報】",
        "task": "理財專員高風險投資聲明書",
        "subtasks": [
            "路徑：內網→電子表單→財富管理處，應列印留存，請經理放行及蓋章"
        ],
        "reference": ""
    },
    {
        "months": [1, 7],
        "deadline": "",
        "task": "安全維護會報紀錄表",
        "subtasks": [],
        "reference": ""
    },
    {
        "months": [1, 7],
        "deadline": "",
        "task": "自衛編組演練",
        "subtasks": [],
        "reference": ""
    },
    {
        "months": [],
        "deadline": "",
        "task": "庫存現金點算查核（　/　）",
        "subtasks": [],
        "reference": ""
    },
    {
        "months": [],
        "deadline": "",
        "task": "債權憑證人工盤點（　/　）",
        "subtasks": [],
        "reference": ""
    }
]

# Annual tasks
ANNUAL_TASKS = [
    {
        "months": [5, 6, 7, 8, 9],
        "deadline": "【5~9月間】",
        "task": "行舍電氣(器)及資訊設備安全檢核表",
        "subtasks": [
            "保存 5 年"
        ],
        "reference": ""
    },
    {
        "months": [8, 9],
        "deadline": "【8~9月】",
        "task": "職場不法侵害預防計畫表",
        "subtasks": [
            "保存 3 年"
        ],
        "reference": ""
    },
    {
        "months": [12],
        "deadline": "【12月】",
        "task": "FO/FA 及其代理人應提供「信用報告」備查",
        "subtasks": [
            "路徑：內網→電子表單→財富管理處→FA/FO 綜合信用報告檢覈表"
        ],
        "reference": ""
    },
    {
        "months": list(range(1, 13)), 
        "deadline": "【接任滿3個月起，1年內應辦理1次】",
        "task": "無預警職務輪調",
        "subtasks": [
            "櫃員主任、ATM 經辦、DAO 至少連續 3 個營業日，並於 PeopleSoft 系統登錄",
            "理專由總行指定期間，於輪調前一日至 PeopleSoft 系統登錄",
            "均應填寫「無預警指定輪調登記表」",
            "應填寫「職務交接查核紀錄表」",
            "櫃員主任（  /   ~   /  ）",
            "ATM 經辦（  /   ~   /  ）",
            "DAO （03/25 ~ 03/27）", 
        ],
        "reference": ""
    }
]



def generate_full_html():
    """Generate complete HTML file - single page for year 2026"""
    
    html_header = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>週期性任務檢核表 2026年</title>
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
        
        .year-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .year-header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .year-header {
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
        
        .period-grid-container {
            display: grid;
            grid-template-columns: 390px 455px 1fr;
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
        
        .period-tasks {
            list-style: none;
        }
        
        .task-item {
            padding: 12px;
            margin: 8px 0;
            background: white;
            border-radius: 6px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            display: flex;
            align-items: flex-start;
            transition: all 0.3s ease;
        }
        
        .task-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
        }
        
        .task-item input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-right: 12px;
            margin-top: 2px;
            cursor: pointer;
            accent-color: #667eea;
            flex-shrink: 0;
        }
        
        .task-item > div {
            flex: 1;
        }
        
        .task-item label {
            cursor: pointer;
            font-size: 0.95em;
            display: block;
            line-height: 1.6;
        }
        
        .subtask-list {
            list-style: none;
            margin: 0 0 0 0;
            padding: 0 0 0 0;
        }
        
        .subtask-item {
            padding: 4px 0 4px 12px;
            font-size: 0.85em;
            color: #6c757d;
            line-height: 1.6;
        }
        
        .reference {
            margin-top: 8px;
            padding: 6px 10px;
            background: #f1f3f5;
            border-radius: 4px;
            font-size: 0.8em;
            color: #495057;
            font-style: italic;
        }
        
        .deadline-indicator {
            color: #667eea;
            font-weight: bold;
            font-size: 0.9em;
            margin-right: 5px;
        }
        
        .month-indicator {
            display: inline-block;
            background: #e7f5ff;
            color: #1864ab;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 5px;
        }
        
        @media print {
            /* 1. 強制瀏覽器印出背景色與漸層 */
            body {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                background: white; /* 底色留白，保留區塊標題與標籤的顏色 */
                padding: 0;
            }

            .year-section {
                box-shadow: none;
                padding: 10px;
                border: none;
            }

            .print-button {
                display: none;
            }

            /* 2. 改為直式 A4，讓排版更適合閱讀 */
            @page {
                size: A4 portrait; 
                margin: 1cm;
            }

            /* 3. 重新配置列印網格：上方兩欄，下方一欄 */
            .period-grid-container {
                display: grid;
                grid-template-columns: 1fr 1fr; /* 切分為平均兩欄 */
                gap: 15px;
            }

            .column:nth-child(1) { /* 每季任務 */
                grid-column: 1 / 2;
            }

            .column:nth-child(2) { /* 每半年任務 */
                grid-column: 2 / 3;
            }

            .column:nth-child(3) { /* 每年任務 - 佔滿整欄往下長 */
                grid-column: 1 / 3; 
            }

            /* 4. 防止任務項目跨頁被切成兩半 */
            .task-item {
                break-inside: avoid;
                page-break-inside: avoid;
                padding: 8px 10px;
                margin: 6px 0;
            }

            /* 微調內距節省空間 */
            .column {
                padding: 10px;
            }
        }
        
        @media (max-width: 1400px) {
            .period-grid-container {
                grid-template-columns: 390px 455px 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="year-section">
            <div class="year-header-container">
                <div class="year-header">📅 週期性任務檢核表 - 2026年</div>
                <button class="print-button" onclick="window.print()">🖨️ 列印</button>
            </div>
            <div class="period-grid-container">
'''
    
    html_footer = '''
            </div>
        </div>
    </div>
    
    <script>
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
                const label = e.target.nextElementSibling.querySelector('label');
                if (label) {
                    if (e.target.checked) {
                        label.style.textDecoration = 'line-through';
                        label.style.opacity = '0.6';
                    } else {
                        label.style.textDecoration = 'none';
                        label.style.opacity = '1';
                    }
                }
            }
        });
        
        // Apply saved styles on load
        window.addEventListener('load', function() {
            document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
                if (checkbox.checked) {
                    const label = checkbox.nextElementSibling.querySelector('label');
                    if (label) {
                        label.style.textDecoration = 'line-through';
                        label.style.opacity = '0.6';
                    }
                }
            });
        });
    </script>
</body>
</html>'''
    
    # Generate single page with all tasks
    full_html = html_header
    
    # Quarterly tasks column
    full_html += '''                <!-- Quarterly Tasks -->
                <div class="column">
                    <div class="column-title">每季任務</div>
                    <ul class="period-tasks">
'''
    for idx, task in enumerate(QUARTERLY_TASKS, 1):
        months_str = "、".join([f"{m}月" for m in task["months"]])
        task_id = f"quarterly-{idx}"
        deadline_html = f'<span class="deadline-indicator">{task["deadline"]}</span>' if task["deadline"] else ''
        
        full_html += f'''                        <li class="task-item">
                            <input type="checkbox" id="{task_id}">
                            <div>
                                <label for="{task_id}">{deadline_html}{task["task"]}<span class="month-indicator">{months_str}</span></label>
'''
        if task["subtasks"]:
            full_html += '''                                <ul class="subtask-list">
'''
            for subtask in task["subtasks"]:
                full_html += f'''                                    <li class="subtask-item">- {subtask}</li>
'''
            full_html += '''                                </ul>
'''
        if task["reference"]:
            full_html += f'''                                <div class="reference">{task["reference"]}</div>
'''
        full_html += '''                            </div>
                        </li>
'''
    full_html += '''                    </ul>
                </div>
'''
    
    # Semi-annual tasks column
    full_html += '''                <!-- Semi-Annual Tasks -->
                <div class="column">
                    <div class="column-title">每半年任務</div>
                    <ul class="period-tasks">
'''
    for idx, task in enumerate(SEMI_ANNUAL_TASKS, 1):
        months_str = "、".join([f"{m}月" for m in task["months"]])
        task_id = f"semiannual-{idx}"
        deadline_html = f'<span class="deadline-indicator">{task["deadline"]}</span>' if task["deadline"] else ''
        
        full_html += f'''                        <li class="task-item">
                            <input type="checkbox" id="{task_id}">
                            <div>
                                <label for="{task_id}">{deadline_html}{task["task"]}<span class="month-indicator">{months_str}</span></label>
'''
        if task["subtasks"]:
            full_html += '''                                <ul class="subtask-list">
'''
            for subtask in task["subtasks"]:
                full_html += f'''                                    <li class="subtask-item">- {subtask}</li>
'''
            full_html += '''                                </ul>
'''
        if task["reference"]:
            full_html += f'''                                <div class="reference">{task["reference"]}</div>
'''
        full_html += '''                            </div>
                        </li>
'''
    full_html += '''                    </ul>
                </div>
'''
    
    # Annual tasks column
    full_html += '''                <!-- Annual Tasks -->
                <div class="column">
                    <div class="column-title">每年任務</div>
                    <ul class="period-tasks">
'''
    for idx, task in enumerate(ANNUAL_TASKS, 1):
        # Show months if not all months
        if len(task["months"]) < 12:
            months_str = "、".join([f"{m}月" for m in task["months"]])
            month_html = f'<span class="month-indicator">{months_str}</span>'
        else:
            month_html = '<span class="month-indicator">全年</span>'
        
        task_id = f"annual-{idx}"
        deadline_html = f'<span class="deadline-indicator">{task["deadline"]}</span>' if task["deadline"] else ''
        
        full_html += f'''                        <li class="task-item">
                            <input type="checkbox" id="{task_id}">
                            <div>
                                <label for="{task_id}">{deadline_html}{task["task"]}{month_html}</label>
'''
        if task["subtasks"]:
            full_html += '''                                <ul class="subtask-list">
'''
            for subtask in task["subtasks"]:
                full_html += f'''                                    <li class="subtask-item">- {subtask}</li>
'''
            full_html += '''                                </ul>
'''
        if task["reference"]:
            full_html += f'''                                <div class="reference">{task["reference"]}</div>
'''
        full_html += '''                            </div>
                        </li>
'''
    full_html += '''                    </ul>
                </div>
'''
    
    full_html += html_footer
    
    return full_html

if __name__ == "__main__":
    html_content = generate_full_html()
    
    with open("checklist_2026_periodic.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ 已成功生成週期性任務檢核表: checklist_2026_periodic.html")
    print("📅 涵蓋：2026年全年")
    print("📋 包含：每季、每半年、每年任務")
