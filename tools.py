import asyncio
import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains


def disable_modal_window(driver):
    try:
        driver.find_element(By.ID, "dialog")
        time.sleep(1)
        driver.execute_script("document.getElementById('dialog').style.display = 'none';")
        time.sleep(0.5)
        driver.execute_script("document.getElementsByTagName('tp-yt-iron-overlay-backdrop')[0].style.display = 'none';")
    except:
        ...


def click_on_video_update(driver, wait, element, viewing_time):
    try:
        action = ActionChains(driver)
        driver.execute_script(f"window.scrollTo(0, {element.location.get('y')})")
        driver.execute_script("arguments[0].click();", element)
        wait.until(ec.presence_of_element_located((By.CLASS_NAME, "style-scope ytd-watch-metadata")))

        body = driver.find_element(By.TAG_NAME, 'body')
        action.move_to_element_with_offset(body, 0, 0)

        time.sleep(5)
        action.move_by_offset(-500, 500).click().perform()

        now = time.time() + viewing_time + 20
        i = 0
        while time.time() < now:
            i += 1
            print(i)
            time.sleep(1)
            try:
                advertising_btn_s = driver.find_elements(By.CLASS_NAME, 'ytp-ad-image')
            except Exception as e:
                advertising_btn_s = None

            try:
                premium_block = driver.find_element(By.CLASS_NAME, 'style-scope ytd-mealbar-promo-renderer')
            except Exception as e:
                premium_block = None

            if premium_block:
                button = premium_block.find_element(By.ID, "dismiss-button")
                button.click()

            time.sleep(1)
            try:
                div = driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-slot")
                button = div.find_element(By.TAG_NAME, "div")

            except NoSuchElementException:
                continue
            if button:
                wait.until(ec.element_to_be_clickable(button))
                if button.text.find("ропусти"):
                    button.click()

    finally:
        time.sleep(viewing_time)
        driver.close()
