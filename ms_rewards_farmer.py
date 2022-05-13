import time
import json
from datetime import date, timedelta, datetime
import requests
import random
import urllib.parse
import ipapi
import os

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, UnexpectedAlertPresentException, NoAlertPresentException

# Define user-agents
PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0. 3945.79 Mobile Safari/537.36'

POINTS_COUNTER = 0

BASE_URL = ""

# Define browser setup function
def browserSetup(headless_mode: bool = False, user_agent: str = PC_USER_AGENT) -> WebDriver:
    # Create Chrome browser
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("user-agent=" + user_agent)
    options.add_argument('lang=' + LANG.split("-")[0])
    if headless_mode :
        options.add_argument("--headless")
    options.add_argument('log-level=3')
    chrome_browser_obj = webdriver.Chrome(options=options)
    return chrome_browser_obj

# Define login function
def login(browser: WebDriver, email: str, pwd: str, isMobile: bool = False):
    # Access to bing.com
    browser.get('https://login.live.com/')
    # Wait complete loading
    waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    # Enter email
    print('[LOGIN]', 'Writing email...')
    browser.find_element(By.NAME, "loginfmt").send_keys(email)
    # Click next
    browser.find_element(By.ID, 'idSIButton9').click()
    # Wait 2 seconds
    time.sleep(2)
    # Wait complete loading
    waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    # Enter password
    #browser.find_element(By.ID, "i0118").send_keys(pwd)
    browser.execute_script("document.getElementById('i0118').value = '" + pwd + "';")
    print('[LOGIN]', 'Writing password...')
    # Click next
    browser.find_element(By.ID, 'idSIButton9').click()
    # Wait 5 seconds
    time.sleep(5)
    # Click Security Check
    print('[LOGIN]', 'Passing security checks...')
    try:
        browser.find_element(By.ID, 'iLandingViewAction').click()
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    try:
        browser.find_element(By.ID, 'iNext').click()
    except:
        pass
    # Wait complete loading
    try:
        waitUntilVisible(browser, By.ID, 'KmsiCheckboxField', 10)
    except (TimeoutException) as e:
        pass
    # Click next
    try:
        browser.find_element(By.ID, 'idSIButton9').click()
        # Wait 5 seconds
        time.sleep(5)
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    print('[LOGIN]', 'Logged-in !')
    # Check Login
    print('[LOGIN]', 'Ensuring login on Bing...')
    checkBingLogin(browser, isMobile)

def checkBingLogin(browser: WebDriver, isMobile: bool = False):
    global POINTS_COUNTER
    #Access Bing.com
    browser.get('https://bing.com/')
    # Wait 8 seconds
    time.sleep(8)
    #Accept Cookies
    try:
        browser.find_element(By.ID, 'bnp_btn_accept').click()
    except:
        pass
    if isMobile:
        try:
            time.sleep(1)
            browser.find_element(By.ID, 'mHamburger').click()
        except:
            try:
                browser.find_element(By.ID, 'bnp_btn_accept').click()
            except:
                pass
            try:
                browser.find_element(By.ID, 'bnp_ttc_close').click()
            except:
                pass
            time.sleep(1)
            try:
                browser.find_element(By.ID, 'mHamburger').click()
            except:
                pass
        try:
            time.sleep(1)
            browser.find_element(By.ID, 'HBSignIn').click()
        except:
            pass
        try:
            time.sleep(2)
            browser.find_element(By.ID, 'iShowSkip').click()
            time.sleep(3)
        except:
            if str(browser.current_url).split('?')[0] == "https://account.live.com/proofs/Add":
                input('[LOGIN] Please complete the Security Check on ' + browser.current_url)
                exit()
    #Wait 2 seconds
    time.sleep(2)
    # Refresh page
    browser.get('https://bing.com/')
    # Wait 5 seconds
    time.sleep(10)
    #Update Counter
    try:
        if not isMobile:
            POINTS_COUNTER = int(browser.find_element(By.ID, 'id_rc').get_attribute('innerHTML'))
        else:
            try:
                browser.find_element(By.ID, 'mHamburger').click()
            except:
                try:
                    browser.find_element(By.ID, 'bnp_btn_accept').click()
                except:
                    pass
                try:
                    browser.find_element(By.ID, 'bnp_ttc_close').click()
                except:
                    pass
                time.sleep(1)
                browser.find_element(By.ID, 'mHamburger').click()
            time.sleep(1)
            POINTS_COUNTER = int(browser.find_element(By.ID, 'fly_id_rc').get_attribute('innerHTML'))
    except:
        checkBingLogin(browser, isMobile)

def waitUntilVisible(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(ec.visibility_of_element_located((by_, selector)))

def waitUntilClickable(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(ec.element_to_be_clickable((by_, selector)))

def waitUntilQuestionRefresh(browser: WebDriver):
    tries = 0
    refreshCount = 0
    while True:
        try:
            browser.find_elements(By.CLASS_NAME, 'rqECredits')[0]
            return True
        except:
            if tries < 10:
                tries += 1
                time.sleep(0.5)
            else:
                if refreshCount < 5:
                    browser.refresh()
                    refreshCount += 1
                    tries = 0
                    time.sleep(5)
                else:
                    return False

def waitUntilQuizLoads(browser: WebDriver):
    tries = 0
    refreshCount = 0
    while True:
        try:
            browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]')
            return True
        except:
            if tries < 10:
                tries += 1
                time.sleep(0.5)
            else:
                if refreshCount < 5:
                    browser.refresh()
                    refreshCount += 1
                    tries = 0
                    time.sleep(5)
                else:
                    return False

def findBetween(s: str, first: str, last: str) -> str:
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def getCCodeLangAndOffset() -> tuple:
    try:
        nfo = ipapi.location()
        lang = nfo['languages'].split(',')[0]
        geo = nfo['country']
        tz = str(round(int(nfo['utc_offset']) / 100 * 60))
        return(lang, geo, tz)
    except:
        return('fr-FR', 'FR', '120')

def getGoogleTrends(numberOfwords: int) -> list:
    search_terms = []
    i = 0
    while len(search_terms) < numberOfwords :
        i += 1
        r = requests.get('https://trends.google.com/trends/api/dailytrends?hl=' + LANG + '&ed=' + str((date.today() - timedelta(days = i)).strftime('%Y%m%d')) + '&geo=' + GEO + '&ns=15')
        google_trends = json.loads(r.text[6:])
        for topic in google_trends['default']['trendingSearchesDays'][0]['trendingSearches']:
            search_terms.append(topic['title']['query'].lower())
            for related_topic in topic['relatedQueries']:
                search_terms.append(related_topic['query'].lower())
        search_terms = list(set(search_terms))
    del search_terms[numberOfwords:(len(search_terms)+1)]
    return search_terms

def getRelatedTerms(word: str) -> list:
    try:
        r = requests.get('https://api.bing.com/osjson.aspx?query=' + word, headers = {'User-agent': PC_USER_AGENT})
        return r.json()[1]
    except:
        return []

def resetTabs(browser: WebDriver):
    try:
        curr = browser.current_window_handle

        for handle in browser.window_handles:
            if handle != curr:
                browser.switch_to.window(handle)
                time.sleep(0.5)
                browser.close()
                time.sleep(0.5)

        browser.switch_to.window(curr)
        time.sleep(0.5)
        browser.get(BASE_URL)
    except:
        browser.get(BASE_URL)

def getAnswerCode(key: str, string: str) -> str:
	t = 0
	for i in range(len(string)):
		t += ord(string[i])
	t += int(key[-2:], 16)
	return str(t)

def bingSearches(browser: WebDriver, numberOfSearches: int, isMobile: bool = False):
    global POINTS_COUNTER
    i = 0
    search_terms = getGoogleTrends(numberOfSearches)
    for word in search_terms :
        i += 1
        print('[BING]', str(i) + "/" + str(numberOfSearches))
        points = bingSearch(browser, word, isMobile)
        if points <= POINTS_COUNTER :
            relatedTerms = getRelatedTerms(word)
            for term in relatedTerms :
                points = bingSearch(browser, term, isMobile)
                if not points <= POINTS_COUNTER :
                    break
        if points > 0:
            POINTS_COUNTER = points
        else:
            break

def bingSearch(browser: WebDriver, word: str, isMobile: bool):
    browser.get('https://bing.com')
    time.sleep(2)
    searchbar = browser.find_element(By.ID, 'sb_form_q')
    searchbar.send_keys(word)
    searchbar.submit()
    time.sleep(random.randint(10, 15))
    points = 0
    try:
        if not isMobile:
            points = int(browser.find_element(By.ID, 'id_rc').get_attribute('innerHTML'))
        else:
            try :
                browser.find_element(By.ID, 'mHamburger').click()
            except UnexpectedAlertPresentException:
                try :
                    browser.switch_to.alert.accept()
                    time.sleep(1)
                    browser.find_element(By.ID, 'mHamburger').click()
                except NoAlertPresentException :
                    pass
            time.sleep(1)
            points = int(browser.find_element(By.ID, 'fly_id_rc').get_attribute('innerHTML'))
    except:
        pass
    return points

def completePromotionalItems(browser: WebDriver):
    try:
        item = getDashboardData(browser)["promotionalItem"]
        if (item["pointProgressMax"] == 100 or item["pointProgressMax"] == 200) and item["complete"] == False and (item["destinationUrl"] == BASE_URL or item["destinationUrl"].startswith("https://www.bing.com/")):
            browser.find_element(By.XPATH, '//*[@id="promo-item"]/section/div/div/div/span').click()
            time.sleep(1)
            browser.switch_to.window(window_name = browser.window_handles[1])
            time.sleep(8)
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name = browser.window_handles[0])
            time.sleep(2)
    except:
        pass

def completeDailySetSearch(browser: WebDriver, cardNumber: int):
    time.sleep(5)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetSurvey(browser: WebDriver, cardNumber: int):
    time.sleep(5)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    browser.find_element(By.ID, "btoption" + str(random.randint(0, 1))).click()
    time.sleep(random.randint(10, 15))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetQuiz(browser: WebDriver, cardNumber: int):
    time.sleep(2)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    numberOfQuestions = browser.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
    numberOfOptions = browser.execute_script("return _w.rewardsQuizRenderInfo.numberOfOptions")
    for question in range(numberOfQuestions):
        if numberOfOptions == 8:
            answers = []
            for i in range(8):
                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("iscorrectoption").lower() == "true":
                    answers.append("rqAnswerOption" + str(i))
            for answer in answers:
                browser.find_element(By.ID, answer).click()
                time.sleep(5)
                if not waitUntilQuestionRefresh(browser):
                    return
            time.sleep(5)
        elif numberOfOptions == 4:
            correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
            for i in range(4):
                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                    browser.find_element(By.ID, "rqAnswerOption" + str(i)).click()
                    time.sleep(5)
                    if not waitUntilQuestionRefresh(browser):
                        return
                    break
            time.sleep(5)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetVariableActivity(browser: WebDriver, cardNumber: int):
    time.sleep(2)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    try :
        browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 3)
    except (NoSuchElementException, TimeoutException):
        try:
            counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
            numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
            for question in range(numberOfQuestions):
                browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                time.sleep(5)
                browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                time.sleep(3)
            time.sleep(5)
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name=browser.window_handles[0])
            time.sleep(2)
            return
        except NoSuchElementException:
            time.sleep(random.randint(5, 9))
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name = browser.window_handles[0])
            time.sleep(2)
            return
    time.sleep(3)
    correctAnswer = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
    if browser.find_element(By.ID, "rqAnswerOption0").get_attribute("data-option") == correctAnswer:
        browser.find_element(By.ID, "rqAnswerOption0").click()
    else :
        browser.find_element(By.ID, "rqAnswerOption1").click()
    time.sleep(10)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetThisOrThat(browser: WebDriver, cardNumber: int):
    time.sleep(2)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(10):
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element(By.ID, "rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = getAnswerCode(answerEncodeKey, answer1Title)

        answer2 = browser.find_element(By.ID, "rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = getAnswerCode(answerEncodeKey, answer2Title)

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

def getDashboardData(browser: WebDriver) -> dict:
    dashboard = findBetween(browser.find_element(By.XPATH, '/html/body').get_attribute('innerHTML'), "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
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
        try:
            if activity['complete'] == False:
                cardNumber = int(activity['offerId'][-1:])
                if activity['promotionType'] == "urlreward":
                    print('[DAILY SET]', 'Completing search of card ' + str(cardNumber))
                    completeDailySetSearch(browser, cardNumber)
                if activity['promotionType'] == "quiz":
                    if activity['pointProgressMax'] == 50 and activity['pointProgress'] == 0:
                        print('[DAILY SET]', 'Completing This or That of card ' + str(cardNumber))
                        completeDailySetThisOrThat(browser, cardNumber)
                    elif (activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30) and activity['pointProgress'] == 0:
                        print('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                        completeDailySetQuiz(browser, cardNumber)
                    elif activity['pointProgressMax'] == 10 and activity['pointProgress'] == 0:
                        searchUrl = urllib.parse.unquote(urllib.parse.parse_qs(urllib.parse.urlparse(activity['destinationUrl']).query)['ru'][0])
                        searchUrlQueries = urllib.parse.parse_qs(urllib.parse.urlparse(searchUrl).query)
                        filters = {}
                        for filter in searchUrlQueries['filters'][0].split(" "):
                            filter = filter.split(':', 1)
                            filters[filter[0]] = filter[1]
                        if "PollScenarioId" in filters:
                            print('[DAILY SET]', 'Completing poll of card ' + str(cardNumber))
                            completeDailySetSurvey(browser, cardNumber)
                        else:
                            print('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                            completeDailySetVariableActivity(browser, cardNumber)
        except:
            resetTabs(browser)

def getAccountPoints(browser: WebDriver) -> int:
    return getDashboardData(browser)['userStatus']['availablePoints']

def completePunchCard(browser: WebDriver, url: str, childPromotions: dict):
    browser.get(url)
    for child in childPromotions:
        if child['complete'] == False:
            if child['promotionType'] == "urlreward":
                browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                time.sleep(1)
                browser.switch_to.window(window_name = browser.window_handles[1])
                time.sleep(random.randint(13, 17))
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name = browser.window_handles[0])
                time.sleep(2)
            if child['promotionType'] == "quiz":
                browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                time.sleep(1)
                browser.switch_to.window(window_name = browser.window_handles[1])
                time.sleep(8)
                counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
                for question in range(numberOfQuestions):
                    browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                    time.sleep(5)
                    browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                    time.sleep(3)
                time.sleep(5)
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name = browser.window_handles[0])
                time.sleep(2)

def completePunchCards(browser: WebDriver):
    punchCards = getDashboardData(browser)['punchCards']
    for punchCard in punchCards:
        try:
            if punchCard['parentPromotion'] != None and punchCard['childPromotions'] != None and punchCard['parentPromotion']['complete'] == False and punchCard['parentPromotion']['pointProgressMax'] != 0:
                if BASE_URL == "https://rewards.microsoft.com":
                    completePunchCard(browser, punchCard['parentPromotion']['attributes']['destination'], punchCard['childPromotions'])
                else:
                    url = punchCard['parentPromotion']['attributes']['destination']
                    path = url.replace(
                        'https://account.microsoft.com/rewards/dashboard/', '')
                    userCode = path[:4]
                    dest = 'https://account.microsoft.com/rewards/dashboard/' + \
                        userCode + path.split(userCode)[1]
                    completePunchCard(browser, url, punchCard['childPromotions'])
        except:
            resetTabs(browser)
    time.sleep(2)
    browser.get(BASE_URL)
    time.sleep(2)

def completeMorePromotionSearch(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionQuiz(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    numberOfQuestions = browser.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
    numberOfOptions = browser.execute_script("return _w.rewardsQuizRenderInfo.numberOfOptions")
    for question in range(numberOfQuestions):
        if numberOfOptions == 8:
            answers = []
            for i in range(8):
                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("iscorrectoption").lower() == "true":
                    answers.append("rqAnswerOption" + str(i))
            for answer in answers:
                browser.find_element(By.ID, answer).click()
                time.sleep(5)
                if not waitUntilQuestionRefresh(browser):
                    return
            time.sleep(5)
        elif numberOfOptions == 4:
            correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
            for i in range(4):
                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                    browser.find_element(By.ID, "rqAnswerOption" + str(i)).click()
                    time.sleep(5)
                    if not waitUntilQuestionRefresh(browser):
                        return
                    break
            time.sleep(5)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionABC(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
    numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
    for question in range(numberOfQuestions):
        browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(5)
        browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
        time.sleep(3)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionThisOrThat(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(10):
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element(By.ID, "rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = getAnswerCode(answerEncodeKey, answer1Title)

        answer2 = browser.find_element(By.ID, "rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = getAnswerCode(answerEncodeKey, answer2Title)

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
        try:
            i += 1
            if promotion['complete'] == False and promotion['pointProgressMax'] != 0:
                if promotion['promotionType'] == "urlreward":
                    completeMorePromotionSearch(browser, i)
                elif promotion['promotionType'] == "quiz" and promotion['pointProgress'] == 0:
                    if promotion['pointProgressMax'] == 10:
                        completeMorePromotionABC(browser, i)
                    elif promotion['pointProgressMax'] == 30 or promotion['pointProgressMax'] == 40:
                        completeMorePromotionQuiz(browser, i)
                    elif promotion['pointProgressMax'] == 50:
                        completeMorePromotionThisOrThat(browser, i)
                else:
                    if promotion['pointProgressMax'] == 100 or promotion['pointProgressMax'] == 200:
                        completeMorePromotionSearch(browser, i)
        except:
            resetTabs(browser)

def getRemainingSearches(browser: WebDriver):
    dashboard = getDashboardData(browser)
    searchPoints = 1
    counters = dashboard['userStatus']['counters']
    if not 'pcSearch' in counters:
        return 0, 0
    progressDesktop = counters['pcSearch'][0]['pointProgress'] + counters['pcSearch'][1]['pointProgress']
    targetDesktop = counters['pcSearch'][0]['pointProgressMax'] + counters['pcSearch'][1]['pointProgressMax']
    if targetDesktop == 33 :
        #Level 1 EU
        searchPoints = 3
    elif targetDesktop == 55 :
        #Level 1 US
        searchPoints = 5
    elif targetDesktop == 102 :
        #Level 2 EU
        searchPoints = 3
    elif targetDesktop >= 170 :
        #Level 2 US
        searchPoints = 5
    remainingDesktop = int((targetDesktop - progressDesktop) / searchPoints)
    remainingMobile = 0
    if dashboard['userStatus']['levelInfo']['activeLevel'] != "Level1":
        progressMobile = counters['mobileSearch'][0]['pointProgress']
        targetMobile = counters['mobileSearch'][0]['pointProgressMax']
        remainingMobile = int((targetMobile - progressMobile) / searchPoints)
    return remainingDesktop, remainingMobile

def prRed(prt):
    print("\033[91m{}\033[00m".format(prt))
def prGreen(prt):
    print("\033[92m{}\033[00m".format(prt))
def prPurple(prt):
    print("\033[95m{}\033[00m".format(prt))
def prYellow(prt):
    print("\033[93m{}\033[00m".format(prt))

prRed("""
███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗ 
████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝""")
prPurple("        by Charles Bel (@charlesbel)               version 2.0\n")

LANG, GEO, TZ = getCCodeLangAndOffset()

try:
    account_path = os.path.dirname(os.path.abspath(__file__)) + '/accounts.json'
    ACCOUNTS = json.load(open(account_path, "r"))
except FileNotFoundError:
    with open(account_path, 'w') as f:
        f.write(json.dumps([{
            "username": "Your Email",
            "password": "Your Password"
        }], indent=4))
    prPurple("""
[ACCOUNT] Accounts credential file "accounts.json" created.
[ACCOUNT] Edit with your credentials and save, then press any key to continue...
    """)
    input()
    ACCOUNTS = json.load(open(account_path, "r"))

random.shuffle(ACCOUNTS)

for account in ACCOUNTS:

    prYellow('********************' + account['username'] + '********************')
    browser = browserSetup(True, PC_USER_AGENT)
    print('[LOGIN]', 'Logging-in...')
    login(browser, account['username'], account['password'])
    prGreen('[LOGIN] Logged-in successfully !')
    startingPoints = POINTS_COUNTER
    prGreen('[POINTS] You have ' + str(POINTS_COUNTER) + ' points on your account !')

    browser.get('https://account.microsoft.com/')
    waitUntilVisible(browser, By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a', 20)

    if browser.find_element(By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a').get_attribute('target') == '_blank':
        BASE_URL = 'https://rewards.microsoft.com'
        browser.find_element(By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a').click()
        time.sleep(1)
        browser.switch_to.window(window_name=browser.window_handles[0])
        browser.close()
        browser.switch_to.window(window_name=browser.window_handles[0])
        time.sleep(10)
    else:
        BASE_URL = 'https://account.microsoft.com/rewards'
        browser.get(BASE_URL)

    print('[DAILY SET]', 'Trying to complete the Daily Set...')
    completeDailySet(browser)
    prGreen('[DAILY SET] Completed the Daily Set successfully !')
    print('[PUNCH CARDS]', 'Trying to complete the Punch Cards...')
    completePunchCards(browser)
    prGreen('[PUNCH CARDS] Completed the Punch Cards successfully !')
    print('[MORE PROMO]', 'Trying to complete More Promotions...')
    completeMorePromotions(browser)
    prGreen('[MORE PROMO] Completed More Promotions successfully !')
    remainingSearches, remainingSearchesM = getRemainingSearches(browser)
    if remainingSearches != 0:
        print('[BING]', 'Starting Desktop and Edge Bing searches...')
        bingSearches(browser, remainingSearches)
        prGreen('[BING] Finished Desktop and Edge Bing searches !')
    browser.quit()

    if remainingSearchesM != 0:
        browser = browserSetup(True, MOBILE_USER_AGENT)
        print('[LOGIN]', 'Logging-in...')
        login(browser, account['username'], account['password'], True)
        print('[LOGIN]', 'Logged-in successfully !')
        print('[BING]', 'Starting Mobile Bing searches...')
        bingSearches(browser, remainingSearchesM, True)
        prGreen('[BING] Finished Mobile Bing searches !')
        browser.quit()

    prGreen('[POINTS] You have earned ' + str(POINTS_COUNTER - startingPoints) + ' points today !')
    prGreen('[POINTS] You are now at ' + str(POINTS_COUNTER) + ' points !\n')
