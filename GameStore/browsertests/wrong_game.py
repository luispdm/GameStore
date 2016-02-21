from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
"""
Luigi
In this test file we stress the input validation when adding a new game to the store.

NOTE: to run the following on Google Chrome, you need to download the proper driver on the Selenium website.
"""


delay = 10
testUsername = "dev99"
testPassword = "00000000"
loginAddress = "http://fast-badlands-87500.herokuapp.com//accounts/login"
addGameAddress = "http://fast-badlands-87500.herokuapp.com//store/devzone/games"
pathToChromeDriver = '/Users/luigidigirolamo/Downloads/chromedriver'
nameProvided = "GTA V"
urlProvided = "https://en.wikipedia.org/wiki/Gran_Turismo_6"

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

    # =========== TRY WITH BLANK NAME ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("")
    driver.find_element_by_id("id_description").send_keys("Hello")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys(40)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a name to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH BLANK DESCRIPTION ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("sss")
    driver.find_element_by_id("id_description").send_keys("")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys(40)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a description to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH BLANK URL ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("Game Name")
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys("")
    driver.find_element_by_id("id_price").send_keys(40)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a url to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH BLANK PRICE ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("Game Name")
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys()
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a price to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH BLANK LOGO ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("Game Name")
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys(40)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a logo to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH BLANK CATEGORY ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("Game Name")
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys(40)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a category to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH A NAME ALREADY PROVIDED========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys(nameProvided)
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys(30)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("This game is already available in the Store")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH A URL ALREADY PROVIDED ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("otto")
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys(urlProvided)
    driver.find_element_by_id("id_price").send_keys(30)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("The url provided already belong to a game in the Store")
    except TimeoutException:
        print("Something went wrong...")
    finally:
        driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise

# ============== SAME TESTS, BUT ON GOOGLE CHROME ==============

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

    # =========== TRY WITH BLANK NAME ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("")
    driver.find_element_by_id("id_description").send_keys("Hello")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys(40)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a name to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH BLANK DESCRIPTION ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("sss")
    driver.find_element_by_id("id_description").send_keys("")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys(40)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a description to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH BLANK URL ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("Game Name")
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys("")
    driver.find_element_by_id("id_price").send_keys(40)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a url to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH BLANK PRICE ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("Game Name")
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys()
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a price to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH BLANK LOGO ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("Game Name")
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys(40)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a logo to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH BLANK CATEGORY ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("Game Name")
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys(40)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("Please, provide a category to the game")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH A NAME ALREADY PROVIDED========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys(nameProvided)
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys("http://www.yahoo.com")
    driver.find_element_by_id("id_price").send_keys(30)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("This game is already available in the Store")
    except TimeoutException:
        print("Something went wrong...")

    # =========== TRY WITH A URL ALREADY PROVIDED ========
    driver.get(addGameAddress)
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-primary")))
        print("Wait performed")
    except NoSuchElementException:
        print("Wait need more time")
    driver.find_element_by_class_name("btn-primary").click()
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "id_name")))
        print("Wait performed")
    except ElementNotVisibleException:
        print("Wait need more time")
    driver.find_element_by_id("id_name").send_keys("otto")
    driver.find_element_by_id("id_description").send_keys("Description")
    driver.find_element_by_id("id_url").send_keys(urlProvided)
    driver.find_element_by_id("id_price").send_keys(30)
    lastOne = driver.find_element_by_id("id_logo")
    lastOne.clear()
    lastOne.send_keys("http://www.image.com")
    select = Select(driver.find_element_by_id("id__category"))
    select.select_by_visible_text("FPS")
    lastOne.submit()
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        print("The url provided already belong to a game in the Store")
    except TimeoutException:
        print("Something went wrong...")
    finally:
        driver.quit()

except FileNotFoundError:
    raise
except Exception:
    raise