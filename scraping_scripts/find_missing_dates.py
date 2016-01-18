import glob
import NASA_scrape

dates = NASA_scrape.get_dates()

files = []
for file in glob.glob("scraped_floating_geotiffs/*.tiff"):
    files.append(file[file.find("/")+1:file.find(".")])

if __name__ == '__main__':
    for date in dates:
        if date not in files:
            print(date)