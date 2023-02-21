import mechanicalsoup
import pandas as pd
import sqlite3
import time

def mk_dfs(data,to_remove,cols):
    indices = [idx for idx, x in enumerate(data) if x in to_remove]

    df_lst = []
    for idx,x in enumerate(indices):
        if idx == 0:
            cop = data.copy()
            cop = cop[:x -1]
            df_lst.extend(cop)
        elif x == indices[-1]:
            cop = data.copy()
            cop = cop[x+1:]
            df_lst.extend(cop)
        else:
            cop = data.copy()
            cop = cop[indices[idx-1] + 1 : x-1]
            df_lst.extend(cop)

    df_dict =  {} 

    for idx, key in enumerate(cols):
        df_dict[key] = df_lst[idx:][::9] 

    df = pd.DataFrame(df_dict)

    return df

def repeat_values(num,char ,remove_last = True):
    if remove_last == False:
        return (char * num)
    else:
        return (char * num)[:-1]
    
def insert(table,df,vals,cols):
    #create and connect to sqlite3 database
    conn = sqlite3.connect('WWEChamps.db')
    cur = conn.cursor()
    #create table
    cur.execute(f'Create Table {table} ({cols})')

    #insert data into table
    cur.executemany(f'''Insert into {table}
                        values({vals})
                        ''', df.values.tolist())
        
    conn.commit()
    conn.close #close conncection

def main():
    url = 'https://en.wikipedia.org/wiki/List_of_WWE_Champions'

    #making broswer object and opening url
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)

    #getting all the data
    td = browser.page.find_all('td')
    browser.close() #closing browser

    data  = [value.text.replace('\n','') for value in td]

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

    '''these are table values that identifiy the coompany name at the time
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
    #creating df
    df = mk_dfs(reigns,to_remove, cols)
    
    #getting right number of values per row for insert
    vals = repeat_values(8, char='?,')
    
    #foramtting col names for insert
    cols = ','.join(cols)
    
    #inserting data into sqlite3 database
    insert('Champs',df,vals,cols)



if __name__ == '__main__':
    start = time.time()
    try:
        main()
        executionTime = (time.time()- start)
        print(f'Execution time in seconds: {executionTime}')
    except Exception as e:
        print(e)
        executionTime = (time.time()- start)
        print(f'Execution time in seconds: {executionTime}')