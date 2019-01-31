import time
import datetime

import openpyxl

from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC


long, lat = 0, 0

num = 115 

def openChrome():
    """open chrome to autotest"""

    # randomly swift UserAgent
    ua = UserAgent().random

    # configration
    option = webdriver.ChromeOptions()
    prefs={
        'profile.default_content_setting_values': {
            'images': 2,
            'User-Agent': ua,
            }
        }
    option.add_argument('disable-infobars')
    option.add_argument('--proxy-server=http://110.52.235.119:9999') 
    option.add_extension('adblock.crx')
    option.add_experimental_option('prefs',prefs)

    # launch chromedriver
    driver = webdriver.Chrome(chrome_options=option)
    return driver

def getData(driver, county):
    """get the data we need"""

    global long, lat

    try:
        # find the input area
        elem = driver.find_element_by_class_name('width70')

        elem.clear()
        elem.send_keys(county)

        # post this form
        driver.find_element_by_xpath("//*[@id='btnfind']").click()
    except exceptions.UnexpectedAlertPresentException:
        driver.switch_to_alert().accept()
        return 0, 0
    except exceptions.InvalidElementStateException:
        return 0, 0
    else:
        # get the data of longtitude and latitude
        try:
            WebDriverWait(driver, 100, 0.5).until_not(EC.visibility_of_element_located((By.ID, 'loading')))

            long_elem = driver.find_element_by_id('lng')
            long = long_elem.get_attribute('value')

            lat_elem = driver.find_element_by_id('lat')
            lat = lat_elem.get_attribute('value')

            print(county, 'longtitude is', long)
            print(county, 'latitude is', lat)

            return long, lat
        except Exception:
            print('error in getData!')

def getCounty(row):
    """get the counties' name"""

    try:
        file = openpyxl.load_workbook(r'source.xlsx')
        sheet = file.get_sheet_by_name('Sheet1')

        location = 'B' + str(row)

        county = sheet[location].value

        print(county + ' is ready!')
    except Exception as e:
        print(e)

    return county

def writeData(row, county, long_coor, lat_coor):
    """write counties' longtitude and latitude into a file"""

    global num

    try:
        file = openpyxl.load_workbook(r'data.xlsx')
        sheet = file.get_sheet_by_name('Sheet')

        location_1 = 'A' + str(row)
        location_2 = 'B' + str(row)
        location_3 = 'C' + str(row)

        if sheet[location_1].value == county:
            sheet[location_2] = long_coor
            sheet[location_3] = lat_coor

        print(county + ' is completed!' + ' ' + str(num))
        
        num += 1

        file.save(r'data.xlsx')
    except Exception as e:
        print(e)

def main():
    """main function"""

    starttime = datetime.datetime.now()

    driver = openChrome()

    url = "https://www.latlong.net"
    driver.get(url)
    
    for i in range(115, 135):
        try:
            county = getCounty(i)
            longtitude, latitude = getData(driver, county)
            writeData(i, county, longtitude, latitude)
        except TypeError:
            pass

    driver.close()
    endtime = datetime.datetime.now()
    
    print (endtime - starttime)


if __name__ == '__main__':
    main()

