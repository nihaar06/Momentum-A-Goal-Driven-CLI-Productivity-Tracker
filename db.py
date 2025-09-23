import os
from supabase import Client,create_client
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

url=os.getenv('SUPABASE_URL')
key=os.getenv("SUPABASE_KEY")
sb:Client=create_client(url,key)


class ops:
    ###GOALS###
    def add_goal(self,description,metric,target,deadline):
        try:
            payload={'description':description,'metric':metric,'target_value':target,'deadline':deadline}
            resp=sb.table('goals').insert(payload).execute()
            return resp.data
        except:
            raise ValueError("An error occured!")
    
    def list_goals(self):
        try:
            res=sb.table('goals').select('*').execute()
            return res.data if res.data else None
        except:
            raise ValueError("Error! Could not retrieve the data")
        
    def get_goal(self,goal_id):
        try:
            resp=sb.table('goals').select('*').eq('goal_id',goal_id).execute()
            return resp.data[0] if resp.data else None
        except:
            raise ValueError("Error Occured! Could not retrieve the goal")
    
    def update_progress(self,goal_id,value):
        try:
            resp=sb.table('goals').select('*').eq('goal_id',goal_id).execute()
            if resp.data:
                n=resp.data[0]['current_value']+value
                res=sb.table('goals').update({'current_value':n}).eq('goal_id',goal_id).execute()
                return res.data if res.data else None
        except:
            raise ValueError("Error! Could not update progress")
        
    def show_progress(self,goal_id):
        try:
            resp=sb.table('goals').select('*').eq('goal_id',goal_id).execute()
            if resp.data:
                progress=resp.data[0]['current_value']/resp.data[0]['target_value']
                return progress
        except:
            raise ValueError("Error! Unable to show progress")
    
    ###TASKS###
    def add_task(self,goal_id,description):
        try:
            payload={'goal_id':goal_id,'description':description}
            resp=sb.table('tasks').insert(payload).execute()
            return resp.data
        except:
            raise ValueError('Error Occured! Could not add the task')
        
    def get_task(self,task_id):
        try:
            resp=resp=sb.table('tasks').select('*').eq('task_id',task_id).execute()
            return resp.data[0] if resp.data else None
        except:
            raise ValueError("Error Occured! Could not retrieve the task")
    
    def update_task_status(self,task_id,status):
        try:
            resp=sb.table('tasks').select('*').eq('task_id',task_id).execute()
            if resp.data:
                res=sb.table('tasks').update({'status':status}).eq('task_id',task_id).execute()
                return res.data if res.data else None
        except:
            raise ValueError('Error! Could not update')
    
    def get_task_status(self,task_id):
        try:
            resp=sb.table('tasks').select('*').eq('task_id',task_id).execute()
            if resp.data:
                return resp.data[0]['status']
        except Exception as e:
            print("Database error:",e)
            return None
    ###TIME_ENTRY###
    def add_time_entry(self,task_id,start_time,end_time,dur):
        try:
            payload={
                'task_id':task_id,
                'start_time':start_time,
                'end_time':end_time,
                'duration_minutes':dur
            }
            res=sb.table('time_entries').insert(payload).execute()
            return res.data if res.data else None
        except Exception as e:
            raise ValueError("Error! Could not insert the entry :",e)