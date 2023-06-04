from pytube import YouTube
from datetime import datetime
import tomli
import traceback

log = open('YTDownloader.log.txt','w')

def main():
    yt = YouTube(URL)

    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=FOLDER_PATH)


if __name__ == '__main__':
    start = datetime.now()
    log.write(f'Script Started: {start}\n\n')
    with open('YTDownloader.config.toml', mode='rb') as fp:
        config = tomli.load(fp)
    URL             = config['URL']
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