import os
from datascraper.module1 import energy_scraper

scraper = energy_scraper()

def test_json_present():
    scraper.check_new()
    assert os.path.exists('datetime.json')

def test_status_code():
    scraper.download()
    assert scraper.status_code == 200

def test_data_cleaned():
    scraper.clean_data()
    assert scraper.df.shape > (0,0)
    assert isinstance(scraper.df.index, pd.DatetimeIndex) == True

def test_csv_created():
    scraper.save()
    assert os.path.exists('cleaned_energy_data.csv')

