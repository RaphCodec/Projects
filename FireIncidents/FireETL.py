import pandas as pd
import json
import requests

pd.options.display.max_columns = None

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

    intcols = [
        'starfire_incident_id',
        'alarm_box_number',
        'dispatch_response_seconds_qy',
        'engines_assigned_quantity',
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
        'congressionaldistrict'
    ]
    print(df[intcols])

    df[intcols] = df[intcols].apply(pd.to_numeric)
    


    print(df.dtypes)


def Load():
    print('y')



LINK = 'https://data.cityofnewyork.us/resource/8m42-w767.json'
Extract(LINK)