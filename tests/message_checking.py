from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import traceback


def perform_actions_hybridtab(driver):
    try:
        availability_box_xpath = "//div[contains(@class, 'box-shadow-availability')]"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, availability_box_xpath)))
        print("Availability box is present.")

        # Locate the div with id=js-area-date-filter
        date_filter_xpath = "//div[@id='js-area-date-filter']"
        date_filter = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, date_filter_xpath)))

        # Locate the nested div inside date_filter and get the text
        nested_div_xpath = ".//div[contains(@id, 'js-date-available')]"
        nested_div = date_filter.find_element(By.XPATH, nested_div_xpath)
        nested_div_text = nested_div.get_attribute('innerText')
        print(f"Nested div found with text: {nested_div_text}")

        # Check if the div contains the expected text
        expected_text = "Dates selected are available"
        if expected_text in nested_div_text:
            print(f"Expected text found: {nested_div_text}")
        else:
            print(f"Failed to get expected text. Found text: {nested_div_text}")

        # Add any other actions you need to perform on the new tab here
        time.sleep(2)
    except Exception as e:
        print(f"An error occurred while performing actions on the new tab: {str(e)}")
        print(traceback.format_exc())