import subprocess

TIFF_DIR = "scraped_tiffs"

def is_data(file_path):
    return "image data" not in subprocess.check_output(["file", "scraped_tiffs/" + file_path])

def get_file_paths():
    return subprocess.check_output(["ls", "scraped_tiffs/"]).split('\n')


# correct files look like this --> 2009-01-01.tiff: TIFF image data, big-endian
# corrupted files look like thi --> 2001-12-08.tiff: data

if __name__ == '__main__':
    #make sure to run this file from /GeoDB directory
    print("filtering dates")
    dates = filter(is_data, get_file_paths())
    print("dates filtered")

    for index,i in enumerate(dates):
        print("cleaning a date")
        dates[index] = i[:-5]

    print("about to scrape")
    subprocess.check_output(["python", "nasa_scrape.py"] + dates)
