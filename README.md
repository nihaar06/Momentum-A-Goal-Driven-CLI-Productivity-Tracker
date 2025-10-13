# Momentum: Goal-Driven CLI Productivity Tracker

A comprehensive productivity tracking application built with Streamlit and Supabase.

## Features

- 🎯 **Goal Management**: Set and track your goals with progress monitoring
- ⏱️ **Task Management**: Create and manage tasks linked to your goals
- 📊 **Dashboard**: Visual analytics of your productivity patterns
- ⚙️ **Rules Management**: Categorize applications as productive, distracting, or neutral
- 🔄 **Auto-tracking**: Automatic time tracking for applications

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Supabase

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Copy your project URL and anon key
3. Update `config.py` with your credentials:

```python
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

### 3. Set up Database Schema

Run the SQL commands from `src/dao/schema.sql` in your Supabase SQL editor to create the required tables.

### 4. Run the Application

```bash
streamlit run app.py
```

## Project Structure

```
├── app.py                 # Main Streamlit application
├── config.py             # Configuration file
├── requirements.txt      # Python dependencies
├── src/
│   ├── dao/              # Database operations
│   │   ├── db.py         # Database connection and operations
│   │   └── schema.sql    # Database schema
│   ├── frontend/         # Streamlit UI components
│   │   ├── app.py        # Main app (legacy)
│   │   ├── dashboard.py  # Dashboard page
│   │   ├── goals.py      # Goals management
│   │   ├── rules.py      # Rules management
│   │   └── tasks.py      # Tasks management
│   └── services/         # Business logic
│       ├── services.py   # Main service layer
│       └── auto_tracking.py  # Auto-tracking functionality
```

## Usage

1. **Dashboard**: View your productivity metrics and activity logs
2. **Goals**: Create and manage your goals with progress tracking
3. **Tasks**: Add tasks linked to your goals
4. **Rules Management**: Set up categorization rules for applications

## 📸 Screenshots
![dashboard](https://github.com/user-attachments/assets/888f11ab-c316-4fcb-8ae4-deb2767aca45)
![goal](https://github.com/user-attachments/assets/f42eb610-0f6e-49b3-a703-803abb44140b)
![tasks](https://github.com/user-attachments/assets/22365b00-50af-401c-a094-67d22fb0a772)
![rules](https://github.com/user-attachments/assets/85324128-68b7-44cc-a4c7-06cd227f06f1)

| Screenshot | Description |
|-------------|--------------|
| 🏠 **Dashboard Overview** | Show the main Streamlit dashboard displaying active and completed goals with progress indicators. |
| 🎯 **Goals Page** | Capture the “Goals” section — adding, editing, or deleting a goal, along with goal progress metrics. |
| ✅ **Tasks Page** | Show the “Tasks” interface listing daily or linked tasks, marking one as complete. |
| ⚙️ **Rules Page** | Display your “Rules” or automation setup — e.g., how productivity rules or streaks are created. |
| 📊 **Analytics / Summary (if available)** | Any visual summaries, charts, or streak counters. |
| ⚡ **Add Goal / Task Modal or Form** | Show how users input a new goal or task through Streamlit forms. |
| 🌙 **Dark Mode or Themed View (optional)** | If you’ve styled the app or added themes, include one aesthetic screenshot. |


## Troubleshooting

- Make sure your Supabase credentials are correctly configured
- Ensure all dependencies are installed
- Check that the database schema is properly set up
