from selenium.webdriver.common.keys import Keys
from selenium import webdriver
# from seleniumwire import webdriver as uc
import requests
import random
import json
import time
import os
from datetime import datetime
import string
from proxyscrape import create_collector
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import concurrent.futures
import threading
from fake_useragent import UserAgent



def autoscrape():
    collector = create_collector('my-collector', 'https')
    proxies = collector.get_proxies({'anonymous': True})
    print(len(proxies))
    selection = random.choice(proxies)
    proxy = str(selection[0] + ":" + selection[1])
    return proxy



def proxyfile():
    with open("config/proxies.txt", "r") as f:
        proxies = f.readlines()
    proxy = random.choice(proxies)
    return proxy



def emails():
    with open("config/emails.txt", "r") as f:
        lines = f.readlines()
        email = random.choice(lines).strip('\n')
    with open("config/emails.txt", 'w') as output_file:
        output_file.writelines(line for line in lines if line not in email)
    return email
    # email = str(''.join(random.choice(string.ascii_letters) for x in range(10))) + "@gmail.com"


def grabtoken(email, passwd):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Host': 'discord.com',
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Referer': 'https://discord.com/register',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    json = {
        'email': email,
        'password': passwd,
    }

    esafaf = requests.post('https://discord.com/api/v6/auth/@me', headers=headers, json=json)
    rab = esafaf.json()
    print("\nCaptcha finished, grabbing token.")
    token = rab['token']
    return token


def ratelimit():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Host': 'discord.com',
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Referer': 'https://discord.com/register',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    json = {
        'captcha_key': 'null',
        'consent': 'true',
        'date_of_birth': 'null',
        'email': 'null',
        'fingerprint': 'null',
        'gift_code_sku_id': 'null',
        'invite': 'null',
        'password': 'null',
        'username': 'null'
    }

    esafaf = requests.post('https://discord.com/api/v8/auth/register', headers=headers, json=json)
    status_code = esafaf.status_code
    json = esafaf.json()
    return status_code, json


def gettoken(asef, passwd, email):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Host': 'discord.com',
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Referer': 'https://discord.com/register',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    json = {
        'email': email,
        'password': passwd,
    }

    esafaf = requests.post('https://discord.com/api/v6/auth/login', headers=headers, json=json)
    rab = esafaf.json()
    print("\nCaptcha finished, grabbing token.\n")
    print("JSON: " + str(rab))
    try:
        token = rab['token']
    except:
        token = "Could not get token."
        return token
    file1 = open("results/tokens.txt","a+")
    file1.write("\n{}".format(rab['token']))
    file1 = open("results/accs.txt","a+")
    file1.write("\n\nUsername: {}".format(asef))
    file1.write("\nEmail: {}".format(email))
    file1.write("\nPassword: {}".format(passwd))
    return token


def resend(token):
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16',
        'Host': 'discordapp.com',
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Authorization': token,
        'Content-Type': 'application/json',
        'Referer': 'https://discordapp.com',
        'DNT': '1',
        'Connection': 'keep-alive'
    }


    response = requests.post('https://discordapp.com/api/v6/auth/verify/resend', headers=headers)
    print(response.json())












def settings():
    months = ['December', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']

    selection_month = random.choice(months)
    selection_day = random.randint(1,28)

    r2 = requests.get("http://names.drycodes.com/10")
    fem = r2.json()
    asef = random.choice(fem)
    # r2 = requests.get('https://randomuser.me/api/?inc=login')
    # asef = fem['results'][0]['login']['username']
    # passwd = fem['results'][0]['login']['password']


    r3 = requests.get('https://www.dinopass.com/password/simple')
    passwd = r3.text
    return asef, passwd, selection_month, selection_day


def get_proxys(data_file):
    proxys = []
    with open(data_file, "r") as fd:
        for line in fd.readlines():
            line = line.strip()
            if not line:
               continue
            proxys.append(line)
        proxy = random.choice(proxys)
    return proxy




def browser(asef, passwd, selection_month, selection_day, email, proxy):
    # uc.TARGET_VERSION = 78
    options = uc.ChromeOptions()
    #ua = UserAgent()
    #userAgent = ua.random
    #print(userAgent)
    #options.add_argument(f'user-agent={userAgent}')
    options.add_argument('--proxy-server=' + str(proxy))
    print('Proxy: ' + str(proxy))
    options.add_extension("./extensions/buster_chrome.crx")
    options.add_extension("./extensions/xpather.crx")
    # options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--enable-features=ReaderMode")

    prefs = {"profile.managed_default_content_settings.images": 2,
             "profile.default_content_setting_values.notifications": 2,
             "profile.managed_default_content_settings.stylesheets": 2,
             "profile.managed_default_content_settings.cookies": 2,
             "profile.managed_default_content_settings.javascript": 1,
             "profile.managed_default_content_settings.plugins": 1,
             "profile.managed_default_content_settings.popups": 2,
             "profile.managed_default_content_settings.geolocation": 2,
             "profile.managed_default_content_settings.media_stream": 2,
             }
    prefs1 = {"profile.managed_default_content_settings.images": 2}

    options.add_experimental_option("prefs", prefs)

    options.binary_location = r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
    chrome_driver_binary = "./selenium"

    driver = uc.Chrome(chrome_options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
    driver.set_page_load_timeout(60)
    for i in range(2):
        try:
            driver.get("https://discord.com/register")
            navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
            dom_complete = driver.execute_script("return window.performance.timing.domComplete")
            waittime = int(round(dom_complete - navigation_start)) / 1000
            print("Time to connect & load the Discord page: " + str(waittime))
#            driver.execute_script("window.open('https://www.yinsiduanxin.com/mail.html')")
#            driver.switch_to.window(driver.window_handles[1])
            break
        except:
            print("failed to connect")
            driver.quit()


#    driver.find_element_by_xpath("//button[contains(string(), '随机邮箱')]").click()
#    time.sleep(0.5)
#    emaill = driver.find_element_by_xpath("//span[contains(string(), '@mailscode.com')]").text

    driver.switch_to.window(driver.window_handles[0])
    sleeptime = int(500) / 1000
    try:
        enter_searchbar = driver.find_element_by_name("email")
        enter_searchbar.send_keys(email) #l)
        time.sleep(sleeptime)
        enter_user = driver.find_element_by_name("username")
        enter_user.send_keys(asef)
        time.sleep(sleeptime)
        enter_passwd = driver.find_element_by_name("password")
        enter_passwd.send_keys(passwd)
        time.sleep(sleeptime)
        enter_month = driver.find_element_by_id("react-select-2-input")
        enter_month.send_keys(selection_month, Keys.ENTER)
        time.sleep(sleeptime)
        enter_day = driver.find_element_by_id("react-select-3-input")
        enter_day.send_keys(selection_day, Keys.ENTER)
        time.sleep(sleeptime)
        enter_year = driver.find_element_by_id("react-select-4-input")
        enter_year.send_keys(random.randint(1988, 1997), Keys.ENTER)
        time.sleep(sleeptime)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(sleeptime)
    except:
        print("Value input failed due to unloaded elements.")
        driver.quit()

    try:
        driver.find_element_by_xpath("//div[contains(string(), 'Email is already registered')]").is_displayed()
        email = emails()
        enter_searchbar = driver.find_element_by_name("email")
        enter_searchbar.clear()
        enter_searchbar.send_keys(email)
        time.sleep(sleeptime)
        driver.find_element_by_xpath("//button[@type='submit']").click()
    except:
        print("Email was not used before.")

    try:
        driver.find_element_by_xpath("//span[contains(string(), 'Password is too weak or common to use')]")
        enter_passwd = driver.find_element_by_name("password")
        enter_passwd.send_keys("321!@#")
        time.sleep(sleeptime)
        driver.find_element_by_xpath("//button[@type='submit']").click()
    except:
        print("Password was strong enough.")

    try:
        driver.find_element_by_xpath("//div[contains(string(), 'You are being rate limited')]").is_displayed()
        result = ratelimit()
        if "429" in str(result[0]):
            print("Ratelimited for " + str(round(result[1]['retry_after'])) + " seconds. Waiting until that is over.")
            time.sleep(int(round(result[1]['retry_after'])))
            driver.find_element_by_xpath("//button[@type='submit']").click()
    except:
        print("Registration was not ratelimited.")

    wait = WebDriverWait(driver, 300)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[attribute::*[contains(name(), 'a')]]")))
    #wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-']")))
    wait.until(EC.element_to_be_clickable((By.ID ,"recaptcha-anchor"))).click()


    time.sleep(2)

    for _ in range(10):
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB + " ")
        actions.perform()
        time.sleep(5)
        try:
            #wait = WebDriverWait(driver, 3)
            #wait.until(EC.presence_of_element_located(By.XPATH, "/html/body/div/div/div[1]"))
            driver.find_element_by_xpath("//iframe[attribute::*[contains(name(), 'a')]]/html/body/div/div/div[1]")
            print("Multiple captcha solving needed.")
        except:
            print("breaking")
            break


#    try:
#        wait = WebDriverWait(driver, 30)
#        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='a-']")))
#        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='rc-audiochallenge-error-message']")))
#        print("succeeded.")
#    except:
#        print("passed")


    wait = WebDriverWait(driver, 600)
    desired_url = "https://discord.com/channels/@me"
    wait.until(lambda driver: driver.current_url == desired_url)
    time.sleep(3)
    try:
        driver.find_element_by_xpath("//h2[contains(string(), 'Add Friend')]")
        print("Token works fine.")
    except:
        print("We have been either email or phone-locked.")

#    driver.switch_to.window(driver.window_handles[1])
#    time.sleep(2)
#    driver.find_element_by_xpath("//button[contains(string(), '接收邮件')]").click()
#    time.sleep(2)
#    driver.find_element_by_xpath("//td[contains(string(), 'Discord')]").click()
#    time.sleep(2)
#    driver.find_element_by_xpath("//a[contains(string(), 'Verify Email')]").click()
    driver.quit()


def workers():
    MAX_WORKERS = 1
    threads = []
    for i in range(MAX_WORKERS):
        setting = settings()
        proxy = get_proxys('config/proxies.txt')
        email = emails()
        new_thread = threading.Thread(target=browser, args=(setting[0], setting[1], setting[2], setting[3], email, proxy,), daemon=True).start()
        threads.append(new_thread)


if __name__ == "__main__":
    while True:
        start_gen_time = datetime.now()
        timee = ratelimit()
        if "429" in str(timee[0]):
            print("Please wait " + str(round(timee[1]['retry_after'])) + " seconds.")
            time.sleep(int(round(timee[1]['retry_after'])))
        else:
            print("No ratelimit detected.")
        setting = settings()
        proxy = get_proxys('config/proxies.txt')
        email = emails()
        browser(setting[0], setting[1], setting[2], setting[3], email, proxy)
        result = gettoken(setting[0], setting[1], email)
        print("result: " + str(result))
        end_gen_time = datetime.now()
        gen_time = end_gen_time - start_gen_time
        print("Finished in " + str(round(gen_time.total_seconds(), 2)) + " seconds.")













