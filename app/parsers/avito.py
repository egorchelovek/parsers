from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import xlsxwriter
from app.parsers.utils import *
import re
from selenium.webdriver.chrome.options import Options
from os import path

def parse_avito(params):
    (TYPE, NUMBER_OF_ELEMENTS, CITY, ROOM_AREA_MIN, ROOM_AREA_MAX,, MIN_PRICE, MAX_PRICE) = params
    LOCATION = "/".join(settings.CITIES[CITY].lower())
    FILENAME = 'avito.xlsx'

    # setup browser
    driver = webdriver.Chrome(chrome_options=get_options())

    # get page
    SITE = key_by_value(settings.SOURCE_SITES, 'Avito')
    PAGE = settings.SOURCE_PAGES_RENT['Avito'] if TYPE == 0 else settings.SOURCE_PAGES_SELL['Avito']
    driver.get(SITE+LOCATION+PAGE)
    print(SITE+LOCATION+PAGE)

    # filter by COST
    min_cost_field = driver.find_element_by_xpath('//input[@data-marker="price/from"]')
    min_cost_field.send_keys(str(MIN_COST))
    max_cost_field = driver.find_element_by_xpath('//input[@data-marker="price/to"]')
    max_cost_field.send_keys(str(MAX_COST))
    button = driver.find_element_by_xpath('//button[@data-marker="search-filters/submit-button"]')
    button.click()

    # get first elements
    els = driver.find_elements_by_class_name('item__line')

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
            hlink = el.find_element_by_class_name('item-description-title-link')
            print(hlink.get_attribute('href'))
            hlinks.append(hlink.get_attribute('href'))
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

        # get phone (so much tricky!)
        button = driver.find_element_by_xpath('//a[@data-side="card"]')
        button.click()
        sleep(1)
        with open('phn.png', 'wb') as file:
            phone = driver.find_element_by_xpath('//a[@data-side="card"]')
            file.write(phone.find_element_by_tag_name('img').screenshot_as_png)
        phone = ocr_core('phn.png')
        if not re.match('\d',phone):
            continue

        # get summary
        summary = driver.find_element_by_class_name('title-info-title-text').text.split(',')
        rooms = summary[0]
        square = summary[1]
        floor = summary[2]

        # get another
        adress = driver.find_element_by_class_name('item-address__string').text
        price = driver.find_element_by_class_name('item-price').text
        contact = driver.find_element_by_class_name('seller-info-value').text

        # write info into the table
        worksheet.write_string(row,0,adress)
        worksheet.write_string(row,1,square)
        worksheet.write_string(row,2,price)
        worksheet.write_string(row,3,floor)
        worksheet.write_string(row,4,phone)
        worksheet.write_string(row,5,contact)
        worksheet.write_url(row,6,hlink)
        row += 1

        # print
        print(summary)
        print(adress)
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

# # test
# import settings
# if __name__ == "__main__":
#     parse_avito((0, 10, 1500, 10000))
