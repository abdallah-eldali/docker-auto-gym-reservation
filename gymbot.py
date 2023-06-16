#TODO: Create documentation for the code
#      Move the functions to a separate script and import it here as a module

import logging

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 

from datetime import datetime, time, date, timedelta
import pause

import sys
import logging
import whatsappMessage

#TODO:
# * Add more documentation + create function to make it more modular
# * Improve code for running 24/7

TIMEOUT = 60

# TIMESLOT_TEXT = "5:45 PM"
# if date.today().weekday() in [3, 4]:
#     TIMESLOT_TEXT = "2:15 PM"

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
    #Set up the WebDriverWait object
    driver.wait = WebDriverWait(driver, TIMEOUT)

    logging.info("Opening the reservation website")
    driver.get("https://reservation.frontdesksuite.ca/rcfs/richcraftkanata/Home/Index?pageid=b3b9b36f-8401-466d-b4c4-19eb5547b43a&culture=en&uiculture=en")
    driver.get("https://reservation.frontdesksuite.ca/rcfs/richcraftkanata/ReserveTime/StartReservation?pageId=b3b9b36f-8401-466d-b4c4-19eb5547b43a&buttonId=d4c0e956-e659-46b1-9880-606dc8cd81da&culture=en&uiCulture=en")
    #if the link above doesn't redirect us to the time selection page, then click the Confirm button
    if "TimeSelection" not in driver.current_url:
        logging.info("Clicking the 'Submit' button")
        button = driver.wait.until(EC.presence_of_element_located((By.ID, "submit-btn")))
        ActionChains(driver).move_to_element(button).click(button).perform()
    return driver

def reserveSpot(driver, nameStr, phoneStr, emailStr, weekdayTimeslot, weekendTimeslot):
    #logging.info("Refreshing the page")
    #driver.refresh()

    TIMESLOT_TEXT = weekdayTimeslot
    if date.today().weekday() in [3, 4]:
        TIMESLOT_TEXT = weekendTimeslot;

    logging.info("Clicking the timeslot")
    timeslot = driver.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title.title-padded.d-flex")))[-1]
    ActionChains(driver).move_to_element(timeslot).click(timeslot).perform()
    logging.info("Date: " + timeslot.text)

    driver.implicitly_wait(1)
    timebox = driver.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[span[contains(text(), '" + TIMESLOT_TEXT + "')]]")))[-1]
    logging.info("Time: " + TIMESLOT_TEXT)
    #timebox = timebox.find_element_by_xpath("..")
    driver.implicitly_wait(1)
    if timebox.is_displayed() and timebox.is_enabled():
        ActionChains(driver).move_to_element(timebox).click(timebox).perform()
        logging.info("Clicking on the time slot.")
    else:
        logging.info("Displayed?: " + str(timebox.is_displayed()))
        logging.info("Enabled?: " + str(timebox.is_enabled()))
        logging.info("Button is disabled... ending program")
        whatsappMessage.sendMessage("No available times for the time slot...")
        driver.close()
        return

    logging.info("Waiting for the next page to load...")
    #Phone
    phone = driver.wait.until(EC.presence_of_element_located((By.ID, "telephone")))
    #email
    email = driver.find_element_by_id("email")
    #name
    name = driver.find_element_by_id("field4330")
    #submit
    submit = driver.find_element_by_id("submit-btn")

    logging.info("Filling information and submitting")
    ActionChains(driver).move_to_element(phone).send_keys_to_element(phone, phoneStr) \
                        .move_to_element(email).send_keys_to_element(email, emailStr) \
                        .move_to_element(name).send_keys_to_element(name, nameStr) \
                        .move_to_element(submit).click(submit) \
                        .perform()

    #logging.info("Waiting for confirmation... will timeout in " + str(TIMEOUT) + " seconds")
    #sleep(TIMEOUT)
    if "OverMaxReservationCount" in driver.current_url:
        logging.info("Time has already been reserved")
        whatsappMessage.sendMessage("Spot has already been reserved")
    else:
        logging.info("Reservation Confirmed!")
        whatsappMessage.sendMessage("Successfully reserved spot")
    #WebDriverWait(driver, 60*2).until(EC.url_contains("Confirmed"))
    driver.close()

def main(nameStr, phoneStr, emailStr, weekdayTimeslot, weekendTimeslot):
    try:
        #Time to refresh the page and click the time slot
        opens = datetime.combine(datetime.today(), time(12+6, 1, 0))
        logging.info("Setting the opening at " + str(opens))
        pause.until(opens)

        while True:
            driver = prepareWebsite()
            reserveSpot(driver, nameStr, phoneStr, emailStr, weekdayTimeslot, weekendTimeslot)

            #Wait for tomorrow
            sleepUntilTomorrow = datetime.combine((datetime.today() + timedelta(days=1)), time(12+6, 1, 0))
            logging.info("Sleeping until tomorrow: " + str(sleepUntilTomorrow))
            pause.until(sleepUntilTomorrow)  
    except Exception as e:
        logging.exception("Unexpected exception...")
        whatsappMessage.sendMessage("Failure: " + str(e))
        raise e
    finally:
        logging.info("Closing driver")
        if driver is not None:
            driver.close()

# First argument is the name of the person which the reservation is made for
# Second argument is the phone number
# Third is the email
# Fourth and fifth are the preferred reservation dates
if __name__ == "__main__":
    arguments = sys.argv
    name = arguments[1]
    phone = arguments[2]
    email = arguments[3]
    weekdayTimeslot = arguments[4]
    weekendTimeslot = arguments[5]
    
    print(name, phone, email, weekdayTimeslot, weekendTimeslot)

    main(name, phone, email, weekdayTimeslot, weekendTimeslot)