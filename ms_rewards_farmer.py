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

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, UnexpectedAlertPresentException, NoAlertPresentException

# Define user-agents
#rewardsErr ='C://Users//YourNameHere//Desktop//Microsoft.Rewards.Err.txt' #change YourNameHere to your pc's Username and delete the # infront of rewardsErr
#rewardsLog = 'C://Users//YourNameHere//Desktop//Microsoft.Rewards.Log.txt' #change YourNameHere to your pc's Username and delete the # infront of rewardsLog 
PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 10; Pixel 3) zAppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0. 3945.79 Mobile Safari/537.36'
BASE_URL = ""
POINTS_COUNTER = 0
ACCOUNT_COUNTER = 0
LOWREWARDS = 0
HIGHREWARDS = 0
FIRST_RUN = True
FIRST_RUN_M = True
ACCOUNTISSUE = False
PROTECTISSUE = False
COMPLETESEARCH = 0
RETRYING = False
RETRYINGM = False
CBL_COUNTER = 1
FIRSTWRITE = True
FAOPEN = False
ACCOUNTSWREWARD = []
HIGHACCOUNTSWREWARD = []
ERRCOUNT = 0
tempSleepTimer = random.randint(300, 450) #set to 300-450secs - time waiting if account has no pc or mobile searches from start
longSleepTimer = random.randint(500, 600) #Set to 500-600secs - time waiting between multiple accounts that already earned today's points
sleepTimer = random.randint(300, 500) #Set to 300-400secs - time waiting between multiple accounts AFTER earning points for the account

# Define browser setup function
def browserSetup(headless_mode: bool = False, user_agent: str = PC_USER_AGENT) -> WebDriver:
    try :
        # Create Chrome browser
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("user-agent=" + user_agent)
        options.add_argument('lang=' + LANG.split("-")[0])
        if headless_mode : #comment out this line of code to disable headless mode (make window visable) 
          options.add_argument("--headless") #comment out this line of code to disable headless mode (make window visable) 
        options.add_argument('log-level=3')
        chrome_browser_obj = webdriver.Chrome(options=options)
        return chrome_browser_obj
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Browser Setup.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Browser Setup.\n')
        FA.close()

def accountIssue(browser: WebDriver):
    global ACCOUNTISSUE
    try:
        locked = str(browser.find_element(By.XPATH, '//*[@id="StartHeader"]').get_attribute('innerHTML'))
        prRed('\n[WARNING] [FATAL ERROR] '+ str(locked) +' !\n')
        if locked.startswith('Your account has been') :
            prRed('\n[WARNING] [FATAL ERROR] Check if Account is Locked.\n')
            writeErr()
            FA.write('\n[WARNING] [FATAL ERROR] Check if Account is Locked.')
            FA.close()
            ACCOUNTISSUE = True
            pass
        elif locked.startswith('Votre compte a été') :
            prRed('\n[WARNING] [FATAL ERROR] Check if Account is Locked.\n')
            writeErr()
            FA.write('\n[WARNING] [FATAL ERROR] Check if Account is Locked.')
            FA.close()
            ACCOUNTISSUE = True
            pass
    except:
        pass
    try:
        Suspended = str(browser.find_element(By.XPATH, '//*[@id="error"]/h1').get_attribute('innerHTML'))
        prRed('\n[WARNING] [FATAL ERROR] '+ str(Suspended) +' !\n')
        if Suspended.startswith('Uh oh, it appears') :
            prRed('\n[WARNING] [FATAL ERROR] Check if Account is Suspended or Banned.\n')
            writeErr()
            FA.write('\n[WARNING] [FATAL ERROR] Check if Account is Suspended or Banned.')
            FA.close()
            ACCOUNTISSUE = True
            pass
        elif Suspended.startswith('Oh oh, il semble') :
            prRed('\n[WARNING] [FATAL ERROR] Check if Account is Suspended or Banned.\n')
            writeErr()
            FA.write('\n[WARNING] [FATAL ERROR] Check if Account is Suspended or Banned.')
            FA.close()
            ACCOUNTISSUE = True
            pass
    except:
        return
    
def protectAcc(browser: WebDriver):
    global PROTECTISSUE
    try:
        protect = str(browser.find_element(By.XPATH, '//*[@id="iSelectProofTitle"]').get_attribute('innerHTML'))
        prRed('\n[WARNING] [FATAL ERROR] '+ str(protect) +' !\n')
        if protect.startswith('Help us protect') :
            prRed('\n[WARNING] [FATAL ERROR] You need to manually sign in to ' + account['username'] + ' to verify the account !\n')
            writeErr()
            FA.write('\n[WARNING] [FATAL ERROR] You need to manually sign in to ' + account['username'] + ' to verify the account !\n')
            FA.close()
            PROTECTISSUE= True
            pass
        elif protect.startswith('Aidez-nous à protéger') :
            prRed('\n[WARNING] [FATAL ERROR] You need to manually sign in to ' + account['username'] + ' to verify the account !\n')
            writeErr()
            FA.write('\n[WARNING] [FATAL ERROR] You need to manually sign in to ' + account['username'] + ' to verify the account !\n')
            FA.close()
            PROTECTISSUE= True
            pass
    except:
        return

# Define login function
def login(browser: WebDriver, email: str, pwd: str, isMobile: bool = False):
    global CBL_RETRY
    try :
        # Access to bing.com
        browser.get('https://rewards.bing.com/')
        time.sleep(random.randint(4, 6))
        # Wait complete loading
        waitUntilVisible(browser, By.ID, 'loginHeader', 20)
        time.sleep(random.randint(4, 6))
        # Enter email
        print('[LOGIN]', 'Writing email...')
        browser.find_element(By.NAME, "loginfmt").send_keys(email)
        time.sleep(random.randint(4, 6))
        # Click next
        browser.find_element(By.ID, 'idSIButton9').click()
        # Wait 2 seconds
        time.sleep(random.randint(4, 6))
        # Wait complete loading
        waitUntilVisible(browser, By.ID, 'loginHeader', 20)
        # Enter password
        #browser.find_element(By.ID, "i0118").send_keys(pwd)
        browser.execute_script("document.getElementById('i0118').value = '" + pwd + "';")
        print('[LOGIN]', 'Writing password...')
        time.sleep(random.randint(4, 6))
        # Click next
        browser.find_element(By.ID, 'idSIButton9').click()
        # Wait 5 seconds
        time.sleep(random.randint(4, 6))
        if not isMobile :
            accountIssue(browser)
        if ACCOUNTISSUE == True :
            return
        if not isMobile :
            protectAcc(browser)
        if PROTECTISSUE == True:
            return
        time.sleep(1)
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
            time.sleep(random.randint(4, 6))
        except (NoSuchElementException, ElementNotInteractableException) as e:
            pass
        time.sleep(random.randint(6, 8))
        print('[LOGIN]', 'Logged-in !')
        # Check Login
        print('[LOGIN]', 'Ensuring login on Bing...')
        time.sleep(random.randint(4, 6))
        try:
            CBL_RETRY = True
            while CBL_RETRY == True :
                for x in range (CBL_COUNTER) : #retry if cbl mobile takes longer than 3mins CBL_COUNTER =1 times
                    if CBL_COUNTER > 1 :
                        prRed('[LOGIN] Retrying to Ensure Log in on Bing... Retry #'+str(CBL_COUNTER))
                    checkBingLogin(browser, isMobile)
        except:
            print('[ERROR] An Error has Occured While Ensuring login on Bing...')
            writeErr()
            FA.write('[ERROR] An Error has Occured While Ensuring login on Bing...')
            FA.close()
            pass        
    except OSError as err:
        prRed('\n[ERROR] A Login Error has Occured.\n')
        prRed('\n[ERROR] OS error:', err,'\n')
        browser.quit()
        writeErr()
        FA.write('\n[ERROR] A Login Error has Occured.')
        FA.write('\n[ERROR] OS error:', err,'')
        FA.close()

def checkBingLogin(browser: WebDriver, isMobile: bool = False):
    global CBL_RETRY
    global CBL_COUNTER
    try :
        cBL_st = time.time()
        global POINTS_COUNTER
        #Access Bing.com
        browser.get('https://bing.com/')
        # Wait 8 seconds
        time.sleep(random.randint(8, 10))
        #Accept Cookies
        try:
            browser.find_element(By.ID, 'bnp_btn_accept').click()
        except:
            pass
        try :
            if isMobile:
                try:
                    time.sleep(random.randint(6, 8))
                    try:
                        browser.find_element(By.XPATH,'//*[@id="mHamburger"]').click()
                    except:
                        browser.find_element(By.ID, 'mHamburger').click()
                        pass
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
                cBL_end = time.time() - cBL_st 
                if cBL_end >= 180 : #180=3mins
                    prPurple('[INFO] CBL Time Elapsed: ' + time.strftime("%H:%M:%S", time.gmtime(cBL_end)))
                    CBL_COUNTER =CBL_COUNTER+1
                    CBL_RETRY = True
                    time.clear()
                else :
                    CBL_RETRY = False
                    pass 
            #Wait 3 seconds
            time.sleep(3)
        except:
            prRed('\n[ERROR] An Error has Occured While Trying to Check Bing Login Mobile.\n')
            writeErr()
            FA.write('\n[ERROR] An Error has Occured While Trying to Check Bing Login Mobile.')
            FA.close()
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Check Bing Login Desktop.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Check Bing Login Desktop.')
        FA.close()
    if not isMobile:
        #Refresh page
        browser.get('https://bing.com/')
        #Wait 5 seconds
        time.sleep(10)
    try :
    #Update Counter
        try:
            if not isMobile:
                POINTS_COUNTER = int(browser.find_element(By.ID, 'id_rc').get_attribute('innerHTML'))
                CBL_RETRY = False
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
                CBL_RETRY = False
        except:
            pass
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Update Counter.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Update Counterp.')
        FA.close()

def waitUntilVisible(browser: WebDriver, by_: By, selector: str, time_to_wait: int):
    try :
        time.sleep(2)
        WebDriverWait(browser, time_to_wait).until(ec.visibility_of_element_located((by_, selector)))
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Wait Until Visible.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Wait Until Visible.')
        FA.close()

def waitUntilClickable(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    try :
        WebDriverWait(browser, time_to_wait).until(ec.element_to_be_clickable((by_, selector)))
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Wait Until Clickable.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Wait Until Clickable.')
        FA.close()

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Wait Until Question Refresh.')
        FA.close()

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Wait Until Quiz Loads.')
        FA.close() 

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Find Between.')
        FA.close()

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Get CCode Lang And Offset.')
        FA.close()

def getGoogleTrends(numberOfwords: int) -> list:
    global SEARCH_TERMS
    try :
        SEARCH_TERMS = []
        i = 0
        while len(SEARCH_TERMS) < numberOfwords :
            i += 1
            r = requests.get('https://trends.google.com/trends/api/dailytrends?hl=' + LANG + '&ed=' + str((date.today() - timedelta(days = i)).strftime('%Y%m%d')) + '&geo=' + GEO + '&ns=15')
            google_trends = json.loads(r.text[6:])
            for topic in google_trends['default']['trendingSearchesDays'][0]['trendingSearches']:
                SEARCH_TERMS.append(topic['title']['query'].lower())
                for related_topic in topic['relatedQueries']:
                    SEARCH_TERMS.append(related_topic['query'].lower())
            SEARCH_TERMS = list(set(SEARCH_TERMS))
        del SEARCH_TERMS[numberOfwords:(len(SEARCH_TERMS)+1)]
        return SEARCH_TERMS
    #search_terms
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Google Trends.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Get Google Trends.')
        FA.close()

def getRelatedTerms(word: str) -> list:
    try :
        try :
            r = requests.get('https://api.bing.com/osjson.aspx?query=' + word, headers = {'User-agent': PC_USER_AGENT})
            time.sleep(1)
            return r.json()[1]
        except:
            return []
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Related Terms.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Get Related Terms.')
        FA.close()

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Reset Tabs.')
        FA.close()

def getAnswerCode(key: str, string: str) -> str:
    try :
        t = 0
        for i in range(len(string)):
            t += ord(string[i])
        t += int(key[-2:], 16)
        return str(t)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Answer Code.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Get Answer Code.')
        FA.close()

def bingSearches(browser: WebDriver, numberOfSearches: int, isMobile: bool = False):
    try :
        global POINTS_COUNTER
        global SEARCHESREMAINING
        global COMPLETESEARCH
        i = 0
        SEARCHESREMAINING = numberOfSearches
        search_terms = getGoogleTrends(numberOfSearches)
        totalTimerSt = time.time()
        if isMobile:
            timeMobileTotalSt = time.time()
            mobileTimerSt = time.time()
        for word in search_terms :
            i = i + 1
            COMPLETESEARCH = COMPLETESEARCH + 1
            time.sleep(1)
            print('[BING]', str(i) + "/" + str(numberOfSearches))
            points = bingSearch(browser, word, isMobile)
            time.sleep(2)
            if points <= POINTS_COUNTER :
                relatedTerms = getRelatedTerms(word)
                for term in relatedTerms :
                    time.sleep(2)
                    points = bingSearch(browser, term, isMobile)
                    time.sleep(2)
                    if isMobile:
                        timerMobileLimit = time.time() - mobileTimerSt
                    if numberOfSearches <= 1:
                        break
                    if isMobile and timerMobileLimit>=1800: #1800=30 mins
                        prRed('\n[Error] Mobile Searches Ran Longer Than 25mins... Must Have Gotten Stuck.\n')
                        writeErr()
                        FA.write('\n[Error] Mobile Searches Ran Longer Than 25mins... Must Have Gotten Stuck.')
                        FA.close()
                        print("There are " + str(SEARCHESREMAINING) + " Searches Remaining !")
                        print('[INFO] Mobile Seach Total Time Elapsed: ' + time.strftime("%H:%M:%S", time.gmtime(timerMobileLimit)))
                        break
                    if not points <= POINTS_COUNTER :
                        break
            if points > 0:
                POINTS_COUNTER = points
            else:
                break
            SEARCHESREMAINING = SEARCHESREMAINING-1
        if isMobile: 
            TOTALMOBILETIMER = time.time() - timeMobileTotalSt
            prYellow('[INFO] Mobile Search Total Time Elapsed: ' + time.strftime("%H:%M:%S", time.gmtime(TOTALMOBILETIMER)))
        else:
            TIMETOTAL = time.time()-totalTimerSt
            prYellow('[INFO] PC Search Total Time Elapsed: ' + time.strftime("%H:%M:%S", time.gmtime(TIMETOTAL)))   
    except OSError as err:
        prRed('\n[ERROR] OS error:', err,'\n')
        writeErr()
        FA.write('\n[ERROR] OS error:', err,)
        FA.close()
    except ValueError:
        prRed('\n[ERROR] Could not convert data to an integer.\n')
        writeErr()
        FA.write('\n[ERROR] Could not convert data to an integer.')
        FA.close()
    except Exception as err:
        prRed(f'\n[ERROR] Unexpected {err=}, {type(err)=}\n')
        writeErr()
        FA.write(f'\n[ERROR] Unexpected {err=}, {type(err)=}\n')
        FA.close()
    except:
        if not isMobile:
            prRed('\n[ERROR] An Error has Occured While Trying to Complete PC Bing Searches.\n')
            writeErr()
            FA.write('\n[ERROR] An Error has Occured While Trying to Complete PC Bing Searches.')
            FA.close()
        else:
            prRed('\n[ERROR] An Error has Occured While Trying to Complete Mobile Bing Searches.\n')
            writeErr()
            FA.write('\n[ERROR] An Error has Occured While Trying to Complete Mobile Bing Searches.')
            FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)
        return COMPLETESEARCH

def bingSearch(browser: WebDriver, word: str, isMobile: bool):
    try :
        browser.get('https://bing.com')
        time.sleep(2)
        searchbar = browser.find_element(By.ID, 'sb_form_q')
        searchbar.send_keys(word)
        time.sleep(2)
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
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Bing Search.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Bing Search.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying Complete Promotional Items.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Daily Set Search.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Daily Set Survey.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

def completeDailySetQuiz(browser: WebDriver, cardNumber: int):
    try :
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[1])
        time.sleep(8)
        if not waitUntilQuizLoads(browser):
            resetTabs(browser)
            time.sleep(3)
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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Daily Set Quiz.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

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
            counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
            numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])          
            try :
                counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                numberOfQuestions = (counter.split(" of ")[1])
                for i in range(int(numberOfQuestions)):
                    browser.find_element(By.XPATH, '//*[@id="QuestionPane' + str(i) + '"]/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div/div/div/span[1]/span').click()
                    time.sleep(2)
                    browser.find_element(By.XPATH, '//*[@id="nextQuestionbtn' + str(i) + '"]').click()
                    time.sleep(4)
            except (NoSuchElementException, TimeoutException):
                prRed('\n[Error] An Error has Occured While Trying to Complete Daily Set Variable Activity.\n')
                writeErr()
                FA.write('\n[Error] An Error has Occured While Trying to Complete Daily Set Variable Activity.')
                FA.close()
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
        try:
            if browser.find_element(By.ID, "rqAnswerOption0").get_attribute("data-option") == correctAnswer:
                browser.find_element(By.ID, "rqAnswerOption0").click()
            else :
                browser.find_element(By.ID, "rqAnswerOption1").click()
                return
            correctAnswer = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
            time.sleep(3)
            if browser.find_element(By.ID, "rqAnswerOption0").get_attribute("data-option") == correctAnswer:
                browser.find_element(By.ID, "rqAnswerOption0").click()
            else :
                browser.find_element(By.ID, "rqAnswerOption1").click()
        except :
            pass
        time.sleep(10)
        browser.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Daily Set Variable Activity.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Daily Set Variable Activity.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Daily Set This Or That.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

def getDashboardData(browser: WebDriver) -> dict:
    try :
        dashboard = findBetween(browser.find_element(By.XPATH, '/html/body').get_attribute('innerHTML'), "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
        dashboard = json.loads(dashboard)
        time.sleep(2)
        return dashboard
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Dashboard Data.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Get Dashboard Data.')
        FA.close()

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
                                writeErr()
                                FA.write('\n[ERROR] An Error has Occured While Completing the Daily Poll.')
                                FA.close()
            except:
                resetTabs(browser)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Daily Set.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Daily Set.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)
           
def getAccountPoints(browser: WebDriver) -> int:
    try :
        return getDashboardData(browser)['userStatus']['availablePoints']
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Account Points.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Get Account Points.')
        FA.close()

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
                    try :
                        browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
                    except :
                        pass
                    maxQuestions = browser.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
                    try :
                        numberOfOptions = browser.execute_script("return _w.rewardsQuizRenderInfo.numberOfOptions")
                        for question in range(maxQuestions):
                            if numberOfOptions == 4:
                                correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
                                for i in range(4):
                                    if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                                        browser.find_element(By.ID, "rqAnswerOption" + str(i)).click()
                                        time.sleep(5)
                                        if not waitUntilQuestionRefresh(browser):
                                            return
                                        break
                                time.sleep(5)
                    except :
                        pass
                    try: #backup code
                        counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                        numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])                         
                        for question in range(numberOfQuestions):
                            browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                            time.sleep(5)
                            browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                            time.sleep(3)
                    except :
                       pass
                    time.sleep(5)
                    browser.close()
                    time.sleep(2)
                    browser.switch_to.window(window_name = browser.window_handles[0])
                    time.sleep(2)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete Punch Card.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Punch Card.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete Punch Cards.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

def completeMorePromotionSearch(browser: WebDriver, cardNumber: int):
    try :
        browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
        time.sleep(3)
        try:
            if browser.find_element(By.ID, 'legalTextBox'):
                try:
                    browser.find_element(By.XPATH,'//*[@id="legalTextBox"]/div/div/div[3]/a/span/ng-transclude').click()
                    time.sleep(2)
                    browser.switch_to.window(window_name = browser.window_handles[0])
                    time.sleep(2)
                except :

                    browser.switch_to.window(window_name = browser.window_handles[0])
                    time.sleep(2)
                    pass
        except:
            time.sleep(2)
            resetTabs(browser)
            pass
        time.sleep(2)
        resetTabs(browser)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete More Promotion Search.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete More Promotion Search.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete More Promotion Quiz.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

def completeMorePromotionABC(browser: WebDriver, cardNumber: int):
    try :
        browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
        time.sleep(2)
        browser.switch_to.window(window_name=browser.window_handles[1])
        time.sleep(8)
        try :
            browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        except:
            pass
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
            browser.find_element(By.XPATH, '//*[@id="nextQuestionbtn' + str(question) + '"]').click()
            time.sleep(5)
        time.sleep(5)
        browser.close()
        time.sleep(2)
        browser.switch_to.window(window_name=browser.window_handles[0])
        time.sleep(2)
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete More Promotion ABC.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete More Promotion ABC.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

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
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete More Promotion This Or That.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

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
        resetTabs(browser) 
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Complete More Promotions.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Complete More Promotions.')
        FA.close()
        time.sleep(2)
        browser.switch_to.window(window_name = browser.window_handles[0])
        time.sleep(2)

def getRemainingSearches(browser: WebDriver):
    try :
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
        remainingDesktop = int(((targetDesktop - progressDesktop) / searchPoints))
        remainingMobile = 0
        if dashboard['userStatus']['levelInfo']['activeLevel'] != "Level1":
            progressMobile = counters['mobileSearch'][0]['pointProgress']
            targetMobile = counters['mobileSearch'][0]['pointProgressMax']
            remainingMobile = int((targetMobile - progressMobile) / searchPoints)
        return remainingDesktop, remainingMobile
    except:
        prRed('\n[ERROR] An Error has Occured While Trying to Get Remaining Searches.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Get Remaining Searches.')
        FA.close()

def printDateAndTime():
    try :
        prYellow('[Date/Time] '+datetime.today().strftime('%m-%d-%Y %H:%M:%S'))
    except :
        prRed('\n[ERROR] An Error has Occured While Trying to Print Date And Time.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Print Date And Time.')
        FA.close()

def noReward() :
    global FIRSTWRITE
    global POINTS_COUNTER
    try :
        if not path.exists(rewardsLog):
            f = open(rewardsLog, 'w')
            f.write('Microsoft Rewards Gift Card Info\n')
            if FIRSTWRITE == True :
                f.write('\n\n'+datetime.today().strftime('%m-%d-%Y %H:%M:%S'))
                FIRSTWRITE = False
            f.write('\n' + str(account['username']) + ' - Has ' + str(POINTS_COUNTER) + ' points.')
            f.close()
            prYellow('[INFO] Microsoft.Rewards.Gift.Card.Info.txt Created !')
        else :
            f = open(rewardsLog, 'a')
            if FIRSTWRITE == True :
                f.write('\n'+datetime.today().strftime('%m-%d-%Y %H:%M:%S'))
                FIRSTWRITE = False
            f.write('\n' + str(account['username']) + ' - Has ' + str(POINTS_COUNTER) + ' points.')
            f.close()
            prYellow('[INFO] Microsoft.Rewards.Gift.Card.Info.txt eddited !')
    except :
        prRed('\n[ERROR] An Error has Occured While Trying to Log No Reward.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Log No Reward.')
        FA.close()

def lowReward() :
    try:
        global FIRSTWRITE
        global POINTS_COUNTER
        global ACCOUNTSWREWARD
        global LOWREWARDS
        if not path.exists(rewardsLog):
            f = open(rewardsLog, 'w')
            f.write('Microsoft Rewards Gift Card Info\n')
            if FIRSTWRITE == True :
                f.write('\n\n'+datetime.today().strftime('%m-%d-%Y %H:%M:%S'))
                FIRSTWRITE = False
            f.write('\n' + str(account['username']) + ' - Has ' + str(POINTS_COUNTER) + ' points and can redeem a 5$ Gift Card.')
            f.close()
            prYellow('[INFO] Microsoft.Rewards.Gift.Card.Info.txt Created !')
            prPurple('[INFO] You have ' + str(POINTS_COUNTER) + ' points! Go Redeem a $5 Gift Card !')
            ACCOUNTSWREWARD.append(str(account['username']))
            LOWREWARDS+=1
        else :
            f = open(rewardsLog, 'a')
            if FIRSTWRITE == True :
                f.write('\n\n'+datetime.today().strftime('%m-%d-%Y %H:%M:%S'))
                FIRSTWRITE = False
            f.write('\n' + str(account['username']) + ' - Has ' + str(POINTS_COUNTER) + ' points and can redeem a 5$ gift card.')
            f.close()
            prYellow('[INFO] Microsoft.Rewards.Gift.Card.Info.txt eddited !')
            prPurple('[INFO] You have '+ str(POINTS_COUNTER) +' points! Go Redeem a $5 Gift Card !')
            ACCOUNTSWREWARD.append(str(account['username']))
            LOWREWARDS+=1
    except :
        prRed('\n[ERROR] An Error has Occured While Trying to Log Low Reward.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Log Low Reward.')
        FA.close()

def highReward() :
    try :
        global FIRSTWRITE
        global POINTS_COUNTER
        global HIGHACCOUNTSWREWARD
        global HIGHREWARDS
        if not path.exists(rewardsLog):
            f = open(rewardsLog, 'w')
            f.write('Microsoft Rewards Gift Card Info\n')
            if FIRSTWRITE == True :
                f.write('\n\n'+datetime.today().strftime('%m-%d-%Y %H:%M:%S'))
                FIRSTWRITE = False
            f.write('\n' + str(account['username']) + ' - Has ' + str(POINTS_COUNTER) + ' points and can redeem a $10 Gift Card.')
            f.close()
            prYellow('[INFO] Microsoft.Rewards.Gift.Card.Info.txt Created !')
            prPurple('[INFO] You have ' + str(POINTS_COUNTER) + ' points! Go Redeem a $10 Gift Card !')
            HIGHACCOUNTSWREWARD.append(str(account['username']))
            HIGHREWARDS+=1
        else :
            f = open(rewardsLog, 'a')
            if FIRSTWRITE == True :
                f.write('\n'+datetime.today().strftime('%m-%d-%Y %H:%M:%S'))
                FIRSTWRITE = False
            f.write('\n' + str(account['username']) + ' - Has ' + str(POINTS_COUNTER) + ' points and can redeem a $10 gift card.')
            f.close()
            prYellow('[INFO] Microsoft.Rewards.Gift.Card.Info.txt eddited !')
            prPurple('[INFO] You have '+ str(POINTS_COUNTER) +' points! Go Redeem a $10 Gift Card !')
            HIGHACCOUNTSWREWARD.append(str(account['username']))
            HIGHREWARDS+=1
    except :
        prRed('\n[ERROR] An Error has Occured While Trying to Log High Reward.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Log High Reward.')
        FA.close()

def writeErr() :
    global FAOPEN
    global FA
    global ERRCOUNT
    try :
        if FAOPEN == False :
            FA = open(rewardsErr, 'a')
            FAOPEN = True
        FA.write('\n\n'+datetime.today().strftime('%m-%d-%Y %H:%M:%S'))
        FA.write('\n' + str(account['username']))
        printDateAndTime()
        prYellow('[INFO] Microsoft.Rewards.Err.txt eddited !')
        ERRCOUNT = ERRCOUNT + 1
        FAOPEN = False
    except :
        prRed('\n[ERROR] An Error has Occured While Trying to Write Err.\n')

def displayAccountWRewards() :
    global LOWREWARDS
    global HIGHREWARDS
    global ACCOUNTSWREWARD
    global HIGHACCOUNTSWREWARD
    anyRewards = False
    try :
        if LOWREWARDS == 1 :
            prGreen('\n[INFO] You have ' + str(LOWREWARDS) + ' $5 Gift Card Waiting to be Redeemed on ' + str(ACCOUNTSWREWARD))
            anyRewards = True
        elif LOWREWARDS >= 1 :
            prGreen('\n[INFO] You have ' + str(LOWREWARDS) + ' $5 Gift Cards Waiting to be Redeemed on ' + str(ACCOUNTSWREWARD))
            anyRewards = True
        if HIGHREWARDS == 1 :
            prGreen('\n[INFO] You have ' + str(HIGHREWARDS) + ' $10 Gift Card Waiting to be Redeemed on ' + str(HIGHACCOUNTSWREWARD))
            anyRewards = True
        elif HIGHREWARDS >= 1 :
            prGreen('\n[INFO] You have ' + str(HIGHREWARDS) + ' $10 Gift Cards Waiting to be Redeemed on ' + str(HIGHACCOUNTSWREWARD))
            anyRewards = True
        if anyRewards == True :
            prGreen('\n\n[INFO] Check '+str(rewardsLog)+' For More Information !')
    except :
        prRed('\n[ERROR] An Error has Occured While Trying to Display Account W Rewards.\n')
        writeErr()
        FA.write('\n[ERROR] An Error has Occured While Trying to Display Account W Rewards.')
        FA.close()

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
prPurple("Version 3.0")

LANG, GEO, TZ = getCCodeLangAndOffset()
try :
    FA = open(rewardsErr, 'a')
    FA.write('\n\nMicrosoft Rewards Err Log Created On ' + datetime.today().strftime('%m-%d-%Y %H:%M:%S'))
    FA.close()
except:
    prRed('[ERROR] You do not have rewardsErr set up correctly.')
    pass

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
        pcMobileTimerTotal = time.time()
        printDateAndTime()
        prPurple('[INFO] Starting Account '+str(ACCOUNT_COUNTER) + '/'+str(len(ACCOUNTS)) + ' !' )
        prYellow('********************' + account['username'] + '********************')
        browser = browserSetup(True, PC_USER_AGENT)
        prGreen('[LOGIN] Logging-in as ' + account['username'] + ' !')
        login(browser, account['username'], account['password'])
        if ACCOUNTISSUE == True :
            browser.quit()
            prRed('\n[WARNING] [FATAL ERROR] Check if '+ str(account['username']) +' is Locked, Suspended, or Banned.\n')
            writeErr()
            FA.write('\n[WARNING] [FATAL ERROR] Check if '+ str(account['username']) +' is Locked, Suspended, or Banned.')
            FA.close()
            ACCOUNTISSUE = False
            prRed('[INFO] '+ account['username'] + ' Was Skipped! No Points were earned!\n')
            prYellow('********************' + account['username'] + '********************')
            prPurple('[INFO] ' + str(ACCOUNT_COUNTER)+'/' + str(len(ACCOUNTS)) + ' Accounts Completed ! ')
            prYellow('[INFO] Waiting ' + str(sleepTimer) + 'seconds Until Continuing... \n')
            time.sleep(sleepTimer)
            continue 
        if PROTECTISSUE == True :
            browser.quit()
            prRed('\n[WARNING] [FATAL ERROR] You need to manually sign in to ' + account['username'] + ' to verify the account !\n')
            writeErr()
            FA.write('\n[WARNING] [FATAL ERROR] You need to manually sign in to ' + account['username'] + ' to verify the account !\n')
            FA.close()
            PROTECTISSUE = True
            prRed('[INFO] '+ account['username'] + ' Was Skipped! No Points were earned!\n')
            prYellow('********************' + account['username'] + '********************')
            prPurple('[INFO] ' + str(ACCOUNT_COUNTER)+'/' + str(len(ACCOUNTS)) + ' Accounts Completed ! ')
            prYellow('[INFO] Waiting ' + str(sleepTimer) + 'seconds Until Continuing... \n')
            time.sleep(sleepTimer)
            continue 
        prGreen('[LOGIN] Logged-in Successfully !')
        startingPoints = POINTS_COUNTER
        prGreen('[POINTS] You have ' + str(POINTS_COUNTER) + ' points on your account !')
        time.sleep(random.randint(10, 15))
        try :
            BASE_URL = 'https://rewards.bing.com/'
            browser.get(BASE_URL)
        except:
            prRed('[ERROR] Could not Loading https://rewards.bing.com/.')
            FA.write('\n[ERROR] Could not Loading https://rewards.bing.com/.')
            FA.close()
            pass
        waitUntilVisible(browser, By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[1]/div/card-content/mee-rewards-daily-set-item-content/div', 10)
        try :
            printDateAndTime()
            print('[DAILY SET] Trying to complete the Daily Set...')
            completeDailySet(browser)
            prGreen('[DAILY SET] Completed the Daily Set successfully !')
        except :
            prRed('\n[ERROR] An Error has Occured While Completing the Daily Set.\n')
            writeErr()
            FA.write('\n[ERROR] An Error has Occured While Completing the Daily Set.')
            FA.close()
        try :
            print('[PUNCH CARDS] Trying to complete the Punch Cards...')
            completePunchCards(browser)
            prGreen('[PUNCH CARDS] Completed the Punch Cards successfully !')
        except :
            prRed('\n[ERROR] An Error has Occured While Completing the Punch Cards.\n')
            writeErr()
            FA.write('\n[ERROR] An Error has Occured While Completing the Punch Cards.')
            FA.close()
        try :
            print('[MORE PROMO] Trying to complete More Promotions...')
            completeMorePromotions(browser)
            prGreen('[MORE PROMO] Completed More Promotions successfully !')
        except :
            prRed('\n[ERROR] An Error has Occured While Completing More Promotion.\n')
            writeErr()
            FA.write('\n[ERROR] An Error has Occured While Completing More Promotion.')
            FA.close()
        remainingSearches, remainingSearchesM = getRemainingSearches(browser)
        retrySleep = random.randint(250, 300)

        if remainingSearches != 0:
            printDateAndTime()
            prPurple('[BING] Starting Desktop and Edge Bing Searches...')
            bingSearches(browser, remainingSearches)
            FIRST_RUN = False
            browser.quit()            
            if SEARCHESREMAINING == 0 :
                printDateAndTime()
                prGreen('[BING] Finished Desktop and Edge Bing searches '+str(ACCOUNT_COUNTER) + '/'+str(len(ACCOUNTS)) + ' ! ')
                prPurple('[INFO] ' + str(account['username']) + ' Has Earned All Desktop Points today !')
                prYellow('[INFO] Waiting ' + str(tempSleepTimer) + 'seconds Until Continuing... \n')
                time.sleep(tempSleepTimer)
            else :
                printDateAndTime()
                prRed('\n[ERROR] ' + str(account['username']) + ' Has NOT Earned All Desktop Points today.\n')
                writeErr()
                FA.write('\n[ERROR] ' + str(account['username']) + ' Has NOT Earned All Desktop Points today.')
                FA.close()
                prYellow('[INFO] There are ' + str(SEARCHESREMAINING) +' Searches Remaining !')
                prYellow('[INFO] Waiting ' + str(sleepTimer) + 'seconds Until Continuing... \n')
                time.sleep(sleepTimer)    
        else :
            browser.quit()
            prRed('\n[ERROR] '+ str(account['username']) + ' Has Already Earned All Desktop Points Available Today.\n')
            writeErr()
            FA.write('\n[ERROR] '+ str(account['username']) + ' Has Already Earned All Desktop Points Available Today.')
            FA.close()
            prYellow('\n[INFO] Waiting ' + str(longSleepTimer) +'seconds Until Continuing... \n')
            time.sleep(longSleepTimer)
        try: 
            if remainingSearchesM != 0 :
                printDateAndTime()
                prPurple('[INFO] Starting '+ str(account['username']) +' Mobile Account ' + str(ACCOUNT_COUNTER) + '/'+str(len(ACCOUNTS)) + ' ! ')
                browser = browserSetup(True, MOBILE_USER_AGENT)
                prGreen('[LOGIN] Logging-in as ' + account['username'] + " !")
                login(browser, account['username'], account['password'], True)
                time.sleep(2)
                if ACCOUNTISSUE == True :
                    browser.quit()
                    prRed('\n[WARNING] [FATAL ERROR] Check if '+ str(account['username']) +' is Locked, Suspended, or Banned.\n')
                    writeErr()
                    FA.write('\n[WARNING] [FATAL ERROR] Check if '+ str(account['username']) +' is Locked, Suspended, or Banned.')
                    FA.close()
                    ACCOUNTISSUE = False
                    prRed('[INFO] No Points were earned!\n')
                    prYellow('********************' + account['username'] + '********************')
                    prPurple('[INFO] ' + str(ACCOUNT_COUNTER)+'/' + str(len(ACCOUNTS)) + ' Accounts Completed ! ')
                    prYellow('[INFO] Waiting ' + str(sleepTimer) + 'seconds Until Continuing... \n')
                    time.sleep(sleepTimer)
                    continue
                prGreen('[LOGIN] Logged-in Successfully !')
                printDateAndTime()
                prPurple('[BING] Starting Mobile Bing searches... ')
                bingSearches(browser, remainingSearchesM, True)
                FIRST_RUN_M = False
                browser.quit()
                if ACCOUNT_COUNTER == len(ACCOUNTS):
                    if SEARCHESREMAINING == 0 :
                        printDateAndTime()
                        prGreen('[BING] Finished Mobile Bing searches '+str(ACCOUNT_COUNTER) + '/'+str(len(ACCOUNTS)) + ' ! ')
                        prPurple('[INFO] ' + str(account['username']) + ' Has Earned All Mobile Points Today !\n')
                else:                
                    if SEARCHESREMAINING == 0 :
                        printDateAndTime()
                        prGreen('[BING] Finished Mobile Bing searches '+str(ACCOUNT_COUNTER) + '/'+str(len(ACCOUNTS)) + ' ! ')
                        prPurple('[INFO] ' + str(account['username']) + ' Has Earned All Mobile Points Today !')
                    else :
                        prRed('\n')
                        printDateAndTime()
                        prRed('[ERROR] ' + str(account['username']) + ' Has NOT Earned All Mobile Points Today.\n')
                        writeErr()
                        FA.write('[ERROR] ' + str(account['username']) + ' Has NOT Earned All Mobile Points Today.')
                        FA.close()
            else :
                if FIRST_RUN_M==True and FIRST_RUN==True:
                    prRed('\n')
                    printDateAndTime()
                    prRed('[INFO] '+ str(account['username']) + ' Has Already Earned All Mobile Points Available Today ! ' + '\n')
                else:
                    prRed('\n')
                    printDateAndTime()
                    prRed('[INFO] '+ str(account['username']) + ' Has Already Earned All Mobile Points Available Today ! ' + '\n')
                    prYellow('\n[INFO] Waiting ' + str(longSleepTimer) +'seconds Until Continuing... \n')
                    time.sleep(longSleepTimer)
        except:
            prRed('\n[ERROR] An Error has Occured While Trying to Run Mobile Searches.\n')
            writeErr()
            FA.write('\n[ERROR] An Error has Occured While Trying to Run Mobile Searches.')
            FA.close()
        try : #Account logger
            if 6500 <= POINTS_COUNTER < 13000: # $5 reward
                lowReward()
            elif POINTS_COUNTER >= 13000: # $10 reward
                highReward()
            else : # no reward
                noReward()
        except :
            prRed('\n[ERROR] An Error has Occured When Trying to Create or Write to .txt .\n')
            pass
        prGreen('[POINTS] You have earned ' + str(POINTS_COUNTER - startingPoints) + ' points today !')
        prGreen('[POINTS] You are now at ' + str(POINTS_COUNTER) + ' points !\n') 
        prYellow('********************' + account['username'] + '********************')
        prPurple('[INFO] ' + str(ACCOUNT_COUNTER)+'/' + str(len(ACCOUNTS)) + ' Accounts Completed ! ')
        TIMETOTAL = time.time()-pcMobileTimerTotal
        prYellow('[INFO] '+ str(account['username']) +' Total Time Elapsed: ' + time.strftime("%H:%M:%S", time.gmtime(TIMETOTAL)))
        try:
            if ACCOUNT_COUNTER < len(ACCOUNTS) and FIRST_RUN == True and FIRST_RUN_M == True:
                prRed('\n')
                printDateAndTime()
                prRed('[ERROR] '+ str(account['username']) + ' Has Already Earned All Points Available Today. '  + '\n')
                prYellow('\n[INFO] Waiting ' + str(longSleepTimer) +'seconds Until Continuing... \n')
                time.sleep(longSleepTimer)
            elif ACCOUNT_COUNTER < len(ACCOUNTS):
                prYellow('[INFO] Waiting ' + str(sleepTimer) +'seconds Until Continuing... \n')
                time.sleep(sleepTimer)
        except:
            prRed('\n[ERROR] An Error has Occured with First_run and First_runM SleepTimers.\n')
            writeErr()
            FA.write('\n[ERROR] An Error has Occured with First_run and First_runM SleepTimers.')
            FA.close()
            pass
except OSError as err:
    prRed('\n[ERROR] OS error:', err,'\n')
    browser.quit()
    writeErr()
    FA.write('\n[ERROR] OS error:', err,'')
    FA.close()
except ValueError:
    prRed('\n[ERROR] Could not convert data to an integer.\n')
    browser.quit()
    writeErr()
    FA.write('\n[ERROR] Could not convert data to an integer.')
    FA.close()
except Exception as err:
    prRed(f'\n[ERROR] Unexpected {err=}, {type(err)=}\n')
    browser.quit()
    writeErr()
    FA.write(f'\n[ERROR] Unexpected {err=}, {type(err)=}')
    FA.close()
    raise
finally :
    displayAccountWRewards()
    try :
        FA = open(rewardsErr, 'a')
        FA.write('\n\n'+datetime.today().strftime('%m-%d-%Y %H:%M:%S'))
        FA.write(' Total Errors: ' + str(ERRCOUNT) + '\n')
        FA.close()
    except :
        pass
    TOTAL_TIME = time.time() - st
    prPurple('\n\n[INFO] MS Farmer Total Time Elapsed: ' + time.strftime("%H:%M:%S", time.gmtime(TOTAL_TIME)) + '\n')
    prYellow('[INFO] Thank you for using Microsoft Rewards Farmer ! ')
    prYellow('[INFO] Press Any Key to Exit !')
    input() #comment out or delete this line to auto exit when complete. ([WARNING] You will not see errors without this line !)
    prPurple('[INFO] Have a Good Day! GoodBye :)\n')