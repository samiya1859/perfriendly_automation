from utils.driver_setup import setup_driver
from tests.search_location import test_search_location
from tests.date_picking import select_dates_from_calendar
# from tests.property_tile_selection import click_property_tiles
from tests.property_traversing import click_property_tiles

def run_tests():
    driver = setup_driver()
    driver.maximize_window()
    url = "https://www.petfriendly.io/"
    driver.get(url)
    driver.implicitly_wait(3)

    test_search_location(driver)
    select_dates_from_calendar(driver)
    click_property_tiles(driver)

    driver.quit()

if __name__ == "__main__":
    run_tests()
