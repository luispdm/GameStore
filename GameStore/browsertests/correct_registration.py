from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
"""
Luigi
This file simply register a user in a correct way.

NOTE: to run the following on Google Chrome, you need to download the proper driver on the Selenium website.
"""


delay = 6
testEmail = "testemail90@email.com"
testUsername = "webuser131112"
registerAddress = "http://fast-badlands-87500.herokuapp.com/accounts/register"

# Testing registration on Firefox
try:

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # registration's page
    driver.get(registerAddress)

    driver.find_element_by_id("id_email").send_keys(testEmail)
    driver.find_element_by_id("id_username").send_keys(testUsername)
    driver.find_element_by_id("id_password1").send_keys("12345678")
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys("12345678")
    lastOne.submit()

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
        print("Registration completed")
    except TimeoutException:
        print("Registration failed")
    finally:
        driver.get(registerAddress)

        # now we try to add a user that already exists
        driver.find_element_by_id("id_email").send_keys(testEmail)
        driver.find_element_by_id("id_username").send_keys(testUsername)
        driver.find_element_by_id("id_password1").send_keys("12345678")
        lastOne = driver.find_element_by_id("id_password2")
        lastOne.send_keys("12345678")
        lastOne.submit()
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
            print("Double username and email")
        except TimeoutException:
            print("Registration completed: the user has just been created")
        finally:
            driver.quit()
except FileNotFoundError:
    raise
except Exception:
    raise


# Test registration on Chrome
testEmail = "testemail273@email.com"
testUsername = "webuser2212"

try:

    # To test chrome, you need to download the proper driver
    path = '/Users/luigidigirolamo/Downloads/chromedriver'
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(path)

    # registration's page
    driver.get(registerAddress)

    # here we try with the wrong email format
    driver.find_element_by_id("id_email").send_keys(testEmail)
    driver.find_element_by_id("id_username").send_keys(testUsername)
    driver.find_element_by_id("id_password1").send_keys("12345678")
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys("12345678")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
        print("Registration completed")
    except TimeoutException:
        print("Registration failed")
    finally:
        driver.get(registerAddress)

        # now we try to add a user that already exists
        driver.find_element_by_id("id_email").send_keys(testEmail)
        driver.find_element_by_id("id_username").send_keys(testUsername)
        driver.find_element_by_id("id_password1").send_keys("12345678")
        lastOne = driver.find_element_by_id("id_password2")
        lastOne.send_keys("12345678")
        lastOne.submit()
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
            print("Double username and email")
        except TimeoutException:
            print("Registration completed: the user has just been created")
        finally:
            driver.quit()
except FileNotFoundError:
    raise
except Exception:
    raise
