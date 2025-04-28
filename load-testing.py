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
from concurrent.futures import ThreadPoolExecutor

# Options
br_headless = False # or True (False - normal browser, True - in headless mode)
browser_JS = True # or False (True - JS enabled, False - JS disabled)
num_requests = 5 # Number of requests to send

site_url = 'https://osp6-wp652.local'
site_url_comments = 'https://osp6-wp652.local/hello'

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

if br_headless == True:
    options.headless = True
if browser_JS == False:
    options.set_preference("javascript.enabled", False)
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
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(site_url)
        print(f"Opened site: {site_url}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )

        links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        if links:
            try:
                random_page = random.choice(links)
                href = random_page.get_attribute('href')
                print(f"Attempting to open: {href}")
                random_page.click()

                WebDriverWait(driver, 10).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
            except Exception as e:
                print(f"Error clicking link: {str(e)}")

        driver.get(site_url_comments)
        print(f"Opened comments form: {site_url_comments}")

        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )

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
        time.sleep(2)

        print("Form submitted")

    except Exception as e:
        print(f"Error in worker: {str(e)}")
    finally:
        driver.quit()

def work():
    def worker_wrapper():
        try:
            worker()
        except Exception as e:
            print(f"Error in worker: {str(e)}")

    try:
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(worker_wrapper) for _ in range(num_requests)]
            for future in futures:
                future.result()  # Wait for all workers to complete
    except Exception as e:
        print(f"Error in parallel execution: {str(e)}")


if __name__ == "__main__":
    work()
