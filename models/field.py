class Field:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    # field name
    name = ''
    # url to scrape from
    url = ''

    # weather value lists
    rain = []
    snow = []
    max_temp = []
    min_temp = []
    wind_chill = []