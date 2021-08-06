#TODO: Create documentation for the code
#      Move the functions to a separate script and import it here as a module

import logging

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import TimeoutException

from time import sleep
from datetime import datetime, time, date, timedelta
import pause


'''
PSEUDOCODE

#prepare everything

#pause until 5:59 PM

while True:
    #open the preparation website

    #pause until 6:00 PM

    #do eveything

    #close driver

    #pause until 5:59 PM next day


'''

#FIXME: Remove this when done
URL = "C:\\Program Files (x86)\\chromedriver.exe"

#TODO:
# * Add more documentation + create function to make it more modular
# * Improve code for running 24/7

TIMEOUT = 60

TIMESLOT_TEXT = "5:45 PM"
if date.today().weekday() in [3, 4]:
    TIMESLOT_TEXT = "1:00 PM"

logging.basicConfig(format="%(asctime)s [%(levelname)s] - %(message)s",
                    encoding='utf-8',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler("/var/log/gymbot.log"),
                        logging.StreamHandler()
                    ])

#TODO: think of a better way to do this... try/catch thingy
driver = None

#HELPER FUNCTION:
#TODO: Move to a module script instead

def prepareWebsite():
    logging.info("Creating a webdriver")
    #FIXME: Remove URL when done testing
    driver = webdriver.Chrome()
    logging.info("Opening the reservation website")
    driver.get("https://reservation.frontdesksuite.ca/rcfs/richcraftkanata/Home/Index?pageid=b3b9b36f-8401-466d-b4c4-19eb5547b43a&culture=en&uiculture=en")
    driver.get("https://reservation.frontdesksuite.ca/rcfs/richcraftkanata/ReserveTime/StartReservation?pageId=b3b9b36f-8401-466d-b4c4-19eb5547b43a&buttonId=d4c0e956-e659-46b1-9880-606dc8cd81da&culture=en&uiCulture=en")
    #if the link above doesn't redirect us to the time selection page, then click the Confirm button
    if "TimeSelection" not in driver.current_url:
        logging.info("Clicking the 'Submit' button")
        button = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "submit-btn")))
        ActionChains(driver).move_to_element(button).click(button).perform()
    return driver

def reserveSpot(driver):
    #logging.info("Refreshing the page")
    #driver.refresh()
    logging.info("Clicking the timeslot")
    timeslot = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title.title-padded.d-flex")))[-1]
    timeslot.click()
    timeslot.find_element_by_xpath("./div/span")
    logging.info("Date: " + timeslot.text)

    timebox = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), '" + TIMESLOT_TEXT + "')]")))[-1]
    #logging.info("Test: " + str(timebox.text))
    #imebox.find_element_by_xpath("..")
    logging.info("Time: " + timebox.text)
    timebox = timebox.find_element_by_xpath("..")
    if timebox.is_enabled():
        ActionChains(driver).move_to_element(timebox).click(timebox).perform()
        logging.info("Clicking on the time slot.")
    else:
        logging.info("Button is disabled... ending program")
        driver.close()
        return

    logging.info("Waiting for the next page to load...")
    #Phone
    phone = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "telephone")))
    #email
    email = driver.find_element_by_id("email")
    #name
    name = driver.find_element_by_id("field4330")
    #submit
    submit = driver.find_element_by_id("submit-btn")

    logging.info("Filling information and submitting")
    ActionChains(driver).move_to_element(phone).send_keys_to_element(phone, "***REMOVED***") \
                        .move_to_element(email).send_keys_to_element(email, "***REMOVED***") \
                        .move_to_element(name).send_keys_to_element(name, "***REMOVED***") \
                        .move_to_element(submit).click(submit) \
                        .perform()

    logging.info("Waiting for confirmation... will timeout in " + str(TIMEOUT) + " seconds")
    sleep(TIMEOUT)
    if "OverMaxReservationCount" in driver.current_url:
        logging.info("Time has already been reserved")
    if "Confirmed" in driver.current_url:
        logging.info("Reservation Confirmed!")
    #WebDriverWait(driver, 60*2).until(EC.url_contains("Confirmed"))
    driver.close()

def main():
    try:
        #Time to load the page
        #prepare = tz.localize(datetime.combine(datetime.today(), time(12+5, 59)))
        #logging.info("Prepare until: " + str(prepare))
        #pause.until(prepare)

        #Time to refresh the page and click the time slot
        opens = datetime.combine(datetime.today(), time(12+6, 00, 1))
        logging.info("Setting the opening at " + str(opens))
        pause.until(opens)

        while True:
            driver = prepareWebsite()
            reserveSpot(driver)

            #Wait for tomorrow
            sleepUntilTomorrow = datetime.combine((datetime.today() + timedelta(days=1)), time(12+6, 00, 1))
            logging.info("Sleeping until tomorrow: " + str(sleepUntilTomorrow))
            pause.until(sleepUntilTomorrow)  
    except:
        logging.exception("Unexpected exception...")
        raise
    finally:
        logging.info("Closing driver")
        if driver is not None:
            driver.close()

if __name__ == "__main__":
    main()