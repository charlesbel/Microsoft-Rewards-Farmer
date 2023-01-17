import time
import json
from datetime import date, timedelta, datetime
import requests
import random
import urllib.parse
import ipapi
import os
import os.path
from os import path
import sys

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, UnexpectedAlertPresentException, NoAlertPresentException

# Define user-agents
PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; Pixel 3) zAppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0. 3945.79 Mobile Safari/537.36'
BASE_URL = ""
POINTS_COUNTER = 0
ACCOUNT_COUNTER = 0
REWARDS = 0
FIRST_RUN = True
FIRST_RUN_M = True

#rewardsFile = 'C://Users//YourNameHere//Desktop//Microsoft.Rewards.Gift.Card.Info.txt' #change YourNameHere to your pc's Username and delete the # infront of rewardsFile 
tempSleepTimer = random.randint(200, 300)

# Define browser setup function
def browserSetup(headless_mode: bool = False, user_agent: str = PC_USER_AGENT) -> WebDriver:
    try :
        # Create Chrome browser
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("user-agent=" + user_agent)
        options.add_argument('lang=' + LANG.split("-")[0])
        if headless_mode : #comment out to disable headless mode (makes window visable) 
            options.add_argument("--headless") #comment out to disable headless mode (makes window visable) 
        options.add_argument('log-level=3')
        chrome_browser_obj = webdriver.Chrome(options=options)
        return chrome_browser_obj
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Browser Setup.\n')

# Define login function
def login(browser: WebDriver, email: str, pwd: str, isMobile: bool = False):
    try :
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
        time.sleep(2)
        if not isMobile:
            checkBingLogin(browser, isMobile) #commented out this line to make mobileSearch work
    except :
        prRed('\n[ERROR] A Login Error has Occured.\n')
        return

def checkBingLogin(browser: WebDriver, isMobile: bool = False):
    try :
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
                time.sleep(2)
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
                time.sleep(2)
                try:
                    browser.find_element(By.ID, 'mHamburger').click()
                except:
                    pass
            try:
                time.sleep(2)
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
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Check Bing Login.\n')
    """
    #Refresh page
    browser.get('https://bing.com/')
    #Wait 5 seconds
    time.sleep(10)
    """
    try :
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
                    time.sleep(2)
                    browser.find_element(By.ID, 'mHamburger').click()
                time.sleep(2)
                POINTS_COUNTER = int(browser.find_element(By.ID, 'fly_id_rc').get_attribute('innerHTML'))
        except:
            checkBingLogin(browser, isMobile)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Check Bing Login Mobile.\n')

def waitUntilVisible(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    try :
        WebDriverWait(browser, time_to_wait).until(ec.visibility_of_element_located((by_, selector)))
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Wait Until Visible.\n')

def waitUntilClickable(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    try :
        WebDriverWait(browser, time_to_wait).until(ec.element_to_be_clickable((by_, selector)))
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Wait Until Clickable.\n')

def waitUntilQuestionRefresh(browser: WebDriver):
    try :
        tries = 0
        refreshCount = 0
        while True:
            try:
                browser.find_elements(By.CLASS_NAME, 'rqECredits')[0]
                return True
            except:
                if tries < 10:
                    tries += 1
                    time.sleep(1)
                else:
                    if refreshCount < 5:
                        browser.refresh()
                        refreshCount += 1
                        tries = 0
                        time.sleep(5)
                    else:
                        return False
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Wait Until Question Refresh.\n')

def waitUntilQuizLoads(browser: WebDriver):
    try :
        tries = 0
        refreshCount = 0
        while True:
            try:
                browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]')
                return True
            except:
                if tries < 10:
                    tries += 1
                    time.sleep(1)
                else:
                    if refreshCount < 5:
                        browser.refresh()
                        refreshCount += 1
                        tries = 0
                        time.sleep(5)
                    else:
                        return False
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Wait Until Quiz Loads.\n')

def findBetween(s: str, first: str, last: str) -> str:
    try : 
        try :
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Find Between.\n')

def getCCodeLangAndOffset() -> tuple:
    try :
        try :
            nfo = ipapi.location()
            lang = nfo['languages'].split(',')[0]
            geo = nfo['country']
            tz = str(round(int(nfo['utc_offset']) / 100 * 60))
            return(lang, geo, tz)
        except:
            return('fr-FR', 'FR', '120')
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get CCode Lang And Offset.\n')

def getGoogleTrends(numberOfwords: int) -> list:
    try :
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
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Google Trends.\n')

def getRelatedTerms(word: str) -> list:
    try :
        try :
            r = requests.get('https://api.bing.com/osjson.aspx?query=' + word, headers = {'User-agent': PC_USER_AGENT})
            return r.json()[1]
        except:
            return []
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Related Terms.\n')

def resetTabs(browser: WebDriver):
    try :
        try :
            curr = browser.current_window_handle

            for handle in browser.window_handles:
                if handle != curr:
                    browser.switch_to.window(handle)
                    time.sleep(1)
                    browser.close()
                    time.sleep(1)

            browser.switch_to.window(curr)
            time.sleep(1)
            browser.get(BASE_URL)
        except:
            browser.get(BASE_URL)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Reset Tabs.\n')

def getAnswerCode(key: str, string: str) -> str:
    try :
        t = 0
        for i in range(len(string)):
            t += ord(string[i])
        t += int(key[-2:], 16)
        return str(t)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Answer Code.\n')

def bingSearches(browser: WebDriver, numberOfSearches: int, isMobile: bool = False):
    try :
        global POINTS_COUNTER
        global searchesRemaining
        i = 0
        searchesRemaining = numberOfSearches
        search_terms = getGoogleTrends(numberOfSearches)
        for word in search_terms :
            i += 1
            print('[BING]', str(i) + "/" + str(numberOfSearches))
            points = bingSearch(browser, word, isMobile)
            if points <= POINTS_COUNTER :
                relatedTerms = getRelatedTerms(word)
                for term in relatedTerms :
                    points = bingSearch(browser, term, isMobile)
                    if isMobile and i>20 :
                        break
                    if not points <= POINTS_COUNTER :
                        break
            if points > 0:
                POINTS_COUNTER = points
            else:
                break
            searchesRemaining=(searchesRemaining-1)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying Complete Bing Searches.\n')
def bingSearch(browser: WebDriver, word: str, isMobile: bool):
    try :
        browser.get('https://bing.com')
        time.sleep(2)
        searchbar = browser.find_element(By.ID, 'sb_form_q')
        searchbar.send_keys(word)
        searchbar.submit()
        time.sleep(random.randint(10, 30))
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
                        time.sleep(2)
                        browser.find_element(By.ID, 'mHamburger').click()
                    except NoAlertPresentException :
                        pass
                time.sleep(2)
                points = int(browser.find_element(By.ID, 'fly_id_rc').get_attribute('innerHTML'))
        except:
            pass
        return points
    except:
        prRed('\n[ERROR] An Error has Occured While Trying Complete Bing Search.\n')

def completePromotionalItems(browser: WebDriver):
    try :
        try :
            item = getDashboardData(browser)["promotionalItem"]
            if (item["pointProgressMax"] == 100 or item["pointProgressMax"] == 200) and item["complete"] == False and (item["destinationUrl"] == BASE_URL or item["destinationUrl"].startswith("https://www.bing.com/")):
                browser.find_element(By.XPATH, '//*[@id="promo-item"]/section/div/div/div/span').click()
                time.sleep(2)
                browser.switch_to.window(window_name = browser.window_handles[1])
                time.sleep(8)
                browser.close()
                time.sleep(2)
                browser.switch_to.window(window_name = browser.window_handles[0])
                time.sleep(2)
        except:
            pass
    except:
        prRed('\n[ERROR] An Error has Occured While Trying Complete Promotional Items.\n')

def completeDailySetSearch(browser: WebDriver, cardNumber: int):
    try :
        time.sleep(5)
        browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[1])
        time.sleep(random.randint(13, 17))
        browser.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Daily Set Search.\n')

def completeDailySetSurvey(browser: WebDriver, cardNumber: int):
    try :
        time.sleep(5)
        browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a/div['+ str(cardNumber)+']/span').click()
        time.sleep(5)
        browser.switch_to.window(window_name = browser.window_handles[1])
        time.sleep(8)
        browser.find_element(By.XPATH, '//*[@id="btoption' + str(random.randint(0, 1)) + '"]/div[2]/div[2]' ).click()
        time.sleep(random.randint(10, 15))
        browser.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Daily Set Survey.\n')

def completeDailySetQuiz(browser: WebDriver, cardNumber: int):
    try :
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        time.sleep(2)
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
            elif numberOfOptions == 3:
                correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
                for i in range(3):
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
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Daily Set Quiz.\n')

def completeDailySetVariableActivity(browser: WebDriver, cardNumber: int):
    try :
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[1])
        time.sleep(8)
        try :
            browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
            waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 3)
        except (NoSuchElementException, TimeoutException):
            #tests
            counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
            try:
                numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
            except :
                print('DailySetVariableActivity failed to find numberOfQuestions')
                pass      
            #added radomizer and for loop
            try :
                counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                numberOfQuestions = (counter.split(" of ")[1])
                print('numberOfQuestions='+str(numberOfQuestions)) #delete me test
                for i in range(numberOfQuestions):
                    browser.find_element(By.XPATH, '//*[@id="QuestionPane' + i + '"]/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div/div/div/span[1]/span').click()
                    time.sleep(2)
                    browser.find_element(By.XPATH, '//*[@id="nextQuestionbtn' + i + '"]').click()
                    time.sleep(2)
                prRed('\n[Info] completeDailySetVariableActivity for loops completed\n') #delete me test
            except :
                prRed('\n[Error] completeDailySetVariableActivity for loops failed to run \n') #change or delete me test
                try :
                    browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[1]/div[2]/a[1]/div/div/div/span[1]/span').click()
                    time.sleep(2)
                    browser.find_element(By.XPATH, '//*[@id="nextQuestionbtn0"]').click()
                    time.sleep(2)
                    browser.find_element(By.XPATH, '//*[@id="QuestionPane1"]/div[1]/div[2]/a[1]/div/div/div/span[1]/span').click()
                    time.sleep(2)
                    browser.find_element(By.XPATH, '//*[@id="nextQuestionbtn1"]').click()
                    time.sleep(2)
                    browser.find_element(By.XPATH, '//*[@id="QuestionPane2"]/div[1]/div[2]/a[1]/div/div/div/span[1]/span').click()
                    time.sleep(2)
                    browser.find_element(By.XPATH, '//*[@id="nextQuestionbtn2"]').click()
                    time.sleep(3)
                    prRed('\n[Info] Hard Code Used\n') #delete me test
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
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Daily Set Variable Activity.\n')

def completeDailySetThisOrThat(browser: WebDriver, cardNumber: int):
    try :
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        time.sleep(2)
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
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Daily Set This Or That.\n')

def getDashboardData(browser: WebDriver) -> dict:
    try :
        dashboard = findBetween(browser.find_element(By.XPATH, '/html/body').get_attribute('innerHTML'), "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
        dashboard = json.loads(dashboard)
        return dashboard
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Dashboard Data.\n')

def completeDailySet(browser: WebDriver):
    try :
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
                            try:
                                if "PollScenarioId" in filters:
                                    print('[DAILY SET]', 'Completing poll of card ' + str(cardNumber))
                                    completeDailySetSurvey(browser, cardNumber)
                                else:
                                    print('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                                    completeDailySetVariableActivity(browser, cardNumber)
                            except :
                                prRed('\n[ERROR] An Error has Occured While Completing the Daily Poll.\n')
            except:
                resetTabs(browser)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Daily Set.\n')
           
def getAccountPoints(browser: WebDriver) -> int:
    try :
        return getDashboardData(browser)['userStatus']['availablePoints']
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Account Points.\n')

def completePunchCard(browser: WebDriver, url: str, childPromotions: dict):
    try :
        browser.get(url)
        for child in childPromotions:
            if child['complete'] == False:
                if child['promotionType'] == "urlreward":
                    browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                    time.sleep(2)
                    browser.switch_to.window(window_name = browser.window_handles[1])
                    time.sleep(random.randint(13, 17))
                    browser.close()
                    time.sleep(2)
                    browser.switch_to.window(window_name = browser.window_handles[0])
                    time.sleep(2)
                if child['promotionType'] == "quiz":
                    browser.execute_script("document.getElementsByClassName('offer-cta')[0].click()")
                    time.sleep(2)
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
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Punch Card.\n')

def completePunchCards(browser: WebDriver):
    try :
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
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Punch Cards.\n')

def completeMorePromotionSearch(browser: WebDriver, cardNumber: int):
    try :
        browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[1])
        time.sleep(random.randint(13, 17))
        browser.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete More Promotion Search.\n')

def completeMorePromotionQuiz(browser: WebDriver, cardNumber: int):
    try :
        browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
        time.sleep(2)
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
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete More Promotion Quiz.\n')

def completeMorePromotionABC(browser: WebDriver, cardNumber: int):
    try :
        browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
        time.sleep(2)
        browser.switch_to.window(window_name=browser.window_handles[1])
        time.sleep(8)
        counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
        numberOfQuestions = (counter.split(" of ")[1])
        for question in range(int(numberOfQuestions)):
            browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
            time.sleep(5)
            try:   
                browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                time.sleep(2)
            except:
                pass
            browser.find_element(By.XPATH, '//*[@id="nextQuestionbtn' + str(question) + '"]').click() #should fix more promo quiz
            time.sleep(5)
        time.sleep(5)
        browser.close()
        time.sleep(2)
        browser.switch_to.window(window_name=browser.window_handles[0])
        time.sleep(2)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete More Promotion ABC.\n')

def completeMorePromotionThisOrThat(browser: WebDriver, cardNumber: int):
    try :
        browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
        time.sleep(2)
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
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete More Promotion This Or That.\n')

def completeMorePromotions(browser: WebDriver):
    try :
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
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete More Promotions.\n')

def getRemainingSearches(browser: WebDriver):
    try :
        dashboard = getDashboardData(browser)
        searchPoints = 1
        counters = dashboard['userStatus']['counters']
        if not 'pcSearch' in counters:
            return 0, 0
        progressDesktop = counters['pcSearch'][0]['pointProgress'] + counters['pcSearch'][1]['pointProgress']
        targetDesktop = counters['pcSearch'][0]['pointProgressMax'] + counters['pcSearch'][1]['pointProgressMax']
        if targetDesktop == 50 : #Level 1 US
            searchPoints = 5
        elif targetDesktop >= 150 : #Level 2 US
            searchPoints = 5
        remainingDesktop = int(((targetDesktop - progressDesktop) / searchPoints))
        for i in range (10):
            if remainingDesktop == 30 + i :
                remainingDesktop = (remainingDesktop - i)
        remainingMobile = 0
        if dashboard['userStatus']['levelInfo']['activeLevel'] != "Level1":
            progressMobile = counters['mobileSearch'][0]['pointProgress']
            targetMobile = counters['mobileSearch'][0]['pointProgressMax']
            remainingMobile = int((targetMobile - progressMobile) / searchPoints)
        return remainingDesktop, remainingMobile
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Remaining Searches.\n')

def prRed(prt):
    print("\033[91m{}\033[00m".format(prt))
def prGreen(prt):
    print("\033[92m{}\033[00m".format(prt))
def prPurple(prt):
    print("\033[95m{}\033[00m".format(prt))
def prYellow(prt):
    print("\033[93m{}\033[00m".format(prt))

st = time.time()

prRed("""
███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗ 
████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝""")
prPurple("Version 2.0")

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
try:
    for account in ACCOUNTS:
        ACCOUNT_COUNTER +=1
        prPurple('\n[INFO] Starting Account '+str(ACCOUNT_COUNTER) + '/'+str(len(ACCOUNTS)) + ' !')
        prYellow('********************' + account['username'] + '********************')
        browser = browserSetup(True, PC_USER_AGENT)
        prGreen('[LOGIN] Logging-in as ' + account['username'] + " !")
        login(browser, account['username'], account['password'])
        prGreen('[LOGIN] Logged-in successfully !')
        startingPoints = POINTS_COUNTER
        prGreen('[POINTS] You have ' + str(POINTS_COUNTER) + ' points on your account !')

        browser.get('https://account.microsoft.com/')
        waitUntilVisible(browser, By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a', 20)

        if browser.find_element(By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a').get_attribute('target') == '_blank':
            BASE_URL = 'https://rewards.microsoft.com'
            browser.find_element(By.XPATH, '//*[@id="navs"]/div/div/div/div/div[4]/a').click()
            time.sleep(2)
            browser.switch_to.window(window_name=browser.window_handles[0])
            browser.close()
            browser.switch_to.window(window_name=browser.window_handles[0])
            time.sleep(10)
        else:
            BASE_URL = 'https://account.microsoft.com/rewards'
            browser.get(BASE_URL)
        try :
            print('[DAILY SET] Trying to complete the Daily Set...')
            completeDailySet(browser)
            prGreen('[DAILY SET] Completed the Daily Set successfully !')
        except :
            prRed('\n[ERROR] An Error has Occured While Completing the Daily Set.\n')
        try :
            print('[PUNCH CARDS] Trying to complete the Punch Cards...')
            completePunchCards(browser)
            prGreen('[PUNCH CARDS] Completed the Punch Cards successfully !')
        except :
            prRed('\n[ERROR] An Error has Occured While Completing the Punch Cards.\n')
        try :
            print('[MORE PROMO] Trying to complete More Promotions...')
            completeMorePromotions(browser)
            prGreen('[MORE PROMO] Completed More Promotions successfully !')
        except :
            prRed('\n[ERROR] An Error has Occured While Completing More Promotion.\n')
        remainingSearches, remainingSearchesM = getRemainingSearches(browser)
        retrySleep = random.randint(30, 60)
        if remainingSearches != 0:
            prPurple('[BING] Starting Desktop and Edge Bing searches...')
            bingSearches(browser, remainingSearches)
            prGreen('[BING] Finished Desktop and Edge Bing searches !\n')
            try:
                 if searchesRemaining != 0:
                    prRed('remainingSearches='+str(remainingSearches))
                    prRed('\n[Error] Desktop Seaches did not Complete !')
                    prYellow('[INFO] There are ' + str(remainingSearches) +' Searches Remaining !')
                    prYellow('[INFO] Retrying in ' + str(retrySleep) + 'seconds !')
                    time.sleep(retrySleep)
                    prPurple('[BING] Re-Trying Desktop and Edge Bing searches...')
                    bingSearches(browser, remainingSearches)
                    prGreen('[BING] Finished Re-Trying Desktop and Edge Bing searches !\n')
            except :
                print('[ERROR] An Error has Occured While Re-Trying Desktop and edge Bing searches')
            FIRST_RUN = False
            browser.quit()
        if FIRST_RUN == True :
            prRed('[ERROR] ' + str(account['username']) + ' Has Already Earned PC Points today !\n')
            prYellow('[INFO] Waiting ' + str(tempSleepTimer) + 'seconds !')
            time.sleep(tempSleepTimer)

        if remainingSearchesM != 0:
            prPurple('[INFO] Starting Mobile Account ' + str(ACCOUNT_COUNTER) + '/'+str(len(ACCOUNTS)) + ' !')
            browser = browserSetup(True, MOBILE_USER_AGENT)
            prGreen('[LOGIN] Logging-in as ' + account['username'] + " !")
            login(browser, account['username'], account['password'], True)
            prGreen('[LOGIN] Logged-in successfully !')
            prPurple('[BING] Starting Mobile Bing searches...')
            bingSearches(browser, remainingSearchesM, True)
            prGreen('[BING] Finished Mobile Bing searches !')
            try:
                if searchesRemaining != 0 : #retry mobile searches
                    prRed('\n[Error] Mobile Seaches did not Complete !')
                    prYellow('[INFO] There are ' + str(remainingSearches) +' Searches Remaining !')
                    prYellow('[INFO] Retrying in ' + str(retrySleep) + 'seconds !')
                    time.sleep(retrySleep)
                    prPurple('[INFO] Re-Trying Mobile Account ' + str(ACCOUNT_COUNTER) + '/'+str(len(ACCOUNTS)) + 'in ')
                    browser = browserSetup(True, MOBILE_USER_AGENT)
                    prGreen('[LOGIN] Logging-in as ' + account['username'] + " !")
                    login(browser, account['username'], account['password'], True)
                    prGreen('[LOGIN] Logged-in successfully !')
                    prPurple('[BING] Starting Mobile Bing searches...')
                    bingSearches(browser, remainingSearchesM, True)
                    prGreen('[BING] Finished Re-Trying Mobile Bing searches !')
            except :
                print('[ERROR] An Error has Occured While Re-Trying Desktop and edge Bing searches')
            FIRST_RUN_M = False
            browser.quit()
        if FIRST_RUN_M == True :
            prRed('[ERROR] ' + str(account['username']) + ' Has Already Earned Mobile Points Today !\n')
            prYellow('[INFO] Waiting ' + str(tempSleepTimer) + 'seconds !')
            time.sleep(tempSleepTimer)
        
        prGreen('[POINTS] You have earned ' + str(POINTS_COUNTER - startingPoints) + ' points today !')
        prGreen('[POINTS] You are now at ' + str(POINTS_COUNTER) + ' points !\n') 
        prYellow('********************' + account['username'] + '********************')
        prPurple('[INFO] ' + str(ACCOUNT_COUNTER)+'/' + str(len(ACCOUNTS)) + ' Accounts Completed !')
        try :
            if POINTS_COUNTER>=6500 and not path.exists(rewardsFile):
                f = open(rewardsFile, 'w')
                f.write('Microsoft Rewards Gift Card Info\n')
                f.write('\n' + str(account['username']) + ' - Has over 6500 points. Go Redeem a Gift Card.')
                f.close()
                prYellow('[INFO] Microsoft.Rewards.Gift.Card.Info.txt Created !\n')
                prPurple('[INFO] You have enough points to Redeem a $5 Gift Card !')
                REWARDS+=1
            elif POINTS_COUNTER>=6500 and path.exists(rewardsFile) :
                f = open(rewardsFile, 'a')
                f.write('\n' + str(account['username']) + ' - Has over 6500 points. Redeem a gift card.')
                f.close()
                prYellow('[INFO] Microsoft.Rewards.Gift.Card.Info.txt eddited')
                prPurple('[INFO] You have enough points to Redeem a $5 Gift Card !')
                REWARDS+=1
        except :
            prRed('\n[ERROR] An Error has Occured When Trying to Create or Write to .txt !\n')
        try:
            if ACCOUNT_COUNTER < len(ACCOUNTS):
                sleepTimer = random.randint(400, 600)
                prYellow('[INFO] Waiting ' + str(sleepTimer) +'seconds Until Continuing !\n')
                time.sleep(sleepTimer)
            elif ACCOUNT_COUNTER < len(ACCOUNTS) and FIRST_RUN == True and FIRST_RUN_M == True:
                longSleepTimer = random.randint(600, 800)
                prRed('[ERROR] '+ str(account['username']) + ' Has Already Earned All Points Available Today')
                prYellow('[INFO] Waiting ' + str(longSleepTimer) +'seconds Until Continuing !\n')
                time.sleep(longSleepTimer)
        except:
            prRed('[ERROR] An Error has Occured with First_run and First_runM SleepTimers !')
except OSError as err:
    prRed("\n[ERROR] OS error:", err,'\n')
except ValueError:
    prRed("\n[ERROR] Could not convert data to an integer.\n")
except Exception as err:
    prRed(f"\n[ERROR] Unexpected {err=}, {type(err)=}\n")
except :
    prRed('\n[ERROR] An Error has Occured.\n')
    raise
finally :
    try :
        if REWARDS == 1 :
            prGreen('[INFO] You have ' + str(REWARDS) + ' Gift Card Waiting to be Redeemed !\n [INFO] Check Microsoft.Rewards.Gift.Card.Info.txt For More Information')
        elif REWARDS >= 1 :
            prGreen('[INFO] You have ' + str(REWARDS) + ' Gift Cards Waiting to be Redeemed !\n [INFO] Check Microsoft.Rewards.Gift.Card.Info.txt For More Information')
    except :
        prRed('\n[ERROR] An Error has Occured While Displaying Rewards Earned.\n')
    TOTAL_TIME = time.time() - st
    prYellow('[INFO] Total Time elapsed: ' + time.strftime("%H:%M:%S", time.gmtime(TOTAL_TIME)))
    prYellow('\n[INFO] Thank you for using Microsoft Rewards Farmer !\nPress Any Key to Exit !')
    input()
    prYellow('GoodBye :)\n')