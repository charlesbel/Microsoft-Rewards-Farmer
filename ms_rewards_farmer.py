import time
import json
from datetime import datetime
import requests
import random

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

USERNAME = "Your microsoft email"
PASSWORD = "Your Microsoft password"

PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43'

MOBILE_USER_AGENT = 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:77.0) Gecko/77.0 Firefox/77.0'

def browser_setup(headless_mode, user_agent):
    if headless_mode :
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.headless = headless_mode
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', user_agent)
        profile.set_preference('dom.webnotifications.serviceworker.enabled', False)
        profile.set_preference('dom.webnotifications.enabled', False)
        profile.set_preference('geo.enabled', False)
        firefox_browser_obj = webdriver.Firefox(options=options, firefox_profile=profile)
        return firefox_browser_obj
    else :
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("user-agent=" + user_agent)
        chrome_browser_obj = webdriver.Chrome(options=options)
        return chrome_browser_obj

def login(email, pwd):
    browser.get('https://login.live.com/')
    browser.find_element_by_name("loginfmt").send_keys(email)
    browser.find_element_by_id('idSIButton9').click()
    time.sleep(2)
    wait_until_visible(By.ID, 'loginHeader', 10)
    browser.find_element_by_id("i0118").send_keys(pwd)
    browser.find_element_by_id('idSIButton9').click()
    browser.execute_script("window.open('https://bing.com');")
    time.sleep(2)
    browser.switch_to_window(browser.window_handles[1])
    time.sleep(8)
    browser.refresh()
    time.sleep(8)
    browser.close()
    time.sleep(2)
    browser.switch_to_window(browser.window_handles[0])

def wait_until_visible(by_, selector, time_to_wait=10):
    WebDriverWait(browser, time_to_wait).until(ec.visibility_of_element_located((by_, selector)))

def wait_until_clickable(by_, selector, time_to_wait=10):
    WebDriverWait(browser, time_to_wait).until(ec.element_to_be_clickable((by_, selector)))

def find_between(s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def get_google_trends(numberOfwords):
    search_terms = []
    i = 0
    while len(search_terms) < numberOfwords :
        i += 1
        r = requests.get('https://trends.google.com/trends/api/dailytrends?hl=fr-FR&ed=' + str(datetime.today().strftime('%Y%m')) + str(int(datetime.today().strftime('%d')) - i).zfill(2) + '&geo=FR&ns=15')
        google_trends = json.loads(r.text[6:])
        for topic in google_trends['default']['trendingSearchesDays'][0]['trendingSearches']:
            if len(search_terms) < numberOfwords:
                search_terms.append(topic['title']['query'].lower())
                for related_topic in topic['relatedQueries']:
                    if len(search_terms) < numberOfwords:
                        search_terms.append(related_topic['query'].lower())
    search_terms = set(search_terms)
    return search_terms

def bing_search(numberOfSearches):
    search_terms = get_google_trends(numberOfSearches)
    for word in search_terms :
        browser.get('https://bing.com')
        time.sleep(2)
        browser.find_element_by_id('sb_form_q').send_keys(word)
        browser.find_element_by_class_name('search').click()
        time.sleep(random.randint(10, 15))

def visit_bing_url(url):
    browser.execute_script("window.open('{}');".format(url))
    time.sleep(2)
    browser.switch_to_window(browser.window_handles[1])
    time.sleep(10)
    browser.close()
    browser.switch_to_window(browser.window_handles[0])
    time.sleep(2)

browser = browser_setup(True, PC_USER_AGENT)

login(USERNAME, PASSWORD)

#bing_search(10)