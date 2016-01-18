import subprocess
import re

def get_file_paths():
    return subprocess.check_output(["ls", "scraped_tiffs/"]).split('\n')

def process_title(title):
    if title[6]== '-':
        processed_title = title[:5] + '0' + title[5:]
    if processed_title[9] == '.':
        processed_title = processed_title[:8] + '0' + processed_title[8:]
    return subprocess.check_output(["mv", "scraped_tiffs/" + title, "scraped_tiffs/" + processed_title])

if __name__ == '__main__':
    #make sure to run this file from /GeoDB directory
    titles = get_file_paths()
    for title in titles:
        if len(title) < 15 and ".tiff" in title:
            process_title(title)
