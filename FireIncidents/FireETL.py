import pandas as pd
import json
import requests

#pd.options.display.max_columns = None

def Extract(LINK):
    #loading data from api into dataframe
    api_request = requests.get(LINK)
    api_text = api_request.text
    data = json.loads(api_text)
    df = pd.json_normalize(data)
    Transform(df)

def Transform(df):
    #Perform necessary data transformations

    #replacing Nan's with None.  Makes type transformations easier
    df = df.where(pd.notnull(df), None)

    #Standardizing some column values
    df['incident_borough'] = df['incident_borough'].replace('RICHMOND / STATEN ISLAND', 'STATEN ISLAND')
    df['alarm_box_borough'] = df['alarm_box_borough'].replace('RICHMOND / STATEN ISLAND', 'STATEN ISLAND')

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
    print(df.head())

def main():
    Extract(LINK)
    print('Data Loaded.')

#usuing json config to load hidden variables like link or sql names
jsonConfig = open('Fire.config.json')
config = json.load(jsonConfig)

LINK = config['LINK']


main()