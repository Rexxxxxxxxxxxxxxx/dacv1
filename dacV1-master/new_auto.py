import urllib3
import requests
import random
import time
import yaml
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from proxyscrape import create_collector
import threading
from datetime import datetime
import concurrent.futures



with open('config/config.yml', 'r') as config:
    c = yaml.safe_load(config)
    scrape = c['autoscrape']
    check = c['autocheck']
    binary_path = c['location_of_chromium_exe']





def proxycheck(proxy):
    try:
        response = requests.post('https://www.yinsiduanxin.com/', proxies={'socks5': "socks5://" + proxy, }, timeout=(3, 5))
        status_code = response.status_code
        if "200" or "404" == status_code:
            json = "All good."
        elif "429" == status_code:
            json = response.json()
        else:
            json = "Unknown error."
        return status_code, json, proxy
    except requests.exceptions.ProxyError as proxerror:
        if "Max retries exceeded with url:" in str(proxerror):
            return "error", "delete: " + str(proxy) + " failed to connect at all.", proxy
    except requests.exceptions.ConnectTimeout:
        return "error", "delete: " + str(proxy) + " failed to connect due to 5 second timeout.", proxy
    except requests.exceptions.ReadTimeout:
        return "error", "delete: " + str(proxy) + " couldn't read the website due to 10 second timeout.", proxy
    except urllib3.exceptions.MaxRetryError:
        return "error", "delete: " + str(proxy) + " failed to connect due to maximum retries.", proxy
    except requests.exceptions.SSLError:
        return "error", "delete: " + str(proxy) + " failed to connect due to wrong SSL connection version.", proxy
    except urllib3.exceptions.ProxySchemeUnknown:
        return "error", "delete: " + str(proxy) + " has an invalid format.", proxy
    except Exception as e:
        return "error", "delete: " + str(proxy) + "failed for an unknown reason.\nError: " + str(e), proxy



def autoscrape():
    collector = create_collector('my-collector', 'https')
    full_proxies = collector.get_proxies({'anonymous': True})
    print(len(full_proxies))
    with open("config/proxies.txt", "w") as f:
        for proxy in full_proxies:
            f.write(str(proxy[0]) + ":" + str(proxy[1]) + "\n")
    uniqlines = set(open('config/proxies.txt').readlines())
    with open('config/proxies.txt', 'w') as finish:
        finish.writelines(set(uniqlines))
    return




def emails():
    with open("config/emails.txt", "r") as f:
        lines = f.readlines()
        if len(lines) != 0:
            email = random.choice(lines).strip('\n')
        else:
            email = "None."
    with open("config/emails.txt", 'w') as output_file:
        output_file.writelines(line for line in lines if line not in email)
    return email
    # email = str(''.join(random.choice(string.ascii_letters) for x in range(10))) + "@gmail.com"




def ratelimit(proxy):
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
        'date_of_birth': '1998-04-12',
        'email': 'ilovetheworld123@gmail.com',
        'fingerprint': 'null',
        'gift_code_sku_id': 'null',
        'invite': 'null',
        'password': '12349876!@#',
        'username': 'skelly gang united.'
    }



    proxee = {
        "socks5": "socks5://" + proxy,
    }
    try:
        #response = requests.post("https://api.ipify.org/", proxies=proxee)
        response = requests.post('https://discord.com/register', headers=headers, json=json, proxies=proxee, timeout=(5, 10))
        status_code = response.status_code
        print(status_code)
        if "200" == status_code:
            json = "All good."
        elif "429" == status_code:
            json = response.json()
        else:
            json = "Unknown error."
        return status_code, json
    except Exception as e:
        print("Error: " + str(e))
        proxy_cleaner(proxy)
        return "error", "error"




def gettoken(driver):
    headers = driver.execute_script(
        "var iframe = document.createElement('iframe'); " \
        "iframe.onload = function(){ " \
        "var ifrLocalStorage = iframe.contentWindow.localStorage; " \
        "console.log(ifrLocalStorage.getItem('fingerprint'));}; " \
        "iframe.src = 'about:blank'; " \
        "document.body.appendChild(iframe); " \
        "return iframe.contentWindow.localStorage.getItem('token') ")

    headers = headers.splitlines()
    token = str(headers).lstrip("['\"").rstrip("\"']")
    #    for request in driver.requests:
    #        if request.url == "https://discord.com/api/v8/gateway":
    #            token = request.headers['authorization']
    file1 = open("results/verified.txt", "a+")
    file1.write("\n{}".format(token))
    driver.quit()
    return token




def settings():
    months = ['December', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
              'October', 'November']

    selection_month = random.choice(months)
    selection_day = random.randint(1, 28)

    # r2 = requests.get("http://names.drycodes.com/10")
    # fem = r2.json()
    # user = random.choice(fem)
    r2 = requests.get('https://randomuser.me/api/?inc=login')
    try:
        user = r2.json()['results'][0]['login']['username']
    except:
        time.sleep(0.25)
        r2 = requests.get('https://randomuser.me/api/?inc=login')
        user = r2.json()['results'][0]['login']['username']
    # passwd = fem['results'][0]['login']['password']

    r3 = requests.get('https://www.dinopass.com/password/simple')
    passwd = r3.text
    return user, passwd, selection_month, selection_day

proxynum = 0
def get_proxys():
    global proxynum
    proxys = []
    with open("config/proxies.txt", "r") as fd:
        for line in fd.readlines():
            line = line.strip("\n")
            if not line:
                continue
            proxys.append(line)
        if proxynum < len(proxys):
            proxy = proxys[proxynum]
            print("Proxynum: " + str(proxynum) + " Proxy: " + str(proxy))
            proxynum += 1
        elif proxynum >= len(proxys):
            proxynum = 0
            proxy = proxys[0]
            print("Proxynum: " + str(proxynum) + " Proxy: " + str(proxy))
    return proxy, proxys




def browser(user, passwd, selection_month, selection_day, email, proxy):
    # uc.TARGET_VERSION = 78
    options = uc.ChromeOptions()
    ua = UserAgent()
    userAgent = ua.random
    #print(userAgent)
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--proxy-server=socks5://" + str(proxy))
    options.add_argument("--host-resolver-rules=\"MAP * ~NOTFOUND , EXCLUDE myproxy\"")
    print('Proxy: ' + str(proxy))
    options.add_extension("./extensions/buster_chrome.crx")
    options.add_extension("./extensions/xpather.crx")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--enable-features=ReaderMode")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    # Stricter preferences.
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

    prefs1 = {"profile.managed_default_content_settings.images": 1,
              "profile.managed_default_content_settings.popups": 2,
              "profile.default_content_setting_values.notifications": 2,
              "profile.managed_default_content_settings.geolocation": 2,
              "profile.managed_default_content_settings.stylesheets": 2, }

    options.add_experimental_option("prefs", prefs1)

    options.binary_location = binary_path

    driver = uc.Chrome(chrome_options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
    driver.set_page_load_timeout(120)

    try:
        driver.get('https://www.yinsiduanxin.com/mail.html')
        navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
        dom_complete = driver.execute_script("return window.performance.timing.domComplete")
        driver.execute_script("window.open('https://discord.com/register')")
        waittime = int(round(dom_complete - navigation_start)) / 1000
        print("Time to connect & load the Discord page: " + str(waittime))
    except Exception as e:
        print("failed to connect\nException: " + str(e))
        proxy_cleaner(proxy)
        driver.quit()
        return "Did not load page.", "Did not get token."

    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(string(), '随机邮箱')]"))).click()
    except Exception as e:
        print("Proxy error: " + str(e))
        proxy_cleaner(proxy)
        driver.quit()
        return "Did not load page.", "Did not get token."

    wait = WebDriverWait(driver, 30)
    emaill = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(string(), '@mailscode.com')]"))).text

    driver.switch_to.window(driver.window_handles[1])
    sleeptime = int(500) / 1000
    try:
        wait = WebDriverWait(driver, 30)
        enter_searchbar = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        enter_searchbar.send_keys(emaill)
        time.sleep(sleeptime)
        enter_user = driver.find_element_by_name("username")
        enter_user.send_keys(user)
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
        try:
            driver.find_element_by_xpath("//input[@type='checkbox']").click()
        except:
            pass
        driver.find_element_by_xpath("//button[@type='submit']").click()
    except Exception as e:
        print("Value input failed due to unloaded elements. \nError: " + str(e))
        proxy_cleaner(proxy)
        driver.quit()
        return "Did not load page.", "Did not grab token."
    time.sleep(1)
    try:
        # randomly stops working for some reason, this is just a check.
        driver.find_element_by_xpath("//button[@type='submit']").click()
    except:
        pass


    try:
        driver.find_element_by_xpath("//span[contains(string(), 'Password is too weak or common to use')]")
        enter_passwd = driver.find_element_by_name("password")
        passwd = passwd + "321!@#"
        enter_passwd.send_keys("321!@#")
        time.sleep(sleeptime)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        print("Fixed password being too short.")
    except Exception as e:
        print("Password was strong enough.")  # \nError: " + str(e))

    try:
        driver.find_element_by_xpath("//div[contains(string(), 'You are being rate limited.')]").is_displayed()
        result = ratelimit()
        if "429" in str(result[1]):
            print("Ratelimited for " + str(round(result[1]['retry_after'])) + " seconds. Waiting until that is over.")
            time.sleep(int(round(result[1]['retry_after'])))
            driver.find_element_by_xpath("//button[@type='submit']").click()
        print(result[0] + " " + result[1])
    except Exception as e:
        print("Registration was not ratelimited.")  # \nError: " + str(e))

    try:
        wait = WebDriverWait(driver, 30)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='a-']")))
        wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()
        time.sleep(2)
    except Exception as e:
        print("Could not find captcha. \nError: " + str(e))
        proxy_cleaner(proxy)
        driver.quit()
        return "Did not load page.", "Did not grab token."

    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB + " ")
    actions.perform()

    while True:
        try:
            wait = WebDriverWait(driver, 8)
            desired_url = "https://discord.com/channels/@me"
            wait.until(lambda driver: driver.current_url == desired_url)
            break
        except:
            pass
    #            try:
    #                wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//div//iframe[@title='recaptcha challenge']")))
    #            except Exception as e:
    #                print(str(e))
    #            actions = ActionChains(driver)
    #            actions.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + " ")
    #            print("first:")
    #            time.sleep(5)
    #            actions.send_keys(Keys.TAB + Keys.TAB + " ")
    #            print("second")
    #            actions.perform()

    #    try:
    #        wait = WebDriverWait(driver, 30)
    #        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='a-']")))
    #        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='rc-audiochallenge-error-message']")))
    #        print("succeeded.")
    #    except:
    #        print("passed")

    #    wait = WebDriverWait(driver, 600)
    #    desired_url = "https://discord.com/channels/@me"
    #    wait.until(lambda driver: driver.current_url == desired_url)
    #    print("Captcha passed.")

    driver.delete_all_cookies()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    wait = WebDriverWait(driver, 20)
    driver.find_element_by_xpath("//button[contains(string(), '接收邮件')]").click()
    time.sleep(0.5)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//td[contains(string(), 'Discord')]"))).click()
    time.sleep(0.5)
    driver.find_element_by_xpath("//a[contains(string(), 'Verify Email')]").click()
    driver.switch_to.window(driver.window_handles[2])
    try:
        wait = WebDriverWait(driver, 3)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='a-']")))
        wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()
        time.sleep(2)
        driver.switch_to.default_content
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB + " ")
        actions.perform()
    except:
        pass

    try:
        wait = WebDriverWait(driver, 60)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button']")))
        print("Second captcha solved.")
    except:
        print("Could not find the button.")
    time.sleep(0.5)
    #    driver.switch_to.window(driver.window_handles[2])
    #    try:
    #        driver.find_element_by_xpath("//h2[contains(string(), 'Add Friend')]")
    #        print("Token works fine.")
    #    except Exception as e:
    #        print("We have been either email or phone-locked.\n" + str(e))
    file1 = open("results/verifiedaccs.txt", "a+")
    file1.write("\n\nUsername: {}".format(user))
    file1.write("\nEmail: {}".format(emaill))
    file1.write("\nPassword: {}".format(passwd))
    token = gettoken(driver)
    print("Result: " + str(token))
    file1.write("\nToken: {}".format(token))
    #if int(waittime) < 5:
    #    with open("config/fastwork.txt", "a+") as file2:
    #        if str(proxy).strip("\n") not in file2.readlines():
    #            file2.write("{}\n".format(proxy))
    #elif int(waittime) < 10:
    #    with open("config/medwork.txt", "a+") as file3:
    #        if str(proxy).strip("\n") not in file3.readlines():
    #            file3.write("{}\n".format(proxy))

    return emaill, token


def workers2():
    MAX_WORKERS = 1
    threads = []
    for i in range(MAX_WORKERS):
        new_Thread = threading.Thread(target=main)
        threads.append(new_Thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def workers():
    MAX_WORKERS = 5
    threads = []
    for i in range(MAX_WORKERS):
        setting = settings()
        proxy = get_proxys()
        email = emails()
        new_thread = threading.Thread(target=browser,
                                      args=(setting[0], setting[1], setting[2], setting[3], email, proxy,),
                                      daemon=True).start()
        threads.append(new_thread)

def read_file():
  proxies = []
  with open("config/proxies.txt", "r") as fd:
      for line in fd:
          line = line.strip("\n")
          if not line:
              continue
          proxies.append(line)
  return proxies


def purger(delete_proxylist):
  with open("text.txt", "w") as f:
    for line in f:
      if line.strip("\n") not in delete_proxylist:
        f.write(line)


def main():
    start_gen_time = datetime.now()
    proxy = get_proxys()
    timee = ratelimit(proxy[0])
    if "429" in str(timee[0]):
        print("Please wait " + str(round(timee[1]['retry_after'])) + " seconds.")
        time.sleep(int(round(timee[1]['retry_after'])))
    elif "200" in str(timee[0]):
        print("No ratelimit detected.")
    else:
        print("Status code: " + str(timee[0]))
        return
    setting = settings()
    email = emails()
    browser(setting[0], setting[1], setting[2], setting[3], email, proxy[0])
    end_gen_time = datetime.now()
    gen_time = end_gen_time - start_gen_time
    print("Finished in " + str(round(gen_time.total_seconds(), 2)) + " seconds.")


def proxy_cleaner(del_proxylist):
    print("Deleting " + str(del_proxylist))
    with open("config/proxies.txt", "r") as f:
        lines = f.readlines()
    with open("config/proxies.txt", "w") as output:
        for line in lines:
            proxy = line.strip("\n")
            if not proxy:
                continue
            if proxy not in del_proxylist:
                output.write(line)


def checkers():
    start_time = datetime.now()
    proxys = get_proxys()[1]
    threads = []
    delete_proxylist = []
    for proxy in proxys:
        if proxy == "\n":
            continue
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(proxycheck, proxy) for proxy in proxys]
        for f in futures:
            print(f.result())
            if "delete" in f.result()[1]:
                delete_proxylist.append(f.result()[2])
        print(delete_proxylist)
    end_time = datetime.now()
    total = end_time - start_time
    print(str(round(total.total_seconds(), 2)))
    return delete_proxylist

# workers()
# time.sleep(600)

if __name__ == "__main__":
    if scrape:
        autoscrape()
    if check:
        list = checkers()
        proxy_cleaner(list)
    while True:
        workers2()
