import time
import json
from datetime import date, timedelta, datetime
import requests
import random
import urllib.parse
import ipapi
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, UnexpectedAlertPresentException, NoAlertPresentException


PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.86'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.196 Mobile Safari/537.36'

POINTS_COUNTER = 0

BASE_URL = 'https://rewards.bing.com'


def browserSetup(headlessMode: bool = False, userAgent: str = PC_USER_AGENT) -> WebDriver:
    options = Options()
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument(f'lang={LANG.split("-")[0]}')
    if headlessMode:
        options.add_argument('--headless')
    options.add_argument('log-level=3')
    chrome_browser_obj = webdriver.Chrome(options=options)
    return chrome_browser_obj


def goHome(browser: WebDriver):
    browser.get(BASE_URL)
    waitUntilVisible(browser, By.ID, 'daily-sets', 10)
    tryDismissCookieBanner(browser)


def tryDismissAllMessages(browser: WebDriver):
    buttons = [(By.ID, 'iLandingViewAction'), (By.ID, 'iShowSkip'), (By.ID, 'iNext'), (By.ID,
                                                                                       'iLooksGood'), (By.ID, 'idSIButton9'), (By.CSS_SELECTOR, '.ms-Button.ms-Button--primary')]
    result = False
    for button in buttons:
        try:
            browser.find_element(button[0], button[1]).click()
            result = True
        except:
            continue
    return result


def tryDismissCookieBanner(browser: WebDriver):
    try:
        browser.find_element(
            By.ID, 'cookie-banner').find_element(By.TAG_NAME, 'button').click()
        time.sleep(2)
    except:
        pass


def login(browser: WebDriver, email: str, password: str, isMobile: bool = False):
    global POINTS_COUNTER
    browser.get('https://login.live.com/')

    waitUntilVisible(browser, By.ID, 'loginHeader', 10)
    print('[LOGIN]', 'Writing email...')
    browser.find_element(By.NAME, "loginfmt").send_keys(email)
    browser.find_element(By.ID, 'idSIButton9').click()

    waitUntilClickable(browser, By.ID, 'idSIButton9', 10)
    # browser.find_element(By.NAME, "passwd").send_keys(password)
    # If password contains special characters like " ' or \, send_keys() will not work
    password = password.replace('\\', '\\\\').replace('"', '\\"')
    browser.execute_script(
        f'document.getElementsByName("passwd")[0].value = "{password}";')
    print('[LOGIN]', 'Writing password...')
    browser.find_element(By.ID, 'idSIButton9').click()

    while not (urllib.parse.urlparse(browser.current_url).path == "/" and urllib.parse.urlparse(browser.current_url).hostname == "account.microsoft.com"):
        tryDismissAllMessages(browser)
        time.sleep(1)

    waitUntilVisible(browser, By.CSS_SELECTOR,
                     'html[data-role-name="MeePortal"]', 10)
    tryDismissCookieBanner(browser)

    print('[LOGIN]', 'Logged-in !')

    browser.get(BASE_URL)
    while True:
        tryDismissCookieBanner(browser)
        try:
            browser.find_element(By.ID, 'daily-sets')
            break
        except:
            pass
        if urllib.parse.urlparse(browser.current_url).hostname != urllib.parse.urlparse(BASE_URL).hostname:
            if tryDismissAllMessages(browser):
                time.sleep(1)
                browser.get(BASE_URL)
        time.sleep(1)
    POINTS_COUNTER = getAccountPoints(browser)

    print('[LOGIN]', 'Ensuring login on Bing...')
    checkBingLogin(browser, isMobile)


def checkBingLogin(browser: WebDriver, isMobile: bool = False):
    browser.get('https://www.bing.com/fd/auth/signin?action=interactive&provider=windows_live_id&return_url=https%3A%2F%2Fwww.bing.com%2F')
    isHamburgerOpened = False
    while True:
        currentUrl = urllib.parse.urlparse(browser.current_url)
        if currentUrl.hostname == 'www.bing.com' and currentUrl.path == '/':
            try:
                browser.find_element(By.ID, 'bnp_btn_accept').click()
            except:
                pass
            try:
                if isMobile:
                    if not isHamburgerOpened:
                        browser.find_element(By.ID, 'mHamburger').click()
                        isHamburgerOpened = True
                    int(browser.find_element(
                        By.ID, 'fly_id_rc').get_attribute('innerHTML'))
                else:
                    int(browser.find_element(
                        By.ID, 'id_rc').get_attribute('innerHTML'))
                break
            except:
                pass
        time.sleep(1)


def waitUntilVisible(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(
        ec.visibility_of_element_located((by_, selector)))


def waitUntilClickable(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(
        ec.element_to_be_clickable((by_, selector)))


def waitForMSRewardElement(browser: WebDriver, by_: By, selector: str):
    loadingTimeAllowed = 5
    refreshsAllowed = 5

    checkingInterval = 0.5
    checks = loadingTimeAllowed / checkingInterval

    tries = 0
    refreshCount = 0
    while True:
        try:
            browser.find_element(by_, selector)
            return True
        except:
            if tries < checks:
                tries += 1
                time.sleep(checkingInterval)
            else:
                if refreshCount < refreshsAllowed:
                    browser.refresh()
                    refreshCount += 1
                    tries = 0
                    time.sleep(5)
                else:
                    return False


def waitUntilQuestionRefresh(browser: WebDriver):
    return waitForMSRewardElement(browser, By.CLASS_NAME, 'rqECredits')


def waitUntilQuizLoads(browser: WebDriver):
    return waitForMSRewardElement(browser, By.XPATH, '//*[@id="rqStartQuiz"]')


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
        return (lang, geo)
    except:
        return ('fr-FR', 'FR')


def getGoogleTrends(wordsCount: int) -> list:
    searchTerms = []
    i = 0
    while len(searchTerms) < wordsCount:
        i += 1
        r = requests.get('https://trends.google.com/trends/api/dailytrends?hl=' + LANG + '&ed=' +
                         str((date.today() - timedelta(days=i)).strftime('%Y%m%d')) + '&geo=' + GEO + '&ns=15')
        trends = json.loads(r.text[6:])
        for topic in trends['default']['trendingSearchesDays'][0]['trendingSearches']:
            searchTerms.append(topic['title']['query'].lower())
            for relatedTopic in topic['relatedQueries']:
                searchTerms.append(relatedTopic['query'].lower())
        searchTerms = list(set(searchTerms))
    del searchTerms[wordsCount:(len(searchTerms)+1)]
    return searchTerms


def getRelatedTerms(word: str) -> list:
    try:
        r = requests.get('https://api.bing.com/osjson.aspx?query=' +
                         word, headers={'User-agent': PC_USER_AGENT})
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
        goHome(browser)
    except:
        goHome(browser)


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
    for word in search_terms:
        i += 1
        print('[BING]', str(i) + "/" + str(numberOfSearches))
        points = bingSearch(browser, word, isMobile)
        if points <= POINTS_COUNTER:
            relatedTerms = getRelatedTerms(word)
            for term in relatedTerms:
                points = bingSearch(browser, term, isMobile)
                if not points <= POINTS_COUNTER:
                    break
        if points > 0:
            POINTS_COUNTER = points
        else:
            break


def bingSearch(browser: WebDriver, word: str, isMobile: bool):
    browser.get('https://bing.com')
    waitUntilClickable(browser, By.ID, 'sb_form_q')
    searchbar = browser.find_element(By.ID, 'sb_form_q')
    searchbar.send_keys(word)
    searchbar.submit()
    time.sleep(random.randint(10, 15))
    points = 0
    try:
        if not isMobile:
            points = int(browser.find_element(
                By.ID, 'id_rc').get_attribute('innerHTML'))
        else:
            try:
                browser.find_element(By.ID, 'mHamburger').click()
                time.sleep(1)
            except UnexpectedAlertPresentException:
                try:
                    browser.switch_to.alert.accept()
                    browser.find_element(By.ID, 'mHamburger').click()
                except NoAlertPresentException:
                    pass
            points = int(browser.find_element(
                By.ID, 'fly_id_rc').get_attribute('innerHTML'))
    except:
        pass
    return points


def switchToNewTab(browser: WebDriver):
    time.sleep(0.5)
    browser.switch_to.window(window_name=browser.window_handles[1])


def closeCurrentTab(browser: WebDriver):
    browser.close()
    time.sleep(0.5)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(0.5)


def visitNewTab(browser: WebDriver, timeToWait: int = 0):
    switchToNewTab(browser)
    time.sleep(timeToWait)
    closeCurrentTab(browser)


def completePromotionalItems(browser: WebDriver):
    try:
        item = getDashboardData(browser)["promotionalItem"]
        if (item["pointProgressMax"] == 100 or item["pointProgressMax"] == 200) and item["complete"] == False and (item["destinationUrl"] == BASE_URL or item["destinationUrl"].startswith("https://www.bing.com/")):
            browser.find_element(
                By.XPATH, '//*[@id="promo-item"]/section/div/div/div/span').click()
            visitNewTab(browser, 8)
    except:
        pass


def completeDailySetSearch(browser: WebDriver, cardNumber: int):
    browser.find_element(
        By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    visitNewTab(browser, random.randint(13, 17))


def completeDailySetSurvey(browser: WebDriver, cardNumber: int):
    browser.find_element(
        By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    switchToNewTab(browser)
    time.sleep(8)
    browser.find_element(By.ID, f'btoption{random.randint(0, 1)}').click()
    time.sleep(random.randint(10, 15))
    closeCurrentTab(browser)


def completeDailySetQuiz(browser: WebDriver, cardNumber: int):
    browser.find_element(
        By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    switchToNewTab(browser)
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH,
                     '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    numberOfQuestions = browser.execute_script(
        "return _w.rewardsQuizRenderInfo.maxQuestions")
    numberOfOptions = browser.execute_script(
        "return _w.rewardsQuizRenderInfo.numberOfOptions")
    for _ in range(numberOfQuestions):
        if numberOfOptions == 8:
            answers = []
            for i in range(8):
                if browser.find_element(By.ID, f'rqAnswerOption{i}').get_attribute("iscorrectoption").lower() == "true":
                    answers.append(f'rqAnswerOption{i}')
            for answer in answers:
                browser.find_element(By.ID, answer).click()
                time.sleep(5)
                if not waitUntilQuestionRefresh(browser):
                    return
            time.sleep(5)
        elif numberOfOptions == 4:
            correctOption = browser.execute_script(
                "return _w.rewardsQuizRenderInfo.correctAnswer")
            for i in range(4):
                if browser.find_element(By.ID, f'rqAnswerOption{i}').get_attribute("data-option") == correctOption:
                    browser.find_element(
                        By.ID, f'rqAnswerOption{i}').click()
                    time.sleep(5)
                    if not waitUntilQuestionRefresh(browser):
                        return
                    break
            time.sleep(5)
    time.sleep(5)
    closeCurrentTab(browser)


def completeDailySetVariableActivity(browser: WebDriver, cardNumber: int):
    browser.find_element(
        By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    switchToNewTab(browser)
    time.sleep(8)
    try:
        browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        waitUntilVisible(browser, By.XPATH,
                         '//*[@id="currentQuestionContainer"]/div/div[1]', 3)
    except (NoSuchElementException, TimeoutException):
        try:
            counter = str(browser.find_element(
                By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
            numberOfQuestions = max([int(s)
                                    for s in counter.split() if s.isdigit()])
            for question in range(numberOfQuestions):
                browser.execute_script(
                    f'document.evaluate("//*[@id=\'QuestionPane{question}\']/div[1]/div[2]/a[{random.randint(1, 3)}]/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                time.sleep(5)
                browser.find_element(
                    By.XPATH, f'//*[@id="AnswerPane{question}]/div[1]/div[2]/div[4]/a/div/span/input').click()
                time.sleep(3)
            time.sleep(5)
            closeCurrentTab(browser)
            return
        except NoSuchElementException:
            time.sleep(random.randint(5, 9))
            closeCurrentTab(browser)
            return
    time.sleep(3)
    correctAnswer = browser.execute_script(
        "return _w.rewardsQuizRenderInfo.correctAnswer")
    if browser.find_element(By.ID, "rqAnswerOption0").get_attribute("data-option") == correctAnswer:
        browser.find_element(By.ID, "rqAnswerOption0").click()
    else:
        browser.find_element(By.ID, "rqAnswerOption1").click()
    time.sleep(10)
    closeCurrentTab(browser)


def completeDailySetThisOrThat(browser: WebDriver, cardNumber: int):
    browser.find_element(
        By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    switchToNewTab(browser)
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH,
                     '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for _ in range(10):
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element(By.ID, "rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = getAnswerCode(answerEncodeKey, answer1Title)

        answer2 = browser.find_element(By.ID, "rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = getAnswerCode(answerEncodeKey, answer2Title)

        correctAnswerCode = browser.execute_script(
            "return _w.rewardsQuizRenderInfo.correctAnswer")

        if (answer1Code == correctAnswerCode):
            answer1.click()
            time.sleep(8)
        elif (answer2Code == correctAnswerCode):
            answer2.click()
            time.sleep(8)

    time.sleep(5)
    closeCurrentTab(browser)


def getDashboardData(browser: WebDriver) -> dict:
    return browser.execute_script("return dashboard")


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
                    print('[DAILY SET]',
                          'Completing search of card ' + str(cardNumber))
                    completeDailySetSearch(browser, cardNumber)
                if activity['promotionType'] == "quiz":
                    if activity['pointProgressMax'] == 50 and activity['pointProgress'] == 0:
                        print(
                            '[DAILY SET]', 'Completing This or That of card ' + str(cardNumber))
                        completeDailySetThisOrThat(browser, cardNumber)
                    elif (activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30) and activity['pointProgress'] == 0:
                        print('[DAILY SET]',
                              'Completing quiz of card ' + str(cardNumber))
                        completeDailySetQuiz(browser, cardNumber)
                    elif activity['pointProgressMax'] == 10 and activity['pointProgress'] == 0:
                        searchUrl = urllib.parse.unquote(urllib.parse.parse_qs(
                            urllib.parse.urlparse(activity['destinationUrl']).query)['ru'][0])
                        searchUrlQueries = urllib.parse.parse_qs(
                            urllib.parse.urlparse(searchUrl).query)
                        filters = {}
                        for filter in searchUrlQueries['filters'][0].split(" "):
                            filter = filter.split(':', 1)
                            filters[filter[0]] = filter[1]
                        if "PollScenarioId" in filters:
                            print(
                                '[DAILY SET]', 'Completing poll of card ' + str(cardNumber))
                            completeDailySetSurvey(browser, cardNumber)
                        else:
                            print(
                                '[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                            completeDailySetVariableActivity(
                                browser, cardNumber)
        except:
            resetTabs(browser)


def getAccountPoints(browser: WebDriver) -> int:
    return getDashboardData(browser)['userStatus']['availablePoints']


def completePunchCard(browser: WebDriver, url: str, childPromotions: dict):
    browser.get(url)
    for child in childPromotions:
        if child['complete'] == False:
            if child['promotionType'] == "urlreward":
                browser.execute_script(
                    "document.getElementsByClassName('offer-cta')[0].click()")
                visitNewTab(browser, random.randint(13, 17))
            if child['promotionType'] == "quiz":
                browser.execute_script(
                    "document.getElementsByClassName('offer-cta')[0].click()")
                switchToNewTab(browser)
                time.sleep(8)
                counter = str(browser.find_element(
                    By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                numberOfQuestions = max(
                    [int(s) for s in counter.split() if s.isdigit()])
                for question in range(numberOfQuestions):
                    browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(
                        random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                    time.sleep(5)
                    browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(
                        question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                    time.sleep(3)
                time.sleep(5)
                closeCurrentTab(browser)


def completePunchCards(browser: WebDriver):
    punchCards = getDashboardData(browser)['punchCards']
    for punchCard in punchCards:
        try:
            if punchCard['parentPromotion'] != None and punchCard['childPromotions'] != None and punchCard['parentPromotion']['complete'] == False and punchCard['parentPromotion']['pointProgressMax'] != 0:
                if BASE_URL == "https://rewards.microsoft.com":
                    completePunchCard(
                        browser, punchCard['parentPromotion']['attributes']['destination'], punchCard['childPromotions'])
                else:
                    url = punchCard['parentPromotion']['attributes']['destination']
                    path = url.replace(
                        'https://account.microsoft.com/rewards/dashboard/', '')
                    userCode = path[:4]
                    dest = 'https://account.microsoft.com/rewards/dashboard/' + \
                        userCode + path.split(userCode)[1]
                    completePunchCard(
                        browser, url, punchCard['childPromotions'])
        except:
            resetTabs(browser)
    time.sleep(2)
    browser.get(BASE_URL)
    time.sleep(2)


def completeMorePromotionSearch(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(
        cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)


def completeMorePromotionQuiz(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(
        cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH,
                     '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    numberOfQuestions = browser.execute_script(
        "return _w.rewardsQuizRenderInfo.maxQuestions")
    numberOfOptions = browser.execute_script(
        "return _w.rewardsQuizRenderInfo.numberOfOptions")
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
            correctOption = browser.execute_script(
                "return _w.rewardsQuizRenderInfo.correctAnswer")
            for i in range(4):
                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                    browser.find_element(
                        By.ID, "rqAnswerOption" + str(i)).click()
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
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(
        cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    counter = str(browser.find_element(
        By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
    numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
    for question in range(numberOfQuestions):
        browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(
            random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(5)
        browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(
            question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
        time.sleep(3)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)


def completeMorePromotionThisOrThat(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(
        cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH,
                     '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(10):
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element(By.ID, "rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = getAnswerCode(answerEncodeKey, answer1Title)

        answer2 = browser.find_element(By.ID, "rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = getAnswerCode(answerEncodeKey, answer2Title)

        correctAnswerCode = browser.execute_script(
            "return _w.rewardsQuizRenderInfo.correctAnswer")

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
    progressDesktop = counters['pcSearch'][0]['pointProgress'] + \
        counters['pcSearch'][1]['pointProgress']
    targetDesktop = counters['pcSearch'][0]['pointProgressMax'] + \
        counters['pcSearch'][1]['pointProgressMax']
    if targetDesktop == 33:
        # Level 1 EU
        searchPoints = 3
    elif targetDesktop == 55:
        # Level 1 US
        searchPoints = 5
    elif targetDesktop == 102:
        # Level 2 EU
        searchPoints = 3
    elif targetDesktop >= 170:
        # Level 2 US
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

LANG, GEO = getCCodeLangAndOffset()

try:
    account_path = os.path.dirname(
        os.path.abspath(__file__)) + '/accounts.json'
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

# random.shuffle(ACCOUNTS)

for account in ACCOUNTS:

    prYellow('********************' +
             account['username'] + '********************')
    browser = browserSetup(False, PC_USER_AGENT)
    print('[LOGIN]', 'Logging-in...')
    login(browser, account['username'], account['password'])
    prGreen('[LOGIN] Logged-in successfully !')
    startingPoints = POINTS_COUNTER
    prGreen('[POINTS] You have ' + str(POINTS_COUNTER) +
            ' points on your account !')

    goHome(browser)

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
        browser = browserSetup(False, MOBILE_USER_AGENT)
        print('[LOGIN]', 'Logging-in...')
        login(browser, account['username'], account['password'], True)
        print('[LOGIN]', 'Logged-in successfully !')
        print('[BING]', 'Starting Mobile Bing searches...')
        bingSearches(browser, remainingSearchesM, True)
        prGreen('[BING] Finished Mobile Bing searches !')
        browser.quit()

    prGreen('[POINTS] You have earned ' +
            str(POINTS_COUNTER - startingPoints) + ' points today !')
    prGreen('[POINTS] You are now at ' + str(POINTS_COUNTER) + ' points !\n')
