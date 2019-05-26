# shit code to add parent directory as a package
import os, inspect, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import scrape_field as scraper
import sheets.update_field as db
from models.field import Field

coronet = Field('Coronet Peak', 'https://www.snow-forecast.com/resorts/Coronet-Peak/6day/mid')


def main():
    scraper.do_scrape(coronet)
    db.update(coronet)

if __name__ == "__main__":
    main()

print('done')