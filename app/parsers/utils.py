# basic
def keys(dict):
    return list(dict.keys())

def values(dict):
    return list(dict.values())

def key_by_value(dict, value):
    return keys(dict)[values(dict).index(value)]

# image recognition util
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

# xlsx worksheet util
from typing import Optional
from xlsxwriter.worksheet import (
    Worksheet, cell_number_tuple, cell_string_tuple)
import xlsxwriter
from django.conf import settings
# import settings
def prepare_workbook(filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    my_dic = settings.TABLE_HEADER
    for cell, label in zip(keys(my_dic),values(my_dic)):
        worksheet.write(cell, label, bold)
    return (workbook, worksheet)


def get_column_width(worksheet: Worksheet, column: int) -> Optional[int]:
    """Get the max column width in a `Worksheet` column."""
    strings = getattr(worksheet, '_ts_all_strings', None)
    if strings is None:
        strings = worksheet._ts_all_strings = sorted(
            worksheet.str_table.string_table,
            key=worksheet.str_table.string_table.__getitem__)
    lengths = set()
    for row_id, colums_dict in worksheet.table.items():  # type: int, dict
        data = colums_dict.get(column)
        if not data:
            continue
        if type(data) is cell_string_tuple:
            iter_length = len(strings[data.string])
            if not iter_length:
                continue
            lengths.add(iter_length)
            continue
        if type(data) is cell_number_tuple:
            iter_length = len(str(data.number))
            if not iter_length:
                continue
            lengths.add(iter_length)
    if not lengths:
        return None
    return max(lengths)


def set_column_autowidth(worksheet: Worksheet, column: int):
    """
    Set the width automatically on a column in the `Worksheet`.
    !!! Make sure you run this function AFTER having all cells filled in
    the worksheet!
    """
    maxwidth = get_column_width(worksheet=worksheet, column=column)
    if maxwidth is None:
        return
    worksheet.set_column(first_col=column, last_col=column, width=maxwidth)


# selenium driver utils
from selenium.webdriver.chrome.options import Options

def get_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options
