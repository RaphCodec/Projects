import mechanicalsoup
import pandas as pd
import sqlite3
from datetime import datetime
import tomli

log = open('wwechampsETL.log.txt','w')
            
def insert(table:str,df):
    #create and connect to sqlite3 database
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    #checking if table already exists and creating it if it doesn't
    tablst = cur.execute(
        f"""SELECT name FROM sqlite_master WHERE type='table'
        AND name='{table}' """).fetchall()
    conn.commit()
    
    if not tablst:
        #create table
        cur.execute(f'Create Table {table} ({",".join(df.columns)})')

    #insert data into table
    cur.executemany(f'''Insert into {table}
                        values({('?,' * len(df.columns))[:-1]})
                        ''', df.values.tolist())
        
    conn.commit()
    conn.close #close conncection

def main():

    #making broswer object and opening url
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(URL)

    #getting all the data
    td = browser.page.find_all('td')
    browser.close() #closing browser
    
    data  = [value.text.replace('\n','') for value in td]
    titles(data)
    reigns(data)

def titles(data):
    #global logmsg
    #slicing list to get data for each wwe championship change
    titles = data[data.index('WWWF World Heavyweight Championship'):data.index('Undisputed WWE Universal Championship')+2]

    cols = [
        'Names',
        'Years'
    ]
    df_dict =  {} 

    for idx, key in enumerate(cols):
        df_dict[key] = titles[idx:][::2] 

    df = pd.DataFrame(df_dict)

    #creating a column to count order of titles and act as a primary key
    df.insert(loc=0, column='TitleNum', value= df.index)

    insert(TABLE_TITLES, df)

    #logmsg += 'Titles Data Loaded.'

def reigns(data):
    #slicing list to get data for each wwe championship change
    reigns = data[data.index('Buddy Rogers'):data.index('[204]')+1] 
    
    '''deleting specific unnecessary - from data so that it can be converted to 
        a dataframe later.  These are the - found in the No. column on the webpage
         table but have a <td> tag.
        DO NOT TRY TO REPLACE ALL -
        THERE ARE SOME THAT ARE NEEDED TO COMPLETE ROWS'''
    del reigns[reigns.index('Antonio Inoki') + 9]
    del reigns[reigns.index('Ted DiBiase') + 9]
    del reigns[reigns.index('December 3, 1991') + 8]
    del reigns[reigns.index('January 19, 1997') + 8]
    del reigns[reigns.index('June 29, 1998') + 8]
    del reigns[reigns.index('September 14, 1999') + 8]
    del reigns[reigns.index('September 17, 2006') + 8]
    del reigns[reigns.index('June 7, 2009') + 8]
    del reigns[reigns.index('July 17, 2011') + 8]
    del reigns[reigns.index('September 15, 2013') + 8]
    del reigns[reigns.index('April 6, 2014') + 8]
    del reigns[reigns.index('March 29, 2015') + 8]

    #removing unnecssary '†' character so that creating df is possible later
    reigns=list(filter(lambda a: a != '†', reigns))

    '''these are table values that identifiy the company name at the time
        However they are not needed and create extra undesired elements in the dataframe'''
    
    to_remove = ['World Wide Wrestling Federation (WWWF)',
                'National Wrestling Alliance: World Wide Wrestling Federation (WWWF)',
                'National Wrestling Alliance: World Wrestling Federation (WWF)',
                'World Wrestling Federation (WWF)',
                'World Wrestling Entertainment (WWE)',
                'WWE: SmackDown',
                'WWE: ECW',
                'WWE: Raw',
                'WWE (unbranded)']
    
    #fiding the index numbers for the values in to remove if they are in the reigns list
    indices = [idx for idx, x in enumerate(reigns) if x in to_remove]

    #the column names
    cols = ['Champion',
            'Date',
            'Event',
            'Location',
            'Reign',
            'Days',
            'DaysRecog',
            'Notes'
            ]
    #slcing reigns list to remove unwanted values and adding them to an empty list
    df_lst = []
    for idx,x in enumerate(indices):
        if idx == 0:
            cop = reigns.copy()
            cop = cop[:x -1]
            df_lst.extend(cop)
        elif x == indices[-1]:
            cop = reigns.copy()
            cop = cop[x+1:]
            df_lst.extend(cop)
        else:
            cop = reigns.copy()
            cop = cop[indices[idx-1] + 1 : x-1]
            df_lst.extend(cop)

    #adding list values to corresponding columns in a dictionary
    df_dict =  {} 

    for idx, key in enumerate(cols):
        df_dict[key] = df_lst[idx:][::9] 
    
    #dict to dataframe
    df = pd.DataFrame(df_dict)

    df = df.replace("—", None) #removing uneeded character
    
    #creating a column to count order of champs and act as a primary key
    df.insert(loc=0, column='ChampNum', value= df.index)

    #inserting data into sqlite3 database
    insert(TABLE_REIGNS,df)


if __name__ == '__main__':
    start = datetime.now()
    log.write(f'Script Started: {start}\n\n')
    with open('WWEChamps.config.toml', mode='rb') as fp:
        config = tomli.load(fp)
    URL             = config['URL']
    DB              = config['DB']
    TABLE_REIGNS    = config['TABLE_REIGNS']
    TABLE_TITLES    = config['TABLE_TITLES']

    try:
        from pprint import pformat
        print( f"Using the following config:\n\n{ pformat(config, sort_dicts=False) }" )
        log.write(f'{"*" * 70}\nUsing the following config:\n\n{ pformat(config, sort_dicts=False) }\n\n' )


        main()

        executionTime = (datetime.now()- start).total_seconds()
        print(f'Execution time in seconds: {executionTime}')
        log.write(f'\n{"*" * 70}\nScript Ended: {datetime.now()}\nExecution time in seconds: {executionTime}') 
        log.close()

    except Exception as e:
        print(e)
        log.write(f'{traceback.format_exc()}\n\n')
        executionTime = (datetime.now()- start).total_seconds()
        print(f'Execution time in seconds: {executionTime}')
        log.write(f'\n{"*" * 70}\nScript Ended: {datetime.now()}\nExecution time in seconds: {executionTime}') 
        log.close()