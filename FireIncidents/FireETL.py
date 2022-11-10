import pandas as pd
import json
import requests
import pyodbc
import sys

#pd.options.display.max_columns = None
#pd.options.display.max_rows = None

def Connect(x,y):
    conn = pyodbc.connect('Driver=SQL Server Native Client 11.0;'
        'Server='+x+';'
        'Database='+y+';'
        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    return cursor, conn

def Extract(LINK):
    #loading data from api into dataframe
    api_request = requests.get(LINK)
    api_text = api_request.text#turns response to text
    data = json.loads(api_text)#reads json data
    df = pd.json_normalize(data)#creates dataframe from json

    Transform(df)

def Transform(df):
    #Perform necessary data transformations
    
    #Standardizing some column values
    df[['incident_borough','alarm_box_borough']] = df[['incident_borough','alarm_box_borough']].replace('RICHMOND / STATEN ISLAND', 'STATEN ISLAND')
    
    #replacing Nan's and NaT's with None
    df = df.fillna(0) #should not normally be used but SQLServer Express is not handling None Values well right now 
    #df = df.astype(object).where(df.notnull(), None) #this code should normally be used to properly account for null values

    #transforming columns to apporpriate daata types
    numcols = [
        'starfire_incident_id',
        'alarm_box_number',
        'engines_assigned_quantity',
        'ladders_assigned_quantity',
        'other_units_assigned_quantity',
        'zipcode',
        'policeprecinct',
        'citycouncildistrict',
        'communitydistrict',
        'communityschooldistrict',
        'congressionaldistrict',
        'dispatch_response_seconds_qy',
        'incident_response_seconds_qy',
        'incident_travel_tm_seconds_qy'
    ]

    df[numcols] = df[numcols].apply(pd.to_numeric)
    
    datecols = [
        'incident_datetime',
        'first_assignment_datetime',
        'first_activation_datetime',
        'incident_close_datetime',
        'first_on_scene_datetime'
    ]

    df[datecols] = df[datecols].apply([pd.to_datetime])
    
    Load(df)

def Load(df):
    #connecting to sql server
    cursor, conn = Connect(SERVERNAME, DATABASENAME)
    
    #getting current Table IDs
    #DIT = Data in Table
    DIT_query = f'''SELECT [Starfire Incident ID] as [existing_ids] FROM {TABLENAME}'''
    DIT = pd.read_sql(DIT_query, conn)
    
    #merging old and ned data based on primary keys
    df_merge = pd.merge(df, DIT, how='left', left_on='starfire_incident_id', right_on='existing_ids')

    #creating insert dataframe where only records that aren't already in databse remain
    df_insert = df_merge[pd.isna(df_merge['existing_ids'])]
    
    df_insert = df_insert[[
       'starfire_incident_id', 
       'incident_datetime', 
       'alarm_box_borough',
       'alarm_box_number', 
       'alarm_box_location', 
       'incident_borough',
       'alarm_source_description_tx', 
       'alarm_level_index_description',       
       'highest_alarm_level', 
       'incident_classification',
       'incident_classification_group', 
       'dispatch_response_seconds_qy',      
       'first_assignment_datetime', 
       'first_activation_datetime',
       'incident_close_datetime', 
       'valid_dispatch_rspns_time_indc',
       'valid_incident_rspns_time_indc', 
       'incident_response_seconds_qy',     
       'incident_travel_tm_seconds_qy', 
       'engines_assigned_quantity',
       'ladders_assigned_quantity', 
       'other_units_assigned_quantity', 
       'zipcode',
       'policeprecinct', 
       'citycouncildistrict', 
       'communitydistrict',
       'communityschooldistrict', 
       'congressionaldistrict',
       'first_on_scene_datetime'
    ]]
    
    insert_stmt= f'''Insert INTO {TABLENAME} 
    (
        [Starfire Incident ID]
        ,[Incident Datetime]                              				
        ,[Alarm Box Borough]                                					
        ,[Alarm Box Number]                                 						
        ,[Alarm Box Location]                               					
        ,[Incident Borough]                                 						
        ,[Alarm Source Description Tx]                      			
        ,[Alarm Level Index Description]                    		
        ,[Highest Alarm Level]                              					
        ,[Incident Classification]                          				
        ,[Incident Classification Group]                    		
        ,[Dispatch Response Seconds Qy]                     			
        ,[First Assignment Datetime]                        			
        ,[First Activation Datetime]                        			
        ,[Incident Close Datetime]                          			
        ,[Valid Dispatch Rspns Time Indc]                   		
        ,[Valid Incident Rspns Time Indc]                   		
        ,[Incident Response Seconds Qy]                     		
        ,[Incident Travel Tm Seconds Qy]                    		
        ,[Engines Assigned Quantity]                        			
        ,[Ladders Assigned Quantity]                        			
        ,[Other Units Assigned Quantity]                    		
        ,[Zip Code]                                         							
        ,[Police Precinct]                                  						
        ,[City Council District]                            				
        ,[Community District]                               				
        ,[Community School District]                        			
        ,[Congressional District]                           				
        ,[First On Scene Datetime]) 
        VALUES (?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?)                        
        '''
    if not df_insert.empty:
        cursor.fast_executemany = True
        cursor.executemany(insert_stmt, df_insert.values.tolist())
        conn.commit()
    
    print('data inserted')
    
    #creating dataframe of only records that are already in the database
    df_update = df_merge[~pd.isna(df_merge['existing_ids'])]
    
    #updating xitsint records in database
    df_update = df_update[[ 
       'incident_datetime', 
       'alarm_box_borough',
       'alarm_box_number', 
       'alarm_box_location', 
       'incident_borough',
       'alarm_source_description_tx', 
       'alarm_level_index_description',       
       'highest_alarm_level', 
       'incident_classification',
       'incident_classification_group', 
       'dispatch_response_seconds_qy',      
       'first_assignment_datetime', 
       'first_activation_datetime',
       'incident_close_datetime', 
       'valid_dispatch_rspns_time_indc',
       'valid_incident_rspns_time_indc', 
       'incident_response_seconds_qy',     
       'incident_travel_tm_seconds_qy', 
       'engines_assigned_quantity',
       'ladders_assigned_quantity', 
       'other_units_assigned_quantity', 
       'zipcode',
       'policeprecinct', 
       'citycouncildistrict', 
       'communitydistrict',
       'communityschooldistrict', 
       'congressionaldistrict',
       'first_on_scene_datetime',
       'starfire_incident_id'
    ]]
    
    update_stmt = f'''
        UPDATE {TABLENAME}
        SET				
        [Incident Datetime]			                        = ?
        ,[Alarm Box Borough]			                    = ?
        ,[Alarm Box Number]				                    = ?
        ,[Alarm Box Location]			                    = ?
        ,[Incident Borough]				                    = ?
        ,[Alarm Source Description Tx]	                    = ?
        ,[Alarm Level Index Description]                    = ?
        ,[Highest Alarm Level]			                    = ?
        ,[Incident Classification]		                    = ?
        ,[Incident Classification Group]                    = ?
        ,[Dispatch Response Seconds Qy]	                    = ?
        ,[First Assignment Datetime]	                    = ?
        ,[First Activation Datetime]	                    = ?
        ,[Incident Close Datetime]		                    = ?
        ,[Valid Dispatch Rspns Time Indc]                   = ?		
        ,[Valid Incident Rspns Time Indc]                   = ?		
        ,[Incident Response Seconds Qy]	                    = ?		
        ,[Incident Travel Tm Seconds Qy]                    = ?		
        ,[Engines Assigned Quantity]	                    = ?		
        ,[Ladders Assigned Quantity]	                    = ?		
        ,[Other Units Assigned Quantity]                    = ?		
        ,[Zip Code]						                    = ?		
        ,[Police Precinct]				                    = ?		
        ,[City Council District]		                    = ?		
        ,[Community District]			                    = ?		
        ,[Community School District]	                    = ?		
        ,[Congressional District]		                    = ?		
        ,[First On Scene Datetime]	                        = ?
        WHERE
        [Starfire Incident ID]	                            = ?		
        '''
    if not df_update.empty:
        cursor.fast_executemany = True
        cursor.executemany(update_stmt, df_update.values.tolist())
        conn.commit()
    
    print('data updated')

def main():
    Extract(LINK)
    print('Data Loaded.')

#using json config to load hidden variables like link or sql names
jsonConfig = open('Fire.config.json')
config = json.load(jsonConfig)

#making global varibale from json objects
LINK                        = config['LINK']
SERVERNAME                  = config['SERVERNAME']
DATABASENAME                = config['DATABASENAME']
TABLENAME                   = config['TABLENAME']

main()
