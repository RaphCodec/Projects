from pytube import YouTube
from datetime import datetime
import tomli
import traceback
import glob
import os
from pathlib import Path

log = open('YTDownloader.log.txt','w')

# Function to get user input restricted to "yes" or "no"
def get_yes_no_input(prompt):
    while True:
        user_input = input(prompt).lower()
        if user_input == 'yes' or user_input == 'no':
            return user_input
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    ytDownlaod(url = input('Enter a youtube link:'))
    
    mp3 = get_yes_no_input('Would you like an mp3 download?')
    if mp3 == 'yes':
        print('Converting to mp3')
        MP3()
        print('Enjoy!')
    else:
        print('Enjoy!')

def MP3():
    #getting a list of all mp4 files in folder
    files = glob.glob(FOLDER_PATH + '/*.mp4')
    #get the last added mp4 file in the folder
    latest_file = max(files, key=os.path.getctime)
    #changing the file extension to mp3 from mp4
    p = Path(latest_file)
    p.rename(p.with_suffix('.mp3'))


def ytDownlaod(url):
    yt = YouTube(url)

    print(yt.thumbnail_url)

    yd = yt.streams.get_highest_resolution()
    yd.download(output_path=FOLDER_PATH)
    
    print('Finished Downlaoding')


if __name__ == '__main__':
    start = datetime.now()
    log.write(f'Script Started: {start}\n\n')
    with open('YTDownloader.config.toml', mode='rb') as fp:
        config = tomli.load(fp)

    FOLDER_PATH     = config['FOLDER_PATH']
    

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
        log.write(f'\n{traceback.format_exc()}\n\n')
        executionTime = (datetime.now()- start).total_seconds()
        print(f'Execution time in seconds: {executionTime}')
        log.write(f'\n{"*" * 70}\nScript Ended: {datetime.now()}\nExecution time in seconds: {executionTime}') 
        log.close()