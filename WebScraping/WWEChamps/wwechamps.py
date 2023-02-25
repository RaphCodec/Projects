import pandas as pd
from datetime import datetime
import sqlite3
import tomli
import traceback

log = open('log.txt', 'w')


def main():
    log.write('Connecting')
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_REIGNS}", conn)
    print(df)
    log.write()






if __name__ == '__main__':
    start = datetime.now()
    log.write(f'Script Started: {start}\n\n')
    with open('WWEChamps.config.toml', mode='rb') as fp:
        config = tomli.load(fp)
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