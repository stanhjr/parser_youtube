from selenium.common.exceptions import InvalidSessionIdException
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from fake_useragent import UserAgent

from tools import click_on_video, click_on_video_update
from video_settings import QUERY, SEARCH_TITLE_VIDEO, WATCHING_TIME


def get_name_search(query_name: str) -> str:
    res = query_name.split()
    if len(res) > 1:
        res = '+'.join(res)
        return res
    return query_name


def parser(login, password, ip, port, query, search_title_video, viewing_time):
    proxy_server = f"{ip}:{port}"
    proxy_options = {
        "proxy": {
            "https": f"http://{login}:{password}@{proxy_server}"
        }
    }
    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent.random}")

    driver = webdriver.Chrome("/usr/bin/chromedriver",
                              options=options,
                              seleniumwire_options=proxy_options)
    driver.maximize_window()

    driver.get(f"https://www.youtube.com/results?search_query={query}")

    wait = WebDriverWait(driver, 10)

    try:
        i = 0
        scroll = 1200

        wait.until(ec.presence_of_element_located((By.CLASS_NAME, "style-scope ytd-video-renderer")))

        elements = set(driver.find_elements(By.CSS_SELECTOR, "#video-title.ytd-video-renderer"))
        for element in elements:
            if search_title_video == element.text:
                print(i)
                print('FIND!')
                click_on_video(driver=driver, wait=wait, element=element, viewing_time=viewing_time)
                raise KeyError
        while True:

            driver.execute_script(f"window.scrollTo(0, {scroll})")
            time.sleep(0.5)
            elements2 = set(driver.find_elements(By.CSS_SELECTOR, "#video-title.ytd-video-renderer"))

            elements2.difference_update(elements)
            for element in elements2:
                if search_title_video == element.text:
                    print(i)
                    print('FIND!')
                    click_on_video_update(driver=driver, wait=wait, element=element, viewing_time=viewing_time)
                    raise KeyError
            elements = elements2
            i += 1
            scroll += 1200
    except KeyError:
        ...

    finally:
        ...
        return driver


if __name__ == '__main__':
    now = time.time()

    query = get_name_search(QUERY)

    with open("proxy.txt", "r") as f:
        try:
            i = 1
            try:
                task = []
                for line in f.readlines():
                    now_row = time.time()
                    ip, port, login, password = line.split(":")
                    driver = parser(ip=ip,
                                    password=password,
                                    login=login,
                                    port=port,
                                    query=query,
                                    search_title_video=SEARCH_TITLE_VIDEO,
                                    viewing_time=int(WATCHING_TIME))

                    i += 1
                    etc = time.time() - now_row
                    print("ROW TIME", etc)
            except InvalidSessionIdException:
                ...
            finally:
                ...
        finally:
            driver.close()
            etc = time.time() - now
            print("timer", etc)
