from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
"""
Luigi
Various security tests (i.e. dev acting as a player and player acting as a dev)

NOTE:
- you need to provide two test usernames: one developer and one player
- to perform the 3rd test without troubles, the player must not own the game listed into the "gameAddress" variable
- to run the following on Google Chrome, you need to download the proper driver on the Selenium website.
"""

delay = 5
testDeveloper = "dev96"
testProfile = "user5"
testPassword = "00000000"
loginAddress = "http://fast-badlands-87500.herokuapp.com/accounts/login/"
logoutAddress = "http://fast-badlands-87500.herokuapp.com/accounts/logout/"
addGameAddress = "http://fast-badlands-87500.herokuapp.com/store/devzone/games/"
gameAddress = "http://fast-badlands-87500.herokuapp.com/arena/play/3/"
pathToChromeDriver = '/Users/luigidigirolamo/Downloads/chromedriver'

try:
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # login page
    driver.get(loginAddress)
    driver.find_element_by_id("id_username").send_keys(testDeveloper)
    lastOne = driver.find_element_by_id("id_password")
    lastOne.send_keys(testPassword)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "Dev Area")))
        print("Login correct")
    except TimeoutException:
        print("Wrong credentials!")

    # 1st test: login as a developer and try to play a game
    driver.get(gameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "Dev Area")))
        print("Test went good. The developer can't play!")
    except TimeoutException:
        print("PROBLEM: the developer can play or this is a player")

    # 2nd test: login as a player and try to add a game
    driver.get(logoutAddress)
    driver.get(loginAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "form-login")))
        print("Form visible")
    except NoSuchElementException:
        print("Element not visible: need a higher delay")
    driver.find_element_by_id("id_username").send_keys(testProfile)
    lastOne = driver.find_element_by_id("id_password")
    lastOne.send_keys(testPassword)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "My Games")))
        print("Login correct")
    except TimeoutException:
        print("Wrong credentials!")

    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "My Games")))
        print("Test went good. The player can't add a game!")
    except TimeoutException:
        print("PROBLEM: the player can add a game or this is a developer")

    # 3rd test: player tries to play a game he does not own
    driver.get(gameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "leaderTable")))
        print("PROBLEM: the player can play a game he does not own or he actually owns this game")
    except TimeoutException:
        print("Test went good. The player can't play a game he does not own!")
    driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise


try:
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(pathToChromeDriver)

    print("CHROME TESTING")
    # login page
    driver.get(loginAddress)
    driver.find_element_by_id("id_username").send_keys(testDeveloper)
    lastOne = driver.find_element_by_id("id_password")
    lastOne.send_keys(testPassword)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "Dev Area")))
        print("Login correct")
    except TimeoutException:
        print("Wrong credentials!")

    # 1st test: login as a developer and try to play a game
    driver.get(gameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "Dev Area")))
        print("Test went good. The developer can't play!")
    except TimeoutException:
        print("PROBLEM: the developer can play or this is a player")

    # 2nd test: login as a player and try to add a game
    driver.get(logoutAddress)
    driver.get(loginAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "form-login")))
        print("Form visible")
    except NoSuchElementException:
        print("Element not visible: need a higher delay")
    driver.find_element_by_id("id_username").send_keys(testProfile)
    lastOne = driver.find_element_by_id("id_password")
    lastOne.send_keys(testPassword)
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "My Games")))
        print("Login correct")
    except TimeoutException:
        print("Wrong credentials!")

    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, "My Games")))
        print("Test went good. The player can't add a game!")
    except TimeoutException:
        print("PROBLEM: the player can add a game or this is a developer")

    # 3rd test: player tries to play a game he does not own
    driver.get(gameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "leaderTable")))
        print("PROBLEM: the player can play a game he does not own or he actually owns this game")
    except TimeoutException:
        print("Test went good. The player can't play a game he does not own!")
    driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise