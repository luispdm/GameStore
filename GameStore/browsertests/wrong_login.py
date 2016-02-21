from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
"""
Luigi
In this test file we stress the input validation when adding a new game to the store.

NOTE: to run the following on Google Chrome, you need to download the proper driver on the Selenium website.
"""


delay = 6
testUsername = "aaaa"
testPassword = "10987653"
loginAddress = "http://fast-badlands-87500.herokuapp.com//accounts/login"
pathToChromeDriver = '/Users/luigidigirolamo/Downloads/chromedriver'

try:
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # login page
    driver.get(loginAddress)
    driver.find_element_by_id("id_username").send_keys(testUsername)
    lastOne = driver.find_element_by_id("id_password")
    lastOne.send_keys(testPassword)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-error")))
        print("Wrong login")
    except TimeoutException:
        print("User correctly logged in, something went wrong!")
    finally:
        driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise

try:
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(pathToChromeDriver)

    # login page
    driver.get(loginAddress)
    driver.find_element_by_id("id_username").send_keys(testUsername)
    lastOne = driver.find_element_by_id("id_password")
    lastOne.send_keys(testPassword)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-error")))
        print("Wrong login")
    except TimeoutException:
        print("User correctly logged in, something went wrong!")
    finally:
        driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise
