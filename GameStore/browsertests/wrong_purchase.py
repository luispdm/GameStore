from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
"""
Luigi
This tests tries to stress the purchasing system.

NOTE:
- to perform correctly the test, you SHOULD ALREADY HAVE the FIRST game of the store in your "My Games" section.
- to run the following on Google Chrome, you need to download the proper driver on the Selenium website.
"""

delay = 10
testUsername = "user83"
testPassword = "00000000"
loginAddress = "http://fast-badlands-87500.herokuapp.com/accounts/login"
storeAddress = "http://fast-badlands-87500.herokuapp.com/store"
cartAddress = "http://fast-badlands-87500.herokuapp.com/store/cart"
pathToChromeDriver = '/Users/luigidigirolamo/Downloads/chromedriver'
xPathButtonCart = "//*[@id=\"tableId\"]/tbody/tr[2]/td[7]/button"
idModal = "modalMessage"

showAlert = "document.getElementById('modalInfo').style.display = 'block';"
removeAlert = "document.getElementById('modalInfo').style.display = 'none';"

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

    # 1st stress test is: ordering two times the same game (in the same order)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, xPathButtonCart)))
        driver.find_element_by_xpath(xPathButtonCart).click()
        print("Wait performed")  # we need to wait the button to appear
    except TimeoutException as e:
        print("Message timeout!")
    except NoSuchElementException as nsee:
        print("XPATH not found! Game already purchased?")
    try:
        driver.execute_script(removeAlert)  # if we don't remove the alert, the driver won't find the button
        driver.find_element_by_xpath(xPathButtonCart).click()
        driver.execute_script(showAlert)
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, idModal)))
        print("Game already purchased, the stress test went good.")
    except TimeoutException as e:
        print("Message timeout!")
    except NoSuchElementException as nsee:
        print("XPATH not found!")

    # 2nd stress test: execute JS to force the cart having a game already purchased
    driver.execute_script(removeAlert)
    driver.execute_script("add_game_cart(1);")
    driver.get(cartAddress)
    elem = driver.find_element_by_class_name("form-signin").size
    if elem.__len__() == 2:  # 2 elements because the footer is inside the div
        print("Test is fine, game already purchased NOT added to the cart")
    else:
        print("You haven't got this game previously")

    # 3rd stress test: try to make an order with empty cart
    try:
        driver.find_element_by_class_name("gameRemove").click()
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-success")))
        driver.find_element_by_class_name("btn-success").click()
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-warning")))
        print("Order not created!")
    except TimeoutException:
        print("Cart was empty and order created, this shouldn't happen...")
    except NoSuchElementException as nsee:
        print("Button(s) not found!")
    except UnexpectedAlertPresentException:  # this alert makes no sense even if the test at this point went good
        print("Order not created!")
    driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise


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

    # 1st stress test is: ordering two times the same game (in the same order)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, xPathButtonCart)))
        driver.find_element_by_xpath(xPathButtonCart).click()
        print("Wait performed")  # we need to wait the button to appear
    except TimeoutException as e:
        print("Message timeout!")
    except NoSuchElementException as nsee:
        print("XPATH not found! Game already purchased?")
    try:
        driver.execute_script(removeAlert)  # if we don't remove the alert, the driver won't find the button
        driver.find_element_by_xpath(xPathButtonCart).click()
        driver.execute_script(showAlert)
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, idModal)))
        print("Game already purchased, the stress test went good.")
    except TimeoutException as e:
        print("Message timeout!")
    except NoSuchElementException as nsee:
        print("XPATH not found!")

    # 2nd stress test: execute JS to force the cart having a game already purchased
    driver.execute_script(removeAlert)
    driver.execute_script("add_game_cart(1);")
    driver.get(cartAddress)
    elem = driver.find_element_by_class_name("form-signin").size
    if elem.__len__() == 2:  # 2 elements because the footer is inside the div
        print("Test is fine, game already purchased NOT added to the cart")
    else:
        print("You haven't got this game previously")

    # 3rd stress test: try to make an order with empty cart
    try:
        driver.find_element_by_class_name("gameRemove").click()
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-success")))
        driver.find_element_by_class_name("btn-success").click()
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-warning")))
        print("Order not created!")
    except TimeoutException:
        print("Cart was empty and order created, this shouldn't happen...")
    except NoSuchElementException as nsee:
        print("Button(s) not found!")
    except UnexpectedAlertPresentException:
        print("Order not created!")
    driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise