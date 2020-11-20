import time
import json
from datetime import date, timedelta, datetime
import requests
import random
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

ACCOUNTS = [
    {
        "username": "Your Email",
        "password": "Your Password"
    }
]

# Define user-agents
PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:77.0) Gecko/77.0 Firefox/77.0'

# Define browser setup function
def browserSetup(headless_mode: bool = False, user_agent: str = PC_USER_AGENT) -> WebDriver:
    # Create Chrome browser
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("user-agent=" + user_agent)
    if headless_mode :
        options.headless = True
    chrome_browser_obj = webdriver.Chrome(options=options)
    return chrome_browser_obj

# Define login function
def login(browser: WebDriver, email: str, pwd: str, isMobile: bool = False):
    # Access to bing.com
    browser.get('https://login.live.com/')
    # Wait complete loading
    waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    # Enter email
    browser.find_element_by_name("loginfmt").send_keys(email)
    # Click next
    browser.find_element_by_id('idSIButton9').click()
    # Wait 2 seconds
    time.sleep(2)
    # Wait complete loading
    waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    # Enter password
    #browser.find_element_by_id("i0118").send_keys(pwd)
    browser.execute_script("document.getElementById('i0118').value = '" + pwd + "';")
    # Click next
    browser.find_element_by_id('idSIButton9').click()
    # Wait 5 seconds
    time.sleep(5)
    # Click Security Check
    try:
        browser.find_element_by_id('iLandingViewAction').click()
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    # Wait complete loading
    try:
        waitUntilVisible(browser, By.ID, 'KmsiCheckboxField', 10)
    except (TimeoutException) as e:
        pass
    # Click next
    try:
        browser.find_element_by_id('idSIButton9').click()
        # Wait 5 seconds
        time.sleep(5)
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    # Access bing.com
    browser.get('https://bing.com/')
    # Wait 8 seconds
    time.sleep(8)
    #Accept Cookies
    try:
        browser.find_element_by_id('bnp_btn_accept').click()
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    if isMobile:
        try:
            time.sleep(1)
            browser.find_element_by_id('mHamburger').click()
        except (NoSuchElementException, ElementNotInteractableException) as e:
            pass
        try:
            time.sleep(1)
            browser.find_element_by_id('HBSignIn').click()
        except (NoSuchElementException, ElementNotInteractableException) as e:
            pass
        try:
            time.sleep(2)
            browser.find_element_by_id('iShowSkip').click()
            time.sleep(3)
        except (NoSuchElementException, ElementNotInteractableException) as e:
            pass
    #Wait 2 seconds
    time.sleep(2)
    # Refresh page
    browser.refresh()
    # Wait 5 seconds
    time.sleep(5)

def waitUntilVisible(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(ec.visibility_of_element_located((by_, selector)))

def waitUntilClickable(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(ec.element_to_be_clickable((by_, selector)))

def findBetween(s: str, first: str, last: str) -> str:
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def getGoogleTrends(numberOfwords: int) -> list:
    search_terms = []
    i = 0
    while len(search_terms) < numberOfwords :
        i += 1
        r = requests.get('https://trends.google.com/trends/api/dailytrends?hl=fr-FR&ed=' + str((date.today() - timedelta(days = i)).strftime('%Y%m%d')) + '&geo=FR&ns=15')
        google_trends = json.loads(r.text[6:])
        for topic in google_trends['default']['trendingSearchesDays'][0]['trendingSearches']:
            search_terms.append(topic['title']['query'].lower())
            for related_topic in topic['relatedQueries']:
                search_terms.append(related_topic['query'].lower())
        search_terms = list(set(search_terms))
    del search_terms[numberOfwords:(len(search_terms)+1)]
    return search_terms

def bingSearches(browser: WebDriver, numberOfSearches: int):
    search_terms = getGoogleTrends(numberOfSearches)
    for word in search_terms :
        browser.get('https://bing.com')
        time.sleep(2)
        searchbar = browser.find_element_by_id('sb_form_q')
        searchbar.send_keys(word)
        searchbar.submit()
        time.sleep(random.randint(10, 15))
        report =  json.loads(findBetween(browser.find_element_by_xpath('/html/body').get_attribute('innerHTML'), "sj_evt && sj_evt.bind( \"onRALoad\", function() { var reportActivityModule = new ModernRewards.ReportActivity(", "); reportActivityModule.initialize(); }, 1 );;"))
        while report['RewardsSessionData']['PreviousBalance'] == report['RewardsSessionData']['Balance']:
            browser.get('https://bing.com')
            time.sleep(2)
            searchbar = browser.find_element_by_id('sb_form_q')
            searchbar.send_keys(word)
            searchbar.submit()
            time.sleep(random.randint(10, 15))
            report =  json.loads(findBetween(browser.find_element_by_xpath('/html/body').get_attribute('innerHTML'), "sj_evt && sj_evt.bind( \"onRALoad\", function() { var reportActivityModule = new ModernRewards.ReportActivity(", "); reportActivityModule.initialize(); }, 1 );;"))

def completeDailySetSearch(browser: WebDriver, cardNumber: int):
    browser.get('https://account.microsoft.com/rewards/')
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetSurvey(browser: WebDriver, cardNumber: int):
    browser.get('https://account.microsoft.com/rewards/')
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    browser.find_element_by_id("btoption" + str(random.randint(0, 1))).click()
    time.sleep(random.randint(10, 15))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetQuiz(browser: WebDriver, cardNumber: int, numberOfQuestions: int):
    browser.get('https://account.microsoft.com/rewards/')
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(numberOfQuestions):
        points = int((browser.find_elements_by_class_name('rqECredits')[0]).get_attribute("innerHTML"))
        answer = 0
        while (int((browser.find_elements_by_class_name('rqECredits')[0]).get_attribute("innerHTML")) == points) :
            browser.find_element_by_id("rqAnswerOption" + str(answer)).click()
            time.sleep(5)
            answer += 1
        time.sleep(5)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetTrueOrFalse(browser: WebDriver, cardNumber: int):
    browser.get('https://account.microsoft.com/rewards/')
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    correctAnswer = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
    if browser.find_element_by_id("rqAnswerOption0").get_attribute("data-option") == correctAnswer:
        browser.find_element_by_id("rqAnswerOption0").click()
    else :
        browser.find_element_by_id("rqAnswerOption1").click()
    time.sleep(10)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def getDashboardData(browser: WebDriver) -> dict:
    browser.get('https://account.microsoft.com/rewards/')
    dashboard = findBetween(browser.find_element_by_xpath('/html/body').get_attribute('innerHTML'), "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
    dashboard = json.loads(dashboard)
    return dashboard

def completeDailySet(browser: WebDriver):
    d = getDashboardData(browser)['dailySetPromotions']
    todayDate = datetime.today().strftime('%m/%d/%Y')
    todayPack = []
    for date, data in d.items():
        if date == todayDate:
            todayPack = data
    for activity in todayPack:
        if activity['complete'] == False:
            cardNumber = int(activity['offerId'][-1:])
            if activity['promotionType'] == "urlreward":
                completeDailySetSearch(browser, cardNumber)
            if activity['promotionType'] == "quiz":
                if activity['pointProgressMax'] == 40:
                    completeDailySetQuiz(browser, cardNumber, 4)
                elif activity['pointProgressMax'] == 30:
                    completeDailySetQuiz(browser, cardNumber, 3)
                elif activity['pointProgressMax'] == 10:
                    searchUrl = urllib.parse.unquote(urllib.parse.parse_qs(urllib.parse.urlparse(activity['destinationUrl']).query)['ru'][0])
                    searchUrlQueries = urllib.parse.parse_qs(urllib.parse.urlparse(searchUrl).query)
                    filters = {}
                    for filter in searchUrlQueries['filters'][0].split(" "):
                        filter = filter.split(':', 1)
                        filters[filter[0]] = filter[1]
                    if "PollScenarioId" in filters:
                        completeDailySetSurvey(browser, cardNumber)
                    else:
                        completeDailySetTrueOrFalse(browser, cardNumber)

def getAccountPoints(browser: WebDriver) -> int:
    return getDashboardData(browser)['userStatus']['availablePoints']

def completePunchCard(browser: WebDriver, url: str, childPromotions: dict):
    browser.get(url)
    for child in childPromotions:
        if child['complete'] == False and child['promotionType'] == "urlreward":
            browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
            time.sleep(1)
            browser.switch_to.window(window_name = browser.window_handles[1])
            time.sleep(random.randint(13, 17))
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name = browser.window_handles[0])
            time.sleep(2)

def completePunchCards(browser: WebDriver):
    punchCards = getDashboardData(browser)['punchCards']
    for punchCard in punchCards:
        if punchCard['parentPromotion'] != None and punchCard['childPromotions'] != None and punchCard['parentPromotion']['complete'] == False and punchCard['parentPromotion']['promotionType'].split(',')[0] == "urlreward" and punchCard['parentPromotion']['pointProgressMax'] != 0:
            url = punchCard['parentPromotion']['attributes']['destination']
            completePunchCard(browser, url, punchCard['childPromotions'])

def completeMorePromotionSearch(browser: WebDriver, cardNumber: int):
    browser.find_element_by_xpath('//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionQuiz(browser: WebDriver, cardNumber: int):
    browser.find_element_by_xpath('//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(3):
        points = int((browser.find_elements_by_class_name('rqECredits')[0]).get_attribute("innerHTML"))
        answer = 0
        while (int((browser.find_elements_by_class_name('rqECredits')[0]).get_attribute("innerHTML")) == points):
            browser.find_element_by_id("rqAnswerOption" + str(answer)).click()
            time.sleep(5)
            answer += 1
        time.sleep(5)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionThisOrThat(browser: WebDriver, cardNumber: int):
    browser.find_element_by_xpath('//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(10):
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element_by_id("rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = browser.execute_script("var IG = \"" + answerEncodeKey + "\"; function getAnswerCode(n){for (var r, t = 0, i = 0; i < n.length; i++) t += n.charCodeAt(i); return r = parseInt(IG.substr(IG.length - 2), 16), t += r, t.toString();} return getAnswerCode(\"" + answer1Title + "\");")

        answer2 = browser.find_element_by_id("rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = browser.execute_script("var IG = \"" + answerEncodeKey + "\"; function getAnswerCode(n){for (var r, t = 0, i = 0; i < n.length; i++) t += n.charCodeAt(i); return r = parseInt(IG.substr(IG.length - 2), 16), t += r, t.toString();} return getAnswerCode(\"" + answer2Title + "\");")

        correctAnswerCode = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")

        if (answer1Code == correctAnswerCode):
            answer1.click()
            time.sleep(8)
        elif (answer2Code == correctAnswerCode):
            answer2.click()
            time.sleep(8)

    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def completeMorePromotions(browser: WebDriver):
    morePromotions = getDashboardData(browser)['morePromotions']
    i = 0
    for promotion in morePromotions:
        i += 1
        if promotion['complete'] == False and promotion['pointProgressMax'] != 0:
            if promotion['promotionType'] == "urlreward":
                completeMorePromotionSearch(browser, i)
            elif promotion['promotionType'] == "quiz":
                if promotion['pointProgressMax'] == 30:
                    completeMorePromotionQuiz(browser, i)
                elif promotion['pointProgressMax'] == 50:
                    completeMorePromotionThisOrThat(browser, i)

for account in ACCOUNTS:

    browser = browserSetup(False, PC_USER_AGENT)
    login(browser, account['username'], account['password'])

    completeDailySet(browser)

    completePunchCards(browser)

    completeMorePromotions(browser)

    bingSearches(browser, 34)

    browser.quit()


    browser = browserSetup(False, MOBILE_USER_AGENT)
    login(browser, account['username'], account['password'], True)

    bingSearches(browser, 20)

    browser.quit()
