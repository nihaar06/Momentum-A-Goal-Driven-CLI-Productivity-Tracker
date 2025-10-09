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

## Troubleshooting

- Make sure your Supabase credentials are correctly configured
- Ensure all dependencies are installed
- Check that the database schema is properly set up