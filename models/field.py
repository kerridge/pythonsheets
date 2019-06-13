class Field:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    # field name
    name = ''
    # url to scrape from
    url = ''

    # weather value lists
    rain = list()
    snow = list()
    max_temp = list()
    min_temp = list()
    wind_chill = list()