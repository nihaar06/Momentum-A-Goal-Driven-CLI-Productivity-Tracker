# auto_tracker.py
import sys
import time
from datetime import datetime, timedelta
from src.dao.db import ops
from src.services.services import services

try:
    import pygetwindow as gw
except Exception as e:
    print("❌ ERROR: A required GUI library could not be loaded.")
    sys.exit(1)

def get_idle_duration():
    """Returns the number of seconds the user has been idle."""
    idle_duration = 0
    if sys.platform == 'win32':
        from ctypes import Structure, windll, c_uint, sizeof, byref
        class LASTINPUTINFO(Structure):
            _fields_ = [('cbSize', c_uint), ('dwTime', c_uint)]
        
        lii = LASTINPUTINFO()
        lii.cbSize = sizeof(lii)
        windll.user32.GetLastInputInfo(byref(lii))
        millis = windll.kernel32.GetTickCount() - lii.dwTime
        idle_duration = millis / 1000.0
        
    elif sys.platform == 'darwin': # macOS
        # You may need to run: pip install pyobjc-core pyobjc-framework-Quartz
        from Quartz import CGEventSourceSecondsSinceLastEventType, kCGAnyInputEventType
        idle_duration = CGEventSourceSecondsSinceLastEventType(kCGAnyInputEventType)

    # Note: Linux implementation can be complex and is omitted for simplicity.
    # The previous title-parsing method can be a fallback for Linux if needed.

    return idle_duration

# --- Configuration ---
LOG_INTERVAL_SECONDS = 60
IDLE_THRESHOLD_SECONDS = 5 * 60
RULES_REFRESH_INTERVAL_SECONDS = 10 * 60

# --- Setup ---
db_handler = ops()
ss=services()
# --- Helper Functions ---
def parse_app_name_from_title(title: str) -> str:
    # ... (this function remains the same)
    separators = ['-', '|', '—']
    for sep in separators:
        if sep in title:
            return title.split(sep)[-1].strip()
    return title if len(title) < 25 else "Unknown"

def categorize_activity(title: str, rules: list) -> str:
    # ... (this function remains the same)
    if not title:
        return 'uncategorized'
    for rule in rules:
        if rule['keyword'].lower() in title.lower():
            return rule['category']
    return 'neutral'

# --- Main Daemon Loop ---
def main():
    print("🚀 Starting Automatic Activity Tracker... (Press Ctrl+C to stop)")
    
    rules = []
    rules_last_fetched = datetime.min

    while True:
        try:
            now = datetime.now()

            # Dynamically refresh rules
            if (now - rules_last_fetched).total_seconds() > RULES_REFRESH_INTERVAL_SECONDS:
                print("🔄 Refreshing categorization rules...")
                rules = ss.get_all_rules() or []
                rules_last_fetched = now

            # NEW: Simplified idle check
            if get_idle_duration() > IDLE_THRESHOLD_SECONDS:
                category = 'idle'
                app_name = "Idle"
                active_window_title = "Away From Keyboard"
            else:
                # Get active window details
                active_window = gw.getActiveWindow()
                if active_window:
                    active_window_title = active_window.title
                    app_name = parse_app_name_from_title(active_window_title)
                else:
                    active_window_title = "No Active Window"
                    app_name = "Unknown"
                
                category = categorize_activity(active_window_title, rules)

            print(f"Logging: [{category}] {app_name} - {active_window_title}")
            ss.add_activity_logs(
                app_name=app_name,
                window_title=active_window_title,
                start_time=(now - timedelta(seconds=LOG_INTERVAL_SECONDS)),
                end_time=now,
                duration_minutes=int(LOG_INTERVAL_SECONDS / 60),
                category=category
            )
            
            time.sleep(LOG_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\nStopping tracker...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Restarting loop...")
            time.sleep(LOG_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()