from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
"""
Luigi
This file aims to tests the stability of the website in front of wrong input provided (during the user's registration).

NOTE: to run the following on Google Chrome, you need to download the proper driver on the Selenium website.
"""

delay = 6
registerAddress = "http://fast-badlands-87500.herokuapp.com//accounts/register"
correctUsername = "user1000"
correctEmail = "correctformat@email.com"
correctPwd = "00000000"

try:
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # registration's page
    driver.get(registerAddress)

    # here we try with the wrong email format
    driver.find_element_by_id("id_email").send_keys("wrongemail.com")
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys(correctPwd)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("E-mail error properly raised!")
    except TimeoutException:
        print("No error in the page")

    # try to use a username too short (minimum length is 4)
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys("usa")
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys(correctPwd)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Username error properly raised!")
    except TimeoutException:
        print("No error in the page")

    # try to use a password too short (minimum length is 8)
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys("0000")
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys("0000")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Password error properly raised!")
    except TimeoutException:
        print("No error in the page")

    # Try with passwords mismatch
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys("12345678")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Passwords mismatch properly raised!")
    except TimeoutException:
        print("No error in the page")

    # TEST with blank fields. First with email.
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys("")
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys(correctPwd)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Blank email error raised!")
    except TimeoutException:
        print("No error in the page")

    # Test with blank username
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys("")
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys(correctPwd)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Blank username error raised!")
    except TimeoutException:
        print("No error in the page")

    # Test with blank password1
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys("")
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys(correctPwd)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Blank password1 error raised!")
    except TimeoutException:
        print("No error in the page")

    # Test with blank password2
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys("")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Blank password2 error raised!")
    except TimeoutException:
        print("No error in the page")
    finally:
        driver.quit()
except FileNotFoundError:
    raise
except Exception:
    raise


try:
    path = '/Users/luigidigirolamo/Downloads/chromedriver' # To test chrome, you need to download the proper driver
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(path)

    # registration's page
    driver.get(registerAddress)

    # here we try with the wrong email format
    driver.find_element_by_id("id_email").send_keys("wrongemail.com")
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys(correctPwd)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("E-mail error properly raised!")
    except TimeoutException:
        print("No error in the page")

    # try to use a username too short (minimum length is 4)
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys("usa")
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys(correctPwd)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Username error properly raised!")
    except TimeoutException:
        print("No error in the page")

    # try to use a password too short (minimum length is 8)
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys("0000")
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys("0000")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Password error properly raised!")
    except TimeoutException:
        print("No error in the page")

    # Try with passwords mismatch
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys("12345678")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Passwords mismatch properly raised!")
    except TimeoutException:
        print("No error in the page")

    # TEST with blank fields. First with email.
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys("")
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys(correctPwd)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Blank email error raised!")
    except TimeoutException:
        print("No error in the page")

    # Test with blank username
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys("")
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys(correctPwd)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Blank username error raised!")
    except TimeoutException:
        print("No error in the page")

    # Test with blank password1
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys("")
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys(correctPwd)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Blank password1 error raised!")
    except TimeoutException:
        print("No error in the page")

    # Test with blank password2
    driver.get(registerAddress)
    driver.find_element_by_id("id_email").send_keys(correctEmail)
    driver.find_element_by_id("id_username").send_keys(correctUsername)
    driver.find_element_by_id("id_password1").send_keys(correctPwd)
    lastOne = driver.find_element_by_id("id_password2")
    lastOne.send_keys("")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Blank password2 error raised!")
    except TimeoutException:
        print("No error in the page")
    finally:
        driver.quit()
except FileNotFoundError:
    raise
except Exception:
    raise
