


def get_days(month, year):
    if month == 2:
        if year in [2000,2004,2008,2012]: #leap years
            days = 29
        else:
            days = 28
    elif month in [9,4,6,11]:
        days = 30
    else:
        days = 31
    return days

def get_dates():
    dates = []
    for year in range(1998,2016):
        for month in range(1,13):
            days = get_days(month,year)
            for day in range(1,days+1):
                dates.append("{}-{}-{}".format(year,"{0:0=2d}".format(month),"{0:0=2d}".format(day)))
    return dates


if __name__ == '__main__':
    from selenium import webdriver
    import time
    import random
    import urllib
    import sys

    path_to_chromedriver ='/Users/Lin/Downloads/chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
    geotiff_xpath = '//*[@id="content"]/div/div[2]/div[1]/div/div[2]/div[2]/form/table/tbody/tr[1]/td/select/option[8]'
    download_url = '//*[@id="content"]/div/div[2]/div[1]/div/div[2]/div[2]/form/table/tbody/tr[5]/td/a'



    if sys.argv!=['NASA_scrape.py']:
        print('checking sys.argv')
        dates = sys.argv[1:]
    else:
        dates = get_dates()
        #putting the dates in a list means I can resume from a certain date if any problems
    for index, date in enumerate(dates):
        if index%100==0:
            browser.close()
            browser = webdriver.Chrome(executable_path = path_to_chromedriver)
        url = 'http://neo.sci.gsfc.nasa.gov/view.php?datasetId=TRMM_3B43D&date={}'.format(date)
        browser.get(url)
        time.sleep(2+random.randint(1,6))
        try:
            browser.find_element_by_xpath(geotiff_xpath).click()
            download_element = browser.find_element_by_xpath(download_url)
            download_link = download_element.get_attribute('href')
            urllib.urlretrieve(download_link, "scraped_floating_geotiffs/{}.tiff".format(date))
        except Exception:
            print(Exception)
            print(date + ' unsuccessful')
        time.sleep(1)

