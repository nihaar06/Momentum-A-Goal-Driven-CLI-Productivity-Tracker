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
    