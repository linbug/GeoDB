


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

if __name__ == '__main__':
    from selenium import webdriver
    import time
    import random
    import urllib

    path_to_chromedriver ='/Users/Lin/Downloads/chromedriver'

    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
    geotiff_xpath = '//*[@id="content"]/div/div[2]/div[1]/div/div[2]/div[2]/form/table/tbody/tr[1]/td/select/option[3]'
    download_url = '//*[@id="content"]/div/div[2]/div[1]/div/div[2]/div[2]/form/table/tbody/tr[5]/td/a'
    dates = []
    for year in range(1998,2016):
        for month in range(1,13):
            days = get_days(month,year)
            for day in range(1,days+1):
                dates.append("{}-{}-{}".format(year,"{0:0=2d}".format(month),"{0:0=2d}".format(day)))
    #putting the dates in a list means I can resume from a certain date if any problems

    for date in dates[39:]:
        url = 'http://neo.sci.gsfc.nasa.gov/view.php?datasetId=TRMM_3B43D&date={}'.format(date)
        browser.get(url)
        time.sleep(2+random.randint(1,6))
        try:
            browser.find_element_by_xpath(geotiff_xpath).click()
        except:
            time.sleep(5)
            browser.find_element_by_xpath(geotiff_xpath).click()
        download_link = browser.find_element_by_xpath(download_url)

        urllib.urlretrieve( download_link.get_attribute('href'), "scraped_tiffs/{}.tiff".format(date))
        # browser.close()
        time.sleep(1)

