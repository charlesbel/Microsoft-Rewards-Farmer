import time
import json
from datetime import date, timedelta, datetime
import requests
import random
import urllib.parse
import ipapi

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, UnexpectedAlertPresentException, NoAlertPresentException

ACCOUNTS = [
    {
        "username": "Your Email",
        "password": "Your Password"
    }
]

# Define user-agents
PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0. 3945.79 Mobile Safari/537.36'

POINTS_COUNTER = 0

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
    print('[LOGIN]', 'Writing password...')
    # Click next
    browser.find_element_by_id('idSIButton9').click()
    # Wait 5 seconds
    time.sleep(5)
    # Click Security Check
    print('[LOGIN]', 'Passing security checks...')
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
            POINTS_COUNTER = int(browser.find_element_by_id('id_rc').get_attribute('innerHTML'))
        else:
            browser.find_element_by_id('mHamburger').click()
            time.sleep(1)
            POINTS_COUNTER = int(browser.find_element_by_id('fly_id_rc').get_attribute('innerHTML'))
    except (ValueError, NoSuchElementException) as e:
        checkBingLogin(browser, isMobile)

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

def getCCodeLangAndOffset():
    nfo = ipapi.location()
    lang = nfo['languages'].split(',')[0]
    geo = nfo['country']
    tz = str(round(int(nfo['utc_offset']) / 100 * 60))
    return(lang, geo, tz)

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

def getRelatedTerms(word: str) -> int:
    r = requests.get('https://api.bing.com/osjson.aspx?query=' + word, headers = {'User-agent': PC_USER_AGENT})
    return r.json()[1]

def bingSearches(browser: WebDriver, numberOfSearches: int, isMobile: bool = False):
    global POINTS_COUNTER
    i = 0
    search_terms = getGoogleTrends(numberOfSearches)
    for word in search_terms :
        i += 1
        print('[BING]', str(i) + "/" + str(numberOfSearches))
        browser.get('https://bing.com')
        time.sleep(2)
        searchbar = browser.find_element_by_id('sb_form_q')
        searchbar.send_keys(word)
        searchbar.submit()
        time.sleep(random.randint(10, 15))
        points = 0
        if not isMobile:
            points = int(browser.find_element_by_id('id_rc').get_attribute('innerHTML'))
        else :
            try :
                browser.find_element_by_id('mHamburger').click()
            except UnexpectedAlertPresentException:
                try :
                    browser.switch_to.alert.accept()
                    time.sleep(1)
                    browser.find_element_by_id('mHamburger').click()
                except NoAlertPresentException :
                    pass
            time.sleep(1)
            try :
                points = int(browser.find_element_by_id('fly_id_rc').get_attribute('innerHTML'))
            except NoSuchElementException:
                pass
        if points == POINTS_COUNTER :
            relatedTerms = getRelatedTerms(word)
            for term in relatedTerms :
                browser.get('https://bing.com')
                time.sleep(2)
                searchbar = browser.find_element_by_id('sb_form_q')
                searchbar.send_keys(random.choice(term))
                searchbar.submit()
                time.sleep(random.randint(10, 15))
                if not isMobile:
                    points = int(browser.find_element_by_id('id_rc').get_attribute('innerHTML'))
                else :
                    try:
                        browser.find_element_by_id('mHamburger').click()
                    except UnexpectedAlertPresentException:
                        try :
                            browser.switch_to.alert.accept()
                            time.sleep(1)
                            browser.find_element_by_id('mHamburger').click()
                        except NoAlertPresentException :
                            pass
                    time.sleep(1)
                    try :
                        points = int(browser.find_element_by_id('fly_id_rc').get_attribute('innerHTML'))
                    except NoSuchElementException:
                        pass
                if not points == POINTS_COUNTER :
                    break

        POINTS_COUNTER = points

def completeDailySetSearch(browser: WebDriver, cardNumber: int):
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

def completeDailySetVariableActivity(browser: WebDriver, cardNumber: int):
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    try :
        browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
    except NoSuchElementException:
        try:
            for question in range(3):
                browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                time.sleep(5)
                browser.find_element_by_xpath('//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                time.sleep(3)
            time.sleep(5)
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name=browser.window_handles[0])
            time.sleep(2)
        except NoSuchElementException:
            time.sleep(random.randint(5, 9))
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name = browser.window_handles[0])
            time.sleep(2)
            return
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

def completeDailySetThisOrThat(browser: WebDriver, cardNumber: int):
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/div[3]/a').click()
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

def getDashboardData(browser: WebDriver) -> dict:
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
                print('[DAILY SET]', 'Completing search of card ' + str(cardNumber))
                completeDailySetSearch(browser, cardNumber)
            if activity['promotionType'] == "quiz":
                if activity['pointProgressMax'] == 50:
                    print('[DAILY SET]', 'Completing This or That of card ' + str(cardNumber))
                    completeDailySetThisOrThat(browser, cardNumber)
                elif activity['pointProgressMax'] == 40:
                    print('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                    completeDailySetQuiz(browser, cardNumber, 4)
                elif activity['pointProgressMax'] == 30:
                    print('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                    completeDailySetQuiz(browser, cardNumber, 3)
                elif activity['pointProgressMax'] == 10:
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
                counter = str(browser.find_element_by_xpath('//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
                for question in range(numberOfQuestions):
                    browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                    time.sleep(5)
                    browser.find_element_by_xpath('//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                    time.sleep(3)
                time.sleep(5)
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name = browser.window_handles[0])
                time.sleep(2)

def completePunchCards(browser: WebDriver):
    punchCards = getDashboardData(browser)['punchCards']
    for punchCard in punchCards:
        if punchCard['parentPromotion'] != None and punchCard['childPromotions'] != None and punchCard['parentPromotion']['complete'] == False and punchCard['parentPromotion']['pointProgressMax'] != 0:
            url = punchCard['parentPromotion']['attributes']['destination']
            path = url.replace('https://account.microsoft.com/rewards/dashboard/','')
            userCode = path[:4]
            dest = 'https://account.microsoft.com/rewards/dashboard/' + userCode + path.split(userCode)[1]
            completePunchCard(browser, dest, punchCard['childPromotions'])
    time.sleep(2)
    browser.get('https://account.microsoft.com/rewards/')
    time.sleep(2)

def completeMorePromotionSearch(browser: WebDriver, cardNumber: int):
    browser.find_element_by_xpath('//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionQuiz(browser: WebDriver, cardNumber: int, numberOfQuestions: int):
    browser.find_element_by_xpath('//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    browser.find_element_by_xpath('//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(numberOfQuestions):
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

def completeMorePromotionABC(browser: WebDriver, cardNumber: int):
    browser.find_element_by_xpath('//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/div[3]/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    counter = str(browser.find_element_by_xpath('//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
    numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
    for question in range(numberOfQuestions):
        browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(5)
        browser.find_element_by_xpath('//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
        time.sleep(3)
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
                if promotion['pointProgressMax'] == 10:
                    completeMorePromotionABC(browser, i)
                elif promotion['pointProgressMax'] == 30:
                    completeMorePromotionQuiz(browser, i, 3)
                elif promotion['pointProgressMax'] == 40:
                    completeMorePromotionQuiz(browser, i, 4)
                elif promotion['pointProgressMax'] == 50:
                    completeMorePromotionThisOrThat(browser, i)
            else:
                if promotion['pointProgressMax'] == 100:
                    completeMorePromotionSearch(browser, i)

def getRemainingSearches(browser: WebDriver):
    dashboard = getDashboardData(browser)
    searchPoints = 1
    counters = dashboard['userStatus']['counters']
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
    elif targetDesktop == 170 :
        #Level 2 US
        searchPoints = 5
    remainingDesktop = int((targetDesktop - progressDesktop) / searchPoints)
    remainingMobile = 0
    if dashboard['userStatus']['levelInfo']['activeLevel'] != "Level1":
        progressMobile = counters['mobileSearch'][0]['pointProgress']
        targetMobile = counters['mobileSearch'][0]['pointProgressMax']
        remainingMobile = int((targetMobile - progressMobile) / searchPoints)
    return(remainingDesktop, remainingMobile)

LANG, GEO, TZ = getCCodeLangAndOffset()

for account in ACCOUNTS:

    print('********************' + account['username'] + '********************')
    browser = browserSetup(True, PC_USER_AGENT)
    print('[LOGIN]', 'Logging-in...')
    login(browser, account['username'], account['password'])
    print('[LOGIN]', 'Logged-in successfully !')
    startingPoints = POINTS_COUNTER
    print('[POINTS]', 'You have', POINTS_COUNTER, 'points on your account !')
    browser.get('https://account.microsoft.com/rewards/')
    print('[DAILY SET]', 'Trying to complete the Daily Set...')
    completeDailySet(browser)
    print('[DAILY SET]', 'Completed the Daily Set successfully !')
    print('[PUNCH CARDS]', 'Trying to complete the Punch Cards...')
    completePunchCards(browser)
    print('[PUNCH CARDS]', 'Completed the Punch Cards successfully !')
    print('[MORE PROMO]', 'Trying to complete More Promotions...')
    completeMorePromotions(browser)
    print('[MORE PROMO]', 'Completed More Promotions successfully !')
    print('[BING]', 'Starting Desktop and Edge Bing searches...')
    remainingSearches, remainingSearchesM = getRemainingSearches(browser)
    if remainingSearches != 0:
        bingSearches(browser, remainingSearches)
    print('[BING]', 'Finished Desktop and Edge Bing searches !')
    browser.quit()

    if remainingSearchesM != 0:
        browser = browserSetup(True, MOBILE_USER_AGENT)
        print('[LOGIN]', 'Logging-in...')
        login(browser, account['username'], account['password'], True)
        print('[LOGIN]', 'Logged-in successfully !')
        print('[BING]', 'Starting Mobile Bing searches...')
        bingSearches(browser, remainingSearchesM, True)
        print('[BING]', 'Finished Mobile Bing searches !')
        browser.quit()
    
    print('[POINTS]', 'You have earned', str(POINTS_COUNTER - startingPoints), 'points today !', '\n')
