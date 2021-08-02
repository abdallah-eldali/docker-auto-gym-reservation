from sys import platform
import os
import logging

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import TimeoutException

from datetime import datetime, time, date
from pytz import timezone
import pause

#TODO: Maybe look into SeleniumBase to make this easier after done
#Change the name of the file + move it to a separete working directory and push it to git

def main():
    try:
        TIMEOUT = 15

        TIMESLOT_TEXT = "5:45 PM"
        if date.today().weekday() in [3, 4]:
            TIMESLOT_TEXT = "1:00 PM"

        logging.basicConfig(format='%(asctime)s - %(message)s',
                            level=logging.INFO,
                            datefmt='%Y-%m-%d %H:%M:%S')

        logging.info("Creating a webdriver")
        driver = webdriver.Chrome()
        logging.info("Opening the reservation website")
        driver.get("https://reservation.frontdesksuite.ca/rcfs/richcraftkanata/Home/Index?pageid=b3b9b36f-8401-466d-b4c4-19eb5547b43a&culture=en&uiculture=en")
        driver.get("https://reservation.frontdesksuite.ca/rcfs/richcraftkanata/ReserveTime/StartReservation?pageId=b3b9b36f-8401-466d-b4c4-19eb5547b43a&buttonId=d4c0e956-e659-46b1-9880-606dc8cd81da&culture=en&uiCulture=en")
        logging.info("Clicking the 'Submit' button")
        button = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "submit-btn")))
        ActionChains(driver).move_to_element(button).click(button).perform()

        logging.info("Clicking the timeslot")
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title.title-padded.d-flex")))[-1].click()
    

    
    except:
        logging.exception("Unexpected exception...")
        raise
    finally:
        logging.info("Closing driver")
        driver.close()



if __name__ == "__main__":
    main()