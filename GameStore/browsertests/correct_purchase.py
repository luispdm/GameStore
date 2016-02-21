from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
"""
Luigi
This tests performs a simple purchase.

NOTE:
- user shouldn't have the game into the "xPathButtonCart" already
- to run the following on Google Chrome, you need to download the proper driver on the Selenium website.
"""

delay = 10
testUsername = "user27"
testPassword = "00000000"
loginAddress = "http://fast-badlands-87500.herokuapp.com/accounts/login"
storeAddress = "http://fast-badlands-87500.herokuapp.com/store"
cartAddress = "http://fast-badlands-87500.herokuapp.com/store/cart"
pathToChromeDriver = '/Users/luigidigirolamo/Downloads/chromedriver'
xPathButtonCart = "//*[@id=\"tableId\"]/tbody/tr[2]/td[7]/button"

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
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "My Games")))
        print("Correct login")
    except TimeoutException:
        print("Login Failed!")
    driver.get(storeAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, xPathButtonCart)))
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xPathButtonCart)))
        driver.find_element_by_xpath(xPathButtonCart).click()
        print("Wait performed")
    except TimeoutException as e:
        print("Message timeout!")
    except NoSuchElementException as nsee:
        print("XPATH not found! Game already purchased?")
    except ElementNotVisibleException:
        print("Need to wait more time to make the item visible")
    driver.get(cartAddress)
    driver.find_element_by_class_name("btn-success").click()
    driver.find_element_by_xpath("//*[@type='submit']").click()
    driver.find_element_by_xpath("//*[@id=\"content\"]/div/form[2]/button").click()
    print("Game bought!")
    driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise

xPathButtonCart = "//*[@id=\"tableId\"]/tbody/tr[3]/td[7]/button"
try:
    # To test chrome, you need to download the proper driver
    path = '/Users/luigidigirolamo/Downloads/chromedriver'
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(path)

    # login page
    driver.get(loginAddress)
    driver.find_element_by_id("id_username").send_keys(testUsername)
    lastOne = driver.find_element_by_id("id_password")
    lastOne.send_keys(testPassword)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "My Games")))
        print("Correct login")
    except TimeoutException:
        print("Login Failed!")
    driver.get(storeAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, xPathButtonCart)))
        print("Wait performed")
    except TimeoutException as e:
        print("Message timeout!")
    except NoSuchElementException as nsee:
        print("XPATH not found! Game already purchased?")
    driver.find_element_by_xpath(xPathButtonCart).click()
    driver.get(cartAddress)
    driver.find_element_by_class_name("btn-success").click()
    driver.find_element_by_xpath("//*[@type='submit']").click()
    driver.find_element_by_xpath("//*[@id=\"content\"]/div/form[2]/button").click()
    print("Game bought!")
    driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise