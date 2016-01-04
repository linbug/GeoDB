
from selenium import webdriver

def select_month(month):
    elements = driver.find_elements_by_class_name('ui-datepicker-current-day')
    for element in elements:
        if element.get_attribute('data-value') == month
        element.click()
        return



def select_day():



def download():


//*[@id="calendar0"]/div/table/tbody/tr[2]/td[6]/a

//*[@id="calendar0"]/div/table/tbody/tr[2]/td[4]/a

//*[@id="calendar0"]/div/table/tbody/tr[2]/td[4]

//*[@id="calendar11"]/div/table/tbody/tr[5]/td[5]











if __name__ == 'main':

    path_to_chromedriver ='/Users/Lin/Downloads/chromedriver'

    browser = webdriver.Chrome(executable_path = path_to_chromedriver)


for year in years:
    for day in all_the_days:
    url = 'http://neo.sci.gsfc.nasa.gov/view.php?datasetId=TRMM_3B43D&year={}'.format(year)

    browser.get(url)
        - select the month and day in the DOM
        - click download

