import time
import random
import string
import datetime
from datetime import datetime, timedelta
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# Options
br_headless = 'no' # or yes (no - normal browser, yes - in headless mode)
browser_JS = 'yes' # or no (yes - JS enabled, no - JS disabled)

site_url = 'https://site.loc'
site_url_comments = 'https://site.loc/hello'

# Tools ===========================================================================================================

# Move browser view to the element
def align_center(form_element):
    element1 = driver.find_element(By.ID, form_element)
    desired_y = (element1.size['height'] / 2) + element1.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script('return window.pageYOffset')
    scroll_y_by = desired_y - current_y 
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


# Generate random string for user agent
def random_string(length=8):
    chars = string.ascii_letters + string.digits + '_-'
    return ''.join(random.choices(chars, k=length)) + str(random.randint(1000, 9999))


# Tools END ========================================================================================================


# Settings browser ===================================================================================================
options = webdriver.FirefoxOptions()
options.set_preference("general.useragent.override", f"CleanTalk Bot to check connection 1.0 (https://cleantalk.org/help/cleantalk-servers-ip-addresses) {random_string()}")
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
options.add_argument('-private') # open in incognito mode

if br_headless == 'yes':
    options.headless = True
if browser_JS == 'no':
    options.set_preference("javascript.enabled", False)
driver = webdriver.Firefox(options=options)


if br_headless == 'yes':
    driver.set_window_size(2560, 1600) # для headless там делее все равно full screen
else:
    # Calculate 80% of screen size
    import tkinter as tk
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    
    width = int(screen_width * 0.9)
    height = int(screen_height * 0.9)
    
    # Position window at center of screen
    x_position = int((screen_width - width) / 2)
    y_position = int((screen_height - height) / 2)
    
    driver.set_window_size(width, height)
    driver.set_window_position(x_position, y_position)
    
    print(f"Window set to {width}x{height} (90% of screen size)")
# Settings browser END ===============================================================================================


# Functions ==========================================================================================================
def fill_comments_form():
    try:
        driver.get(site_url_comments)
        print(f"Opened comments form: {site_url_comments}")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )

        # Fill the form
        comment_textarea = driver.find_element(By.ID, "comment")
        comment_textarea.send_keys("Hello, world! " + random_string(10))
        name_input = driver.find_element(By.ID, "author")
        name_input.send_keys("John Doe")
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("john.doe@example.com")
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        # Wait for page to load
        time.sleep(2)

        print("Form submitted")

    except Exception as e:
        print(f"Error opening comments form: {str(e)}")
        return 


def worker():
        # Open the site
        driver.get(site_url)
        print(f"Opened site: {site_url}")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        
        # Get fresh list of links and click a random one
        links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        if links:
            try:
                    random_page = random.choice(links)
                    href = random_page.get_attribute('href')
                    print(f"Attempting to open: {href}")
                    random_page.click()
                    
                    # Wait for new page to load
                    WebDriverWait(driver, 10).until(
                        lambda driver: driver.execute_script('return document.readyState') == 'complete'
                    )
            except Exception as e:
                print(f"Error clicking link: {str(e)}")

        # go to page with comments form
        fill_comments_form()

def work():
    try:
        for i in range(10):
            worker()
            time.sleep(5)
        
        driver.quit()
    except Exception as e:
        print(f"Error opening site: {str(e)}")
        driver.quit()
        return 


if __name__ == "__main__":
    work()
