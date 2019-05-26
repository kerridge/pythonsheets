#import library
import gspread
#Service client credential from oauth2client
from oauth2client.service_account import ServiceAccountCredentials

# shit code to add parent directory as a package
import os, inspect, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import random as rand

# builds and returns our cell range as a string
def row_selector (row_num, start_col, end_col):
    # in case somebody passes a number
    row_num = str(row_num)
    return start_col.upper() + row_num + ":" + end_col.upper() + row_num


# field model object
field = None

# name of our Google Sheet file
sheet_name = 'snow'

# the range of cells to grab
selectors = {
    'rain' : row_selector(1, 'B', 'V'),
    'snow' : row_selector(2, 'B', 'V'),
    'max' : row_selector(3, 'B', 'V'),
    'min' : row_selector(4, 'B', 'V'),
    'chill' : row_selector(5, 'B', 'V'),
}

# make db connection and return reference
def connect():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials/drive_creds.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and return the sheet reference
    return client.open(sheet_name).worksheet(field.name)


# takes a weather type string and a row selector string
# and updates a google sheets file one row per loop 
def update_row(weather_type, selector):
    # get our sheet reference
    sheet = connect()

    fields_to_update = {
        'snow' : field.snow,
        'rain' : field.rain,
        'max' : field.max_temp,
        'min' : field.min_temp,
        'chill' : field.wind_chill
    }

    weather_vals = fields_to_update.get(weather_type)
    
    row = sheet.range(selector)

    # loop over cells updating their values
    for idx, cell in enumerate(row):
        cell.value = weather_vals[idx]
    
    # push the update
    sheet.update_cells(row)


# this method gets called from our scraper
def update(scraped_field):
    global field 
    field = scraped_field

    # for key, val in our row selectors
    for weather_type, row_selector in selectors.items():
        # loop over each row, batch updating
        # e.g. update_row('snow', 'B2:F2')
        update_row(weather_type, row_selector)

