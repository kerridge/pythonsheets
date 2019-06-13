import requests
from bs4 import BeautifulSoup

# cast data to ints
def clean_data(weather_list):
    vals = []
    for item in weather_list:
        temp = item.get_text()
        # if no val, set to 0 || else cast to int
        temp = 0 if temp == '-' else int(temp)
        vals.append(temp)
    return vals


# request the page and parse the html
def do_scrape(field):
    # request the html, grab all table rows from it
    print(f'Scraping data from ({field.url})')
    page = requests.get(field.url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_rows = soup.find_all('tr')

    # locate our dang snow row as a start index
    for idx, row in enumerate(table_rows):
        if 'data-row' in row.attrs:
            if row.attrs['data-row'] == 'snow':
                starting_row = idx

    # update the objects member variables with data
    field.snow = clean_data(list(table_rows[starting_row].children)[1:22])
    field.rain = clean_data(list(table_rows[starting_row+1].children)[1:22])
    field.max_temp = clean_data(list(table_rows[starting_row+2].children)[1:22])
    field.min_temp = clean_data(list(table_rows[starting_row+3].children)[1:22])
    field.wind_chill = clean_data(list(table_rows[starting_row+4].children)[1:22])


