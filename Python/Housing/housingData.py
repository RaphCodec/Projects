import pandas as pd
import random
from datetime import datetime, timedelta
import string
import sqlite3
import tomli
import sqlalchemy as sq
import traceback
import platform
import psutil
import shortuuid

log = open('HousingData.log.txt','w')

# Set a random seed for reproducibility
random.seed(123)

def generate_dummy_data(num_rows):
    # Generate the main DataFrame
    descriptions = [
        '2 Story home with 2 full baths and one half bath. 2 bedrooms and 1 guest room. Open concept kitchen, with gas stove and smart refrigerator. Spacious backyard',
        '3 bedroom home. Fully furnished and carpeted. Outdoor Backyard Pool, with a depth of up to 6 feet. Large windows for ample sunlight. Property is fenced.',
        '2 family duplex. Shared backyard. Both units are furnished. Washer and dryer included in both. Easy access to transportation. 20 minutes from downtown.'
    ]

    data = {
        'ID': shortuuid.ShortUUID().random(length=4),
        'HouseName': ['House ' + str(i) for i in range(1, num_rows + 1)],
        'Description': [random.choice(descriptions) for _ in range(num_rows)],
        'OnMarketDate': [datetime(2022, 1, 1) + timedelta(days=random.randint(1, 365)) for _ in range(num_rows)],
        'SoldDate': [datetime(2022, 1, 1) + timedelta(days=random.randint(1, 365)) if random.random() < 0.5 else None for _ in range(num_rows)],
        'InitialPrice': [round(random.uniform(100000, 500000), 2) for _ in range(num_rows)],
        'SoldPrice': [round(random.uniform(80000, 600000), 2) for _ in range(num_rows)]
    }

    df = pd.DataFrame(data)
    return df

def main():
    # Generate the main DataFrame with n rows initially
    df = generate_dummy_data(100)

    # Generate the column descriptions DataFrame
    column_descriptions = pd.DataFrame([
        ['ID', 'Unique ID for each row. Cannot be null'],
        ['HouseName', 'Name for each house. Cannot be null'],
        ['Description', 'Description with 1000 characters or less'],
        ['OnMarketDate', 'Date the house went on the market'],
        ['SoldDate', 'Date the house was sold. Null if not sold yet'],
        ['InitialPrice', 'Initial asking price for the home (rounded to 2 decimal places)'],
        ['SoldPrice', 'Price the house was sold for. Could be higher, lower, or equal to initial price (rounded to 2 decimal places)']
    ], columns=['Column', 'Description'])

    # Display the main DataFrame and column descriptions DataFrame
    print("Main DataFrame:")
    print(df.head())
    print("\nColumn Descriptions DataFrame:")
    print(column_descriptions)


    database_con = f'mssql://@{SERVER}/{DATABASE}?driver={DRIVER}'
    engine = sq.create_engine(database_con, fast_executemany=True)
    con = engine.connect()

    # # Insert Data into sqlite database
    # conn = sqlite3.connect('HousingData.db')


    # Insert into SQL Server
    df.to_sql(name='HousingData', con=con, index=False, if_exists='replace', chunksize=1000)

if __name__ == '__main__':
    start = datetime.now()
    uname = platform.uname()
    log.write(f'Script Started: {start}\n\n')
    log.write(f''' System Information:
    System: {uname.system}'
    Version: {uname.version}'
    Processor: {uname.processor}
    CPU Cores: {psutil.cpu_count(logical=False)}
    CPU Threads: {psutil.cpu_count(logical=True)}
    Max Frequency: {psutil.cpu_freq().max:.2f} Mhz
    Total Memory: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB
    ''')
    print(f''' System Information:
    System: {uname.system}'
    Version: {uname.version}'
    Processor: {uname.processor}
    CPU Cores: {psutil.cpu_count(logical=False)}
    CPU Threads: {psutil.cpu_count(logical=True)}
    Max Frequency: {psutil.cpu_freq().max:.2f} Mhz
    Total Memory: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB
    ''')
    with open('HousingData.config.toml', mode='rb') as fp:
        config = tomli.load(fp)
    SERVER             = config['SERVER']
    DATABASE           = config['DATABASE']
    DRIVER             = config['DRIVER']

    try:
        from pprint import pformat
        print( f"Using the following config:\n\n{ pformat(config, sort_dicts=False) }\n\n{'*' * 70}" )
        log.write(f'Using the following config:\n\n{ pformat(config, sort_dicts=False) }\n\n{"*" * 70}' )

        main()

        executionTime = (datetime.now()- start).total_seconds()
        print(f'{"*" * 70}\nExecution time in seconds: {executionTime}')
        log.write(f'\n{"*" * 70}\nScript Ended: {datetime.now()}\nExecution time in seconds: {executionTime}') 
        log.close()

    except Exception as e:
        print(e)
        log.write(f'\n{traceback.format_exc()}\n\n')
        executionTime = (datetime.now()- start).total_seconds()
        print(f'{"*" * 70}\nExecution time in seconds: {executionTime}')
        log.write(f'\n{"*" * 70}\nScript Ended: {datetime.now()}\nExecution time in seconds: {executionTime}') 
        log.close()