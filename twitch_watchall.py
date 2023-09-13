from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

service_obj = Service("path_to_your_chromedriver")
driver = webdriver.Chrome(service=service_obj)
url = driver.command_executor._url
session_id = driver.session_id
driver = webdriver.Remote(command_executor=url, desired_capabilities={})
time.sleep(1)
driver.session_id = session_id


def get_info():
    driver.get("https://twitch.facepunch.com")
    count = driver.find_elements(By.CLASS_NAME, "streamer-name")
    streamers = []
    wait_timeh = []
    links = []

    for x in range(len(count)):
        streamer = driver.find_elements(By.CLASS_NAME, "streamer-name")[x].text
        if streamer not in streamers:
            read_time = driver.find_elements(By.XPATH, "//*[contains(text(), 'hours')]")[x].text
            streamers.append(streamer)
            wait_timeh.append(int(read_time[0]))
            link = "https://www.twitch.tv/" + streamer
            links.append(link)
    wait_time = [element * 3600 for element in wait_timeh]
    return wait_time, links


def login():
    driver.get("https://www.twitch.tv/drops/inventory")
    wait = WebDriverWait(driver, 600)
    wait.until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "p[data-test-selector='awarded-drop__drop-name']")))


wait_time, links = get_info()
login()

while all(i > 0 for i in wait_time):
    for x in range(len(links)):
        driver.get(links[x])
        time.sleep(10)
        try:
            while True:
                driver.find_element(By.CSS_SELECTOR, "a[status='live']")
                time.sleep(60)
                wait_time[x] -= 60
                print("I have to watch %s for %s minutes" % (links[x], wait_time[x]/60))
                if wait_time[x] < 0:
                    print("Done watching: ", links[x])
                    links.remove(links[x])
                    wait_time.remove(wait_time[x])
                    break
        except:
            print(links[x], "is not live.")
            if x == len(links):
                break
            else:
                continue
