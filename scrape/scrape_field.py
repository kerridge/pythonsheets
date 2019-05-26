import requests
from bs4 import BeautifulSoup

from models.field import Field

def clean_html(weather_list):
    vals = []
    for item in weather_list:
        temp = item.get_text()
        # if no val, set to 0 || else cast to int
        temp = 0 if temp == '-' else int(temp)
        vals.append(temp)
    return vals


def do_scrape(url, field):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_rows = soup.find_all('tr')

    snow = clean_html(list(table_rows[12].children)[1:22])
    rain = clean_html(list(table_rows[13].children)[1:22])
    max_temp = clean_html(list(table_rows[14].children)[1:22])
    min_temp = clean_html(list(table_rows[15].children)[1:22])
    wind_chill = clean_html(list(table_rows[16].children)[1:22])

    field.snow = snow
    field.rain = rain


