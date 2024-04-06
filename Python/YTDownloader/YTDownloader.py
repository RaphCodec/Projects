from pytube import YouTube
from datetime import datetime
import tomli
import traceback
from loguru import logger
import json

logger.add(
    "YTDownloader.log.txt",
    format="{time:YYYY-MM-DD HH:mm:ss} {level} | {message}",
    level="INFO",
    mode="w",
)


# Function to get user input restricted to "audio" or "cideo"
def restricted_input(prompt):
    while True:
        user_input = input(prompt).lower()
        if user_input == "audio" or user_input == "video":
            return user_input
        else:
            print("Invalid input. Please enter 'audio' or 'video'.")


def main():
    file_type = restricted_input("Would you like Audio or Video?")
    ytDownlaod(url=input("Enter a youtube link:"), file_type=file_type)


def ytDownlaod(url, file_type):
    yt = YouTube(url)  # creates Youtube object

    if file_type == "audio":
        yd = yt.streams.filter(only_audio=True).first()  # creates mp4 audio file
    else:
        yd = yt.streams.get_highest_resolution()  # creates mp4 vidoe file
    # sends file to desired directory
    yd.download(output_path=FOLDER_PATH)

    logger.info("Finished Downlaoding")


if __name__ == "__main__":
    with open("YTDownloader.config.toml", mode="rb") as fp:
        CONFIG = tomli.load(fp)

    FOLDER_PATH = CONFIG["FOLDER_PATH"]

    logger.info(f"Using Config:\n{json.dumps(CONFIG, indent = 4)}\n")
    start = datetime.now()
    logger.info(f"Script Started")

    try:
        main()
        elapsed = datetime.now() - start
        logger.info(
            f"Script Ran Sucessfully. {elapsed.seconds // 3600} hours {elapsed.seconds % 3600 // 60} minutes {elapsed.seconds % 60} seconds elapsed"
        )
    except Exception as e:
        elapsed = datetime.now() - start
        logger.error(
            f"Script Failed. {elapsed.seconds // 3600} hours {elapsed.seconds % 3600 // 60} minutes {elapsed.seconds % 60} seconds elapsed"
        )
        # logger.exception(f'Error: {e}')
        """
        UNCOMMENT THE ABOVE LINE FOR A MORE DETAILED AND MORE FORMATTED ERROR MESSAGE
        """
        from traceback import format_exc

        logger.error(f"Error: {e}")
        logger.error(f"\n{format_exc()}")
