from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
"""
Luigi
Try to edit a game not present in developer's inventory.

NOTE:
- developer shouldn't have uploaded the game with id 1 in its inventory (the url is in the "gameNotDevAddress" variable)
- to run the following on Google Chrome, you need to download the proper driver on the Selenium website.
"""


delay = 6
testUsername = "dev96"
testPassword = "00000000"
loginAddress = "http://fast-badlands-87500.herokuapp.com/accounts/login"
gameNotDevAddress = "http://fast-badlands-87500.herokuapp.com/store/devzone/edit_game/1/"
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
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "Dev Area")))
        print("Login correct")
    except TimeoutException:
        print("Wrong credentials!")
    driver.get(gameNotDevAddress)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "form-signin")))
        print("Game not developed, edit possible... SOMETHING WENT WRONG?")
    except TimeoutException:
        print("Game not developed, edit not possible. Test went OK.")
    driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise

# ============== SAME TEST, BUT ON GOOGLE CHROME ==============

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
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "Dev Area")))
        print("Login correct")
    except TimeoutException:
        print("Wrong credentials!")
    driver.get(gameNotDevAddress)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "form-signin")))
        print("Game not developed, edit possible... SOMETHING WENT WRONG?")
    except TimeoutException:
        print("Game not developed, edit not possible. Test went OK.")
    driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise