import os
from supabase import Client,create_client
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime,timedelta,timezone
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import SUPABASE_URL, SUPABASE_KEY

load_dotenv()

# Use environment variables if available, otherwise use config file
url = os.getenv('SUPABASE_URL') or SUPABASE_URL
key = os.getenv("SUPABASE_KEY") or SUPABASE_KEY

if url == 'your_supabase_url_here' or key == 'your_supabase_anon_key_here':
    print("⚠️  WARNING: Please configure your Supabase credentials in config.py or set environment variables")
    print("   SUPABASE_URL and SUPABASE_KEY")

sb:Client=create_client(url,key)


class ops:
    ###GOALS###
    def add_goal(self,description,metric,target,deadline=None):
        try:
            payload={'description':description,'metric':metric,'target_value':target,'deadline':deadline}
            resp=sb.table('goals').insert(payload).execute()
            return resp.data
        except Exception as e:
            raise ValueError(f"An error occured! {e}")

    def update_goal(self, goal_id, description, metric, target_value,deadline=None,current_value=None):
        """Updates an existing goal's details."""
        try:
            payload = {
                'description': description,
                'metric': metric,
                'target_value': target_value,
                'deadline':deadline,
                'current_value':current_value
            }
            res = sb.table('goals').update(payload).eq('goal_id', goal_id).execute()
            return res.data
        except Exception as e:
            raise ValueError(f"Error! Could not update goal: {e}")

    def delete_goal(self, goal_id):
        """Deletes a goal by its ID."""
        try:
            res = sb.table('goals').delete().eq('goal_id', goal_id).execute()
            return res.data
        except Exception as e:
            raise ValueError(f"Error! Could not delete goal: {e}")
    
    def list_goals(self):
        try:
            res=sb.table('goals').select('*').execute()
            return res.data if res.data else None
        except Exception as e:
            raise ValueError(f"Error! Could not retrieve the data:{e}")
        
    def get_goal(self,goal_id):
        try:
            resp=sb.table('goals').select('*').eq('goal_id',goal_id).execute()
            return resp.data[0] if resp.data else None
        except Exception as e:
            raise ValueError(f"Error Occured! Could not retrieve the goal:{e}")
    
    def update_progress(self,goal_id,value):
        try:
            resp=sb.table('goals').select('*').eq('goal_id',goal_id).execute()
            if resp.data:
                n=resp.data[0]['current_value']+value
                res=sb.table('goals').update({'current_value':n}).eq('goal_id',goal_id).execute()
                return res.data if res.data else None
        except Exception as e:
            raise ValueError(f"Error! Could not update progress:{e}")
        
    def show_progress(self,goal_id):
        try:
            resp=sb.table('goals').select('*').eq('goal_id',goal_id).execute()
            if resp.data:
                if resp.data[0]['target_value']==0:
                    return 0.0
                progress=resp.data[0]['current_value']/resp.data[0]['target_value']
                return progress
        except Exception as e:
            raise ValueError(f"Error! Unable to show progress:{e}")
    
    ###TASKS###
    def add_task(self,goal_id,description,priority):
        try:
            payload={'goal_id':goal_id,'description':description,'is_prioritized':priority}
            resp=sb.table('tasks').insert(payload).execute()
            return resp.data
        except Exception as e:
            raise ValueError(f'Error Occured! Could not add the task:{e}')
        
    def get_task(self,task_id):
        try:
            resp=sb.table('tasks').select('*').eq('task_id',task_id).execute()
            return resp.data[0] if resp.data else None
        except Exception as e:
            raise ValueError(f"Error Occured! Could not retrieve the task:{e}")
    
    def list_tasks(self):
        try:
            resp=sb.table("tasks").select("*").execute()
            return resp.data if resp.data else None
        except Exception as e:
            raise ValueError(f"Error Occured! Could not retrieve the tasks table:{e}")      

    def update_task(self, task_id, description, goal_id):
        """Updates an existing task's details."""
        try:
            payload = {'description': description, 'goal_id': goal_id}
            res = sb.table('tasks').update(payload).eq('task_id', task_id).execute()
            return res.data
        except Exception as e:
            raise ValueError(f"Error! Could not update task: {e}")

    def delete_task(self, task_id):
        """Deletes a task by its ID."""
        try:
            res = sb.table('tasks').delete().eq('task_id', task_id).execute()
            return res.data
        except Exception as e:
            raise ValueError(f"Error! Could not delete task: {e}")
    def update_task_status(self,task_id,status):
        try:
            res=sb.table('tasks').update({'status':status}).eq('task_id',task_id).execute()
            return res.data if res.data else None
        except Exception as e:
            raise ValueError(f'Error! Could not update:{e}')
    
    def get_task_status(self,task_id):
        try:
            resp=sb.table('tasks').select('*').eq('task_id',task_id).execute()
            if resp.data:
                return resp.data[0]['status']
        except Exception as e:
            raise ValueError(f"Database error:{e}")
        
    def set_task_prioritized(self,task_id,val):
        try:
            resp=sb.table("tasks").update({'is_prioritized':val}).eq('task_id',task_id).execute()
            return resp.data if resp.data else None
        except Exception as e:
            raise ValueError(f"Error! Could not prioritize the task:{e}")
        
    def get_prioritized_tasks(self):
        try:
            resp=sb.table('tasks').select('*').eq('is_prioritized',True).execute()
            return resp.data if resp.data else None
        except Exception as e:
            raise ValueError(f"Error! Could not retrieve prioritized Tasks:{e}")
        
    ###TIME_ENTRY###
    def add_time_entry(self,task_id,start_time,end_time,dur):
        try:
            payload={
                'task_id':task_id,
                'start_time':start_time.isoformat(),
                'end_time':end_time.isoformat(),
                'duration_minutes':dur
            }
            res=sb.table('time_entries').insert(payload).execute()
            return res.data if res.data else None
        except Exception as e:
            raise ValueError(f"Error! Could not insert the entry :{e}")
        
###RULES MANAGEMENT###
    def add_rule(self,keyword,category):
        try:
            payload={
                'keyword':keyword,
                'category':category
            }
            res=sb.table('rules').insert(payload).execute()
            return res.data if res.data else None
        except Exception as e:
            raise ValueError(f"Error! Could not insert the entry :{e}")
    def list_rules(self):
        try:
            res=sb.table('rules').select("*").execute()
            return res.data if res.data else None
        except Exception as e:
            raise ValueError(f"Error! Could not fetch data :{e}")
    def delete_rule(self,rule_id):
        try:
            ch=sb.table('rules').select('*').eq('rule_id',rule_id).execute()
            if ch.data:
                res=sb.table('rules').delete().eq('rule_id',rule_id).execute()
                return res.data if res.data else None
        except Exception as e:
            raise ValueError(f"Error! Could not delete the entry :{e}")
        
    def add_activity_log(self,app_name,window_title,category,start_time,end_time,duration_minutes):
        try:
            payload={
                'app_name':app_name,
                'window_title':window_title,
                'category':category,
                'start_time':start_time.isoformat(),
                'end_time':end_time.isoformat(),
                'duration_minutes':duration_minutes
            }
            resp=sb.table('activity_logs').insert(payload).execute()
            return resp.data if resp.data else None
        except Exception as e:
            raise ValueError(f"Error! Could not add activity: {e}")
    #BAR CHART,PIE CHART
    def track_progress(self,days):
        try:
            start_date=datetime.now(timezone.utc)-timedelta(days=days)
            resp=sb.table("activity_logs").select('category','duration_minutes','window_title').gte('start_time',start_date.isoformat()).execute()
            if resp.data:
                df=pd.DataFrame(resp.data)
                return df
            else:
                return pd.DataFrame(columns=['category','duration_minutes'])
        except Exception as e:
            raise ValueError(f"Error! Could not perform that action:{e}")
        #LINE CHART
    def track_productivity(self,category,days):
        try:
            start_date=datetime.now(timezone.utc)-timedelta(days=days)
            resp=sb.table("activity_logs").select('start_time','duration_minutes').eq('category',category).gte('start_time',start_date.isoformat()).execute()
            if not resp.data:
                return pd.DataFrame(columns=['date','total_minutes'])
            df=pd.DataFrame(resp.data)
            df['start_time']=pd.to_datetime(df['start_time'])
            df['date']=df['start_time'].dt.date
            daily_summary=df.groupby('date')['duration_minutes'].sum().reset_index()
            daily_summary.rename(columns={'duration_minutes':'total_minutes'},inplace=True)
            return daily_summary
        except Exception as e:
            print(f"Error! Could not perform that action:{e}")
            return pd.DataFrame(columns=['date','total_minutes'])   