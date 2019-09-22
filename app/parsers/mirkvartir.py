# from django.conf import settings
# from app.parsers.utils import *
from utils import *
from urllib.parse import urlencode, quote_plus
import settings
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import xlsxwriter

import re
from selenium.webdriver.chrome.options import Options
from os import path

def parse_mirkvartir(params):
    (TYPE, NUMBER_OF_ELEMENTS, CITY, ROOM_AREA_MIN, ROOM_AREA_MAX, MIN_PRICE, MAX_PRICE) = params
    LOCATION = settings.CITIES[CITY]
    print(LOCATION)
    FILENAME = 'mirkvartir.xlsx'

    # setup browser
    driver = webdriver.Chrome(chrome_options=get_options())

    # get page
    PROTOCOL = "https://"
    DOMAIN = 'arenda.' if TYPE == 0 else ''
    SITE = key_by_value(settings.SOURCE_SITES, 'Mirkvartir')
    PAGE = settings.SOURCE_PAGES_RENT['Mirkvartir'] if TYPE == 0 else settings.SOURCE_PAGES_SELL['Mirkvartir']
    driver.get(PROTOCOL+DOMAIN+SITE+'/'+quote_plus(LOCATION).lower()+'/'+quote_plus(PAGE).lower())
    print(PROTOCOL+DOMAIN+SITE+'/'+quote_plus(LOCATION).lower()+'/'+quote_plus(PAGE).lower())


    # get first elements
    els = driver.find_elements_by_class_name('b-flat')

    # get additional elements by scrolling page (works slowly)
    # if len(els) < NUMBER_OF_ELEMENTS:
    #     itr = 0
    #     while(len(els) >= NUMBER_OF_ELEMENTS or itr >= settings.MAX_SCROLLS):
    #         # scrolling go down to the page
    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         # get elements
    #         els = driver.find_elements_by_class_name('item__line')
    #         # increase counter
    #         itr += 1

    # get info elements
    itr = 0
    hlinks = []
    for el in els:

        # get hyperlink
        try:
            hlinkel = el.find_element_by_class_name('offer-title')
            hlink = hlinkel.get_attribute('href')
            if re.search(re.compile('[0-9]{9}'),hlink):
                hlinks.append(hlink)
                print(hlink)
        except StaleElementReferenceException:
            pass

        # control number of objects to load
        itr += 1
        if itr >= NUMBER_OF_ELEMENTS:
            break

    # prepare document
    workbook, worksheet = prepare_workbook(FILENAME)

    row = 1
    for hlink in hlinks:
        # go to page
        driver.get(hlink)
        sleep(10)
        print(driver.page_source)

        # get summary
        summary = driver.find_element_by_class_name('b-title').text
        # rooms = summary[0]
        # square = summary[1]
        # floor = summary[2]

        # get another
        adress = driver.find_element_by_class_name('l-object-address').text
        price = driver.find_element_by_class_name('prices').text
        contact = driver.find_element_by_class_name('company').text

        element = driver.find_element_by_class_name('company').find_element_by_class_name('b-seller-phone')
        print(element.text)
        # ActionChains(driver).move_to_element(element).click(element).perform()
        # sleep(1)
        # phone = driver.find_element_by_class_name('b-seller-phone m-opened').text

        # write info into the table
        # worksheet.write_string(row,0,adress)
        # worksheet.write_string(row,1,square)
        # worksheet.write_string(row,2,price)
        # worksheet.write_string(row,3,floor)
        # worksheet.write_string(row,4,phone)
        # worksheet.write_string(row,5,contact)
        # worksheet.write_url(row,6,hlink)
        # row += 1

        # print
        print(summary)
        print(adress)
        print(price)
        print(contact)
        # print(phone)
        print('***')

    # autofit page
    # for i in range(0,7):
    #     set_column_autowidth(worksheet,i)

    # close session
    workbook.close()
    driver.close()
    driver.quit()

    return path.realpath(FILENAME)

if __name__ == "__main__":
    TYPE = 0
    NUMBER_OF_ELEMENTS = 1
    CITY = 'Moscow'
    ROOM_AREA_MIN = 10
    ROOM_AREA_MAX = 100
    MIN_PRICE = 1000
    MAX_PRICE = 10000
    params = (TYPE, NUMBER_OF_ELEMENTS, CITY, ROOM_AREA_MIN, ROOM_AREA_MAX, MIN_PRICE, MAX_PRICE)
    parse_mirkvartir(params)
