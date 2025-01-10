from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
import time
import traceback

def perform_actions_on_new_tab(driver):
    try:
        # Wait for the availability box to be present
        availability_box_xpath = "//div[contains(@class, 'box-shadow-availability')]"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, availability_box_xpath)))
        print("Availability box is present.")

        # Check the visibility of the date availability elements
        date_available_xpath = "//div[@id='js-area-date-filter']//div[contains(@id, 'js-date-available')]"
        date_unavailable_xpath = "//div[@id='js-area-date-filter']//div[contains(@id, 'js-date-unavailable')]"

        date_available = driver.find_element(By.XPATH, date_available_xpath)
        date_unavailable = driver.find_element(By.XPATH, date_unavailable_xpath)

        expected_text = "Dates selected are available"

        if date_available.is_displayed():
            date_available_text = date_available.get_attribute('innerText')
            print(date_available_text)
            if expected_text in date_available_text:
                print("Dates selected are available.")
            else:
                print(f"Expected text not found. Found text: {date_available_text}")
        elif date_unavailable.is_displayed():
            print("Dates selected are not available.")
        else:
            print("Unable to determine the availability of the selected dates.")


        # Add any other actions you need to perform on the new tab here
        time.sleep(2)  # Adding a delay to simulate more actions
    except Exception as e:
        print(f"An error occurred while performing actions on the new tab: {str(e)}")
        print(traceback.format_exc())