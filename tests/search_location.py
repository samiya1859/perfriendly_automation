import time  
import random  
from faker import Faker  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  

fake = Faker()  

def test_search_location(driver):  
    max_attempts = 5  
    attempt = 0  

    while attempt < max_attempts:  
        try:  
            # Wait for search input to be present  
            wait = WebDriverWait(driver, 10)  
            search_input = wait.until(  
                EC.presence_of_element_located((By.XPATH, "//input[@id='js-search-autocomplete']"))  
            )  
           
            # Generate fake location  
            fake_location = fake.city()  
            print(f"Searching for location: {fake_location}")  
            search_input.clear()  
           
            # Input the location character by character  
            for char in fake_location:  
                search_input.send_keys(char)  
                time.sleep(0.5)  
               
            # Wait for suggestions to appear  
            wait.until(EC.visibility_of_element_located((By.XPATH, "//ul[@id='js-search-items']")))  

            # Get all suggestions from the ul element  
            suggestions_list = driver.find_element(By.XPATH, "//ul[@id='js-search-items']")  
            
            # Function to get suggestions and handle stale elements  
            def get_suggestions():  
                return suggestions_list.find_elements(By.XPATH, ".//li[contains(@class, 'google-auto-suggestion-list')]")  

            suggestions = get_suggestions()  

            # Filter suggestions where data-pid is empty  
            empty_pid_suggestions = [s for s in suggestions if not s.get_attribute('data-pid')]  

            # Print all filtered suggestions for debugging  
            print(f"\nFound {len(empty_pid_suggestions)} suggestions with empty PID:")  
            for idx, suggestion in enumerate(empty_pid_suggestions, 1):  
                data_place = suggestion.get_attribute('data-place')  
                print(f"{idx}. Place: {data_place} | PID: (empty)")  

            if empty_pid_suggestions:  
                random_suggestion = random.choice(empty_pid_suggestions)  
                selected_text = random_suggestion.text  
                print(f"\nSelected suggestion with empty PID: {selected_text}")  

                # # Re-fetch the suggestions before clicking  
                # suggestions = get_suggestions()  # Re-fetch to avoid stale reference  
                # empty_pid_suggestions = [s for s in suggestions if not s.get_attribute('data-pid')]  

                # Click the suggestion  
                try:  
                    wait.until(EC.element_to_be_clickable(random_suggestion)).click()  
                except Exception as click_exception:  
                    print(f"Error clicking suggestion: {click_exception}. Retrying...")  
                    continue  # Retry the loop if clicking fails  

                time.sleep(2)  
               
                # Verify the input field has been updated  
                updated_value = search_input.get_attribute('value')  
                print(f"Updated input value: {updated_value}")  
                assert updated_value == selected_text, "Input field value does not match the selected suggestion."  
                break 
            else:  
                print("No suggestions with empty PID found, generating a new city...")  
                attempt += 1  # Increment attempt count  
       
        except Exception as e:  
            print(f"An error occurred: {str(e)}")  
            attempt += 1  # Increment attempt count  
            if attempt >= max_attempts:  
                print("Max attempts reached. Exiting the search.")  
                raise  # Reraise the exception after max attempts