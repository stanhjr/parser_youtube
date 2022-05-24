import time

from selenium.common.exceptions import InvalidSessionIdException
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager

from tools import click_on_video_update, disable_modal_window


def get_name_search(query_name: str) -> str:
    res = query_name.split()
    if len(res) > 1:
        res = '+'.join(res)
        return res
    return query_name


def parser(login, password, ip, port, query, search_title_video, viewing_time, time_scroll):
    proxy_server = f"{ip}:{port}"
    proxy_options = {
        "proxy": {
            "https": f"http://{login}:{password}@{proxy_server}"
        }
    }

    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent.random}")

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options, seleniumwire_options=proxy_options)

    driver.maximize_window()

    driver.get(f"https://www.youtube.com/results?search_query={query}")

    wait = WebDriverWait(driver, 10)

    try:
        now_time = time.time() + int(time_scroll)
        i = 0
        scroll = 1200
        disable_modal_window(driver=driver)
        wait.until(ec.presence_of_element_located((By.CLASS_NAME, "style-scope ytd-video-renderer")))

        elements = set(driver.find_elements(By.CSS_SELECTOR, "#video-title.ytd-video-renderer"))
        for element in elements:
            if search_title_video == element.text:
                print(i)
                print('FIND!')
                click_on_video_update(driver=driver, wait=wait, element=element, viewing_time=viewing_time)
                raise KeyError
        while True:
            if time.time() > now_time:
                raise KeyError
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

    driver = None
    now = time.time()

    settings = []
    with open("settings.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            settings.append(line.replace("\n", ""))

    query = get_name_search(settings[0])
    search_title_video = settings[1]
    watching_time = settings[2]
    time_scroll = settings[3]
    print(settings)

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
                                    search_title_video=search_title_video,
                                    viewing_time=int(watching_time),
                                    time_scroll=time_scroll)

                    i += 1
                    etc = time.time() - now_row
                    print("ROW TIME", etc)
            except InvalidSessionIdException:
                ...
            finally:
                ...
        finally:
            if driver:
                driver.close()
            etc = time.time() - now
            print("timer", etc)