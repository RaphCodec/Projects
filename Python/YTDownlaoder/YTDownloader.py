from pytube import YouTube
from datetime import datetime
import tomli
import traceback

log = open('YTDownloader.log.txt','w')

# Function to get user input restricted to "audio" or "cideo"
def restricted_input(prompt):
    while True:
        user_input = input(prompt).lower()
        if user_input == 'audio' or user_input == 'video':
            return user_input
        else:
            print("Invalid input. Please enter 'audio' or 'video'.")

def main():
    file_type = restricted_input('Would you like Audio or Video?')
    ytDownlaod(url = input('Enter a youtube link:'),file_type=file_type)

def ytDownlaod(url, file_type):
    yt = YouTube(url) #creates Youtube object

    if file_type == 'audio':
        yd = yt.streams.filter(only_audio=True).first() #creates mp4 audio file
    else:
        yd = yt.streams.get_highest_resolution() #creates mp4 vidoe file
    #sends file to desired directory
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