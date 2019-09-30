from django.conf import settings
from app.parsers.utils import *
# import settings
# from utils import *
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep
import xlsxwriter
import re
from selenium.webdriver.chrome.options import Options
from os import path

def parse_move(params):
    (TYPE, NUMBER_OF_ELEMENTS, CITY, ROOM_AREA_MIN, ROOM_AREA_MAX, MIN_PRICE, MAX_PRICE) = params
    FILENAME = 'move.xlsx'

    # setup browser
    driver = webdriver.Chrome(chrome_options=get_options())
    driver = facking_location(driver, CITY)

    # get page
    SITE = key_by_value(settings.SOURCE_SITES, 'Move')
    PAGE = settings.SOURCE_PAGES_RENT['Move'] if TYPE == 0 else settings.SOURCE_PAGES_SELL['Move']
    driver.get(SITE+PAGE)
    print(SITE+PAGE)

    # get first elements
    els = driver.find_elements_by_class_name('enshrined-items')

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
            hlink = el.find_element_by_tag_name('a')
            print(hlink.get_attribute('href'))
            hlinks.append(hlink.get_attribute('href'))
        except StaleElementReferenceException:
            pass

        break

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

        contact = driver.find_element_by_class_name('block-user__name').text
        driver.find_element_by_class_name('block-user__show-telephone_number_button-block').find_element_by_tag_name('a').click()
        phone = driver.find_element_by_class_name('block-user__show-telephone_number').text

        # get summary
        summary = driver.find_element_by_class_name('object-info__details-table ').text.split('\n')
        price = summary[1]
        floor = summary[7]
        adress = driver.find_element_by_class_name('geo-block__geo-info').text.replace('\n',', ')
        square = re.search(re.compile(',\s[\d]{2}\sм²'), \
        driver.find_element_by_class_name('object-title_page-title').text).group(0).replace(', ','')

        # write info into the table
        worksheet.write_string(row,0,adress)
        worksheet.write_string(row,1,square)
        worksheet.write_string(row,2,price)
        worksheet.write_string(row,3,floor)
        worksheet.write_string(row,4,phone)
        worksheet.write_string(row,5,contact)
        worksheet.write_url(row,6,hlink)
        row += 1

        print(adress)
        print(floor)
        print(square)
        print(price)
        print(contact)
        print(phone)
        print('***')

    # autofit page
    for i in range(0,7):
        set_column_autowidth(worksheet,i)

    # close session
    workbook.close()
    driver.close()
    driver.quit()

    return path.realpath(FILENAME)

# test
# if __name__ == "__main__":
#     TYPE = 0
#     NUMBER_OF_ELEMENTS = 10
#     CITY = 'Moscow'
#     ROOM_AREA_MIN = 10
#     ROOM_AREA_MAX = 100
#     MIN_PRICE = 1000
#     MAX_PRICE = 10000
#     params = (TYPE, NUMBER_OF_ELEMENTS, CITY, ROOM_AREA_MIN, ROOM_AREA_MAX, MIN_PRICE, MAX_PRICE)
#     parse_move(params)
