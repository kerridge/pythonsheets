#import library
import gspread
#Service client credential from oauth2client
from oauth2client.service_account import ServiceAccountCredentials
# Print nicely
import pprint

import random as rand

# builds and returns our cell range as a string
def row_selector (row_num, start_col, end_col):
    # in case somebody passes a number
    row_num = str(row_num)
    return start_col.upper() + row_num + ":" + end_col.upper() + row_num


sheet_name = 'snow'
current_field = 'coronet'

# our row ranges
rain = row_selector(1, 'B', 'i')
snow = row_selector(2, 'B', 'i')

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials/drive_creds.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open(sheet_name).worksheet(current_field)

# this grabs a row of cell objects for the defined range
row = sheet.range(snow)

# loop over cells updating their values
for idx, cell in enumerate(row):
    if idx % 2 == 0:
        cell.value = rand.randint(0,20)
    else:
        cell.value = rand.randint(20, 40)

sheet.update_cells(row)

for cell in row:
    print(cell.value)
