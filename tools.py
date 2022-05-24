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


def get_filter_list(path_file):
    with open(path_file, "r") as f:
        return [x.strip() for x in f.readlines()]


def click_on_video_update(driver, wait, element, viewing_time):
    try:
        action = ActionChains(driver)
        driver.execute_script(f"window.scrollTo(0, {element.location.get('y')})")
        driver.execute_script("arguments[0].click();", element)
        wait.until(ec.presence_of_element_located((By.CLASS_NAME, "style-scope ytd-watch-metadata")))
        body = driver.find_element(By.TAG_NAME, 'body')
        action.move_to_element_with_offset(body, 0, 0)
        time.sleep(1)
        disable_modal_window(driver)
        time.sleep(3)
        try:
            advertising_btn_s = driver.find_elements(By.CLASS_NAME, 'ytp-ad-image')
            print(advertising_btn_s)
        except Exception as e:
            advertising_btn_s = None
        if not advertising_btn_s:
            print('NO!')
            action.move_by_offset(-500, 500).click().perform()
            time.sleep(0.4)
            driver.execute_script("document.getElementsByClassName('ytp-play-button ytp-button')[0].click();")

        now = time.time() + viewing_time + 20
        i = 0
        while time.time() < now:
            i += 1
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
                wait.until(ec.element_to_be_clickable(button)).click()
                button.click()

    finally:
        time.sleep(viewing_time)
        driver.close()


def click_on_filter(driver, wait, file_path):
    filter_list = get_filter_list(file_path)
    wait.until(ec.presence_of_element_located((By.ID, "filter-menu")))
    filter_menu = driver.find_element(By.ID, "filter-menu")
    filter_click = filter_menu.find_element(By.TAG_NAME, "a")
    filter_click.click()
    time.sleep(1)
    elements_by_class_name = filter_menu.find_elements(By.CLASS_NAME, "style-scope ytd-search-filter-renderer")

    for i, filter_name in enumerate(filter_list, 1):
        for element in elements_by_class_name:
            elements_by_tag = element.find_elements(By.TAG_NAME, "div")
            for element_tag in elements_by_tag:

                if element_tag.text.lower().count(filter_name.lower()):
                    element_tag.click()
                    time.sleep(1)
                    if i != len(filter_list):
                        filter_click.click()
                    time.sleep(1)
    return True






