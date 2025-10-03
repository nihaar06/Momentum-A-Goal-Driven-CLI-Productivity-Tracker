#CLI Implementation

from services import services
from db import ops

ss=services()
op=ops()

def goals_menu():
    while True:
        print("\tGOAL MANAGEMENT MENU")
        print("\n1.Create goal")
        print("2.List Goals\n3.Update progress\n4.Show progress")
        try:
            choice = input("Enter your choice: ")
            ch = int(choice)
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            continue
        match(ch):
            case 1:
                des=input("Enter the description for the goal:")
                m=int(input("Enter the metrics for the goal:"))
                t=int(input("Enter the target of the goal:"))
                deadline=input("Enter the deadline in the format('YYYY-MM-DD')(optional):")
                ss.add_goal(des,m,t,deadline or None)
                print("Goal added successfully")
                 
            case 2:
                print("----YOUR GOALS----")
                goals=ss.list_goals()
                if goals:
                    for i in goals:
                        print(f"ID:{i['goal_id']}, Description:{i['description']}")
                else:
                    print("No goals found")
                 
            case 3:
                id=int(input("Enter the goal id:"))
                val=int(input("Enter the completed progress:"))
                resp=ss.update_progress(id,val)
                if resp:
                    print("Progress updated successfully.")
                else:
                    print("Could not update your progress.")
                 
            case 4:
                id=int(input("Enter the goal id:"))
                pr=ss.show_progress(id)
                if pr is not None:
                    print("Progress:",pr*100)
                else:
                    print("Goal not found")
                 
            case _:
                break   
def tasks_menu():
    while True:
        print("\tTASK MANAGEMENT MENU")
        print("\n1.Add a new task")
        print("\n2.Start timer for a task")
        print("\n3.Stop the current timer")
        print("\n4.Show task status")
        try:
            choice = input("Enter your choice: ")
            ch = int(choice)
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            continue
        match ch:
            case 1:
                id=int(input("Enter the goal id:"))
                desc=input("Enter the description for the task:")
                ss.add_task(id,desc)
                print("TASK ADDED SUCCESSFULLY")
                 
            case 2:
                id=int(input("Enter the task id:"))
                ss.start_timer(id)
                 
            case 3:
                stopped_id=ss.end_timer()
                mark_complete=input("Mark this task as completed?(y/n):").lower()
                if mark_complete=='y':
                    ss.update_task_status(stopped_id,'Completed')
                    print("Task marked as Completed.")
                 
            case 4:
                s=ss.get_status()
                if s:
                    print("Current Task Status:",s)
            case _:
                break
def main():
    print("Welcome to MOMENTUM,your CLI productivity tracker")
    while True:
        print("\t Main Menu")
        print("\n1.Goal Management Menu\n2.Task Management Menu")
        try:
            choice = input("Enter your choice: ")
            ch = int(choice)
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            continue
        match ch:
            case 1:
                goals_menu()
            case 2:
                tasks_menu()
            case _:
                print("KEEP PROGRESSING!\n\tTHANK YOU.")
                exit()
if __name__=="__main__":
    main()
