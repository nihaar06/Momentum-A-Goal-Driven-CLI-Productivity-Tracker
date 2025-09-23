from services import services
from db import ops

ss=services()
op=ops()

def goals_menu():
    while True:
        print("\tGOAL MANAGEMENT MENU")
        print("\n1.Create goal")
        print("\n2.List Goals\n3.Show progress")
        ch=int(input("Enter your choice :"))
        match(ch):
            case 1:
                des=input("Enter the description for the goal:")
                m=int(input("Enter the metrics for the goal:"))
                t=int(input("Enter the target of the goal:"))
                deadline=input("Enter the deadline in the format('YYYY-MM-DD')(optional):")
                ops.add_goal(des,m,t,deadline or None)
                print("Goal added successfully")
                break
            case 2:
                print("----YOUR GOALS----")
                goals=ops.list_goals()
                if goals:
                    for i in goals:
                        print(f"ID:{i['goal_id']}, Description:{i['description']}")
                else:
                    print("No goals found")
                break
            case 3:
                id=int(input("Enter the goal id:"))
                pr=ops.show_progress(id)
                if pr is not None:
                    print("Progress:",pr*100)
                else:
                    print("Goal not found")
                break
            case _:
                exit

