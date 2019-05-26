#import library
import gspread
#Service client credential from oauth2client
from oauth2client.service_account import ServiceAccountCredentials

# shit code to add parent directory as a package
import os, inspect, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# import ski field model
from models.field import Field

import random as rand

# builds and returns our cell range as a string
def row_selector (row_num, start_col, end_col):
    # in case somebody passes a number
    row_num = str(row_num)
    return start_col.upper() + row_num + ":" + end_col.upper() + row_num


field = Field('Coronet Peak', 'https://www.snow-forecast.com/resorts/Coronet-Peak/6day/mid')

# mock values
field.rain = rand.sample(range(30), 21)
field.snow = rand.sample(range(20, 60), 21)

sheet_name = 'snow'
current_field = 'coronet'

selectors = {
    'rain' : row_selector(1, 'B', 'V'),
    'snow' : row_selector(2, 'B', 'V'),
}


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials/drive_creds.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open(sheet_name).worksheet(field.name)


# takes a weather type string and a row selector string
# and updates a google sheets file one row per loop 
def update_row(weather_type, selector):
    if weather_type == 'snow':
        weather_vals = field.snow
    elif weather_type == 'rain':
        weather_vals = field.rain
    
    row = sheet.range(selector)

    # loop over cells updating their values
    for idx, cell in enumerate(row):
        cell.value = weather_vals[idx]
    
    sheet.update_cells(row)


def main():
    # for key, val in our row selectors
    for weather_type, row_selector in selectors.items():
        # loop over each row, batch updating
        # e.g. update_row('snow', 'B2:F2')
        update_row(weather_type, row_selector)

if __name__ == "__main__":
    main()

