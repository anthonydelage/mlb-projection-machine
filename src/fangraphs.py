import os
import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

from exceptions import UnsupportedProjectionTypeException

FANGRAPHS_PROJECTION_URL = 'https://www.fangraphs.com/projections.aspx?pos=all&stats={stats}&type={projection_type}'
PROJECTION_SYSTEMS = [
    'steamer',
    'steamer600',
    'zips',
    'thebat',
    'atc',
    'fangraphsdc'
]
POPUP_WAIT = 5
EXPORT_WAIT = 10
DOWNLOAD_WAIT = 2


def create_chrome_driver(download_path, headless=True):
    options = webdriver.ChromeOptions()
    prefs = {}

    prefs['profile.default_content_settings.popups'] = 0
    prefs['download.default_directory'] = download_path
    options.add_experimental_option('prefs', prefs)

    if headless:
        options.add_argument('headless')

    return webdriver.Chrome(chrome_options=options)


def download_projection(projection_type, data_path):
    if projection_type not in PROJECTION_SYSTEMS:
        raise UnsupportedProjectionTypeException(
            'projection_type must be one of {systems}'.format(
                systems=', '.join(PROJECTION_SYSTEMS)
            )
        )

    print('Getting projections for {system}'.format(system=projection_type))

    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), data_path))
    driver = create_chrome_driver(download_path=full_path)

    for stats in ['bat', 'pit']:
        url = FANGRAPHS_PROJECTION_URL.format(
            stats=stats,
            projection_type=projection_type
        )
        driver.get(url)

        # Close signup popup
        try:
            WebDriverWait(driver, POPUP_WAIT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.my_popup_close'))
            ).click()
        except TimeoutException:
            pass

        # Export data
        WebDriverWait(driver, EXPORT_WAIT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#ProjectionBoard1_cmdCSV'))
        ).click()

        # Rename downloaded file
        while 'FanGraphs Leaderboard.csv' not in os.listdir(full_path):
            sleep(DOWNLOAD_WAIT)

        file_path = os.path.join(full_path, 'FanGraphs Leaderboard.csv')
        new_path = os.path.join(full_path, 'fangraphs_{projection_type}_{stats}.csv'.format(
            stats=stats,
            projection_type=projection_type
        ))
        os.rename(file_path, new_path)

    driver.close()
    return

def download_projections(systems, data_path):
    for system in systems:
        if system['use']:
            download_projection(system['name'], data_path)

    return
