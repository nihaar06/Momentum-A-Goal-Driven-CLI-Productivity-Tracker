from db import ops
import os
import json
from datetime import datetime

op=ops()
class services:
    STATE_FILE_PATH=os.path.expanduser('~/.momentum_state.json')
    def start_timer(self,task_id):
        if os.path.exists(self.STATE_FILE_PATH):
            print("A timer is already running.")
            return 
        tid=op.get_task(task_id)
        if not tid:
            print("No task found.")
            return 
        start_time=datetime.now().isoformat()
        state_data={
            'task_id':task_id,
            'start_time':start_time
        }
        op.update_task_status(task_id,'in_progress')
        try:
            with open(self.STATE_FILE_PATH,'w') as j:
                json.dump(state_data,j)
        except IOError as e:
            print('Error! Could not write to json file')
            return 
        print("Timer started for task :",tid['description'])

    def end_timer(self):
        if os.path.exists(self.STATE_FILE_PATH):
            try:
                with open(self.STATE_FILE_PATH,'r') as f:
                    state_data=json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error: Could not read state file: {e}")
                return
            ti=state_data['task_id']
            stt=state_data['start_time']
            start_time=datetime.fromisoformat(stt)
            end_time=datetime.now()
            duration=end_time-start_time
            d_in_min=int(duration.total_seconds()/60)
            if d_in_min==0:
                d_in_min=1
            tid=op.get_task(ti)
            if not tid:
                print("No task found.")
                os.remove(self.STATE_FILE_PATH)
                return 
            op.add_time_entry(ti,start_time,end_time,d_in_min)
            hours=d_in_min/60
            op.update_progress(tid['goal_id'],hours)           
            op.update_task_status(ti,'todo')
            os.remove(self.STATE_FILE_PATH)
            print("Timer stopped, You worked for",d_in_min,"minutes.")
            return ti
        else:
            print("No timer is running.")
            return

    def get_status(self):
        if os.path.exists(self.STATE_FILE_PATH):
            try:
                with open(self.STATE_FILE_PATH,'r') as f:
                    state_data=json.load(f)
                tid=state_data['task_id']
                status=op.get_task_status(tid)
                return status
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error: Could not read state file: {e}")
                return None
        else :
            print("No timer is running")
            return None
    
    def add_goal(self,des,m,t,deadline):
        res=op.add_goal(des,m,t,deadline)
        return res
    
    def get_goal(self,id):
        return op.get_goal(id)
    
    def update_goals(self,id,desc,metric,target_value,deadline):
        return op.update_goal(id,desc,metric,target_value,deadline)
    
    def delete_goal(self,id):
        return op.delete_goal(id)
    
    def list_goals(self):
        return op.list_goals()
    
    def update_progress(self,id,val):
        return op.update_progress(id,val)
    
    def show_progress(self,id):
        return op.show_progress(id)
    
    def add_task(self,id,desc,p):
        return op.add_task(id,desc,p)

    def update_task(self, task_id, description, goal_id):
        return op.update_task(task_id, description, goal_id)
    
    def delete_task(self, task_id):
        return op.delete_task(task_id)
    
    def set_task_prioritized(self,tid,val):
        return op.set_task_prioritized(tid,val)
    
    def get_prioritized_tasks(self):
        return op.get_prioritized_tasks()

    def update_task_status(self,id,status):
        return op.update_task_status(id,status)
    
    def list_tasks(self):
        return op.list_tasks()

    ###RULES###
    def get_all_rules(self):
        return op.list_rules()
    
    def add_activity_logs(self,app_name,window_title,category,start_time,end_time,duration_minutes):
        return op.add_activity_log(app_name,window_title,category,start_time,end_time,duration_minutes)
    
    def track_activity(self,days):
        return op.track_progress(days)
    
    def track_productivity(self,category,days):
        return op.track_productivity(category,days)