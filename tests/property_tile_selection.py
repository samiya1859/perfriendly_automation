from selenium.webdriver.common.by import By  
import time
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException  

def click_single_property_tile(driver):  
    # Wait for the refine page to load property tiles  
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'property-tiles')]")))  
    
    # Find the first property tile using XPath  
    property_tile = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'property-tiles')]//div[contains(@class, 'details')]//div[contains(@class, 'title')]//a[1]")))  
    
    # Scroll the tile into view  
    driver.execute_script("arguments[0].scrollIntoView();", property_tile)  

    # Try to click the property tile, handling potential exceptions  
    try:  
        property_tile.click()  
        time.sleep(4)
    except (StaleElementReferenceException, ElementClickInterceptedException):  
        print("Encountered an exception when trying to click the property tile. Retrying...")  
        # Re-fetch the property tile again in case of an error  
        property_tile = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'property-tiles')]//div[contains(@class, 'details')]//div[contains(@class, 'title')]//a[1]")))  
        driver.execute_script("arguments[0].scrollIntoView();", property_tile)  
        property_tile.click()  # Retry the click  

    # Wait for the new tab to open  
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))  

    # Switch to the new tab  
    driver.switch_to.window(driver.window_handles[1])  
    time.sleep(3)

    # TODO: Add any interactions you need to perform on the new tab  

    # Close the hybrid tab after actions are complete  
    driver.close()  

    # Switch back to the refine page  
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)



def click_property_tiles(driver, num_tiles=10):  
    # Wait for the js-tiles-container to load  
    try:  
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "js-tiles-container")))  
        print("Property tiles container loaded.")  
    except TimeoutException:  
        print("Timed out waiting for the property tiles container to load.")  
        return  
    
    # Loop through the specified number of tiles  
    for i in range(num_tiles):  
        try:  
            # Constructing the ID for the current tile  
            tile_id = f"js-item-{i}"  
            # Constructing the XPath for the anchor tag inside the details/title structure  
            property_tile_link_xpath = f"//div[@id='{tile_id}']//div[contains(@class, 'details')]//div[contains(@class, 'title')]//a"  
            print(f"Looking for tile link with XPath: {property_tile_link_xpath}")  

            # Wait for the property tile link to be clickable  
            property_tile_link = WebDriverWait(driver, 20).until(  
                EC.element_to_be_clickable((By.XPATH, property_tile_link_xpath))  
            )  
            
            # Scroll the link into view  
            driver.execute_script("arguments[0].scrollIntoView();", property_tile_link)  

            # Attempt to click the property tile link  
            property_tile_link.click()  
            time.sleep(3)

            # Wait for the new tab to open  
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))  
            print("New tab opened.") 

            # Switch to the new tab  
            driver.switch_to.window(driver.window_handles[1]) 
            print(f"Switched to the new tab: {driver.current_window_handle}")   

            # TODO: Add any interactions you want to perform on the new tab here  

            # Close the new tab after actions are complete  
            driver.close()  
            print("Closed the new tab.") 

            # Switch back to the refine page  
            driver.switch_to.window(driver.window_handles[0])
            print(f"Switched back to the main tab: {driver.current_window_handle}")  
            time.sleep(2)  
            
            # Wait for the property tiles section to reload, if necessary  
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "js-tiles-container")))  

        except (StaleElementReferenceException, ElementClickInterceptedException) as e:  
            print(f"Encountered an exception for property tile {tile_id}: {str(e)}. Retrying...")  
            continue  
        except TimeoutException as e:  
            print(f"Timeout exception occurred for tile {i}: {str(e)}")  
            print(traceback.format_exc())  
            continue  
        except Exception as e:  
            print(f"An unexpected error occurred for tile {i}: {str(e)}")  
            print(traceback.format_exc())  
            continue 


            
