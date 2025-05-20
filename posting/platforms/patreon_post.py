from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from time import sleep

ERROR_CODES = {
    1:"Internal Error (couldn't load the page). Contact Bruno",
    2:"Invalid email",
    3:"No patreon account for this email exists. (redirect to signup page was detected)",
    4:"Incorrect password for this email.",

}


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    
    # Add these options to avoid detection
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Add these to make it look more like a real browser
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # Execute CDP commands to prevent detection
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    # Remove webdriver flags
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver



def test_patreon_login(email, password):
    try:
        driver = setup_driver()
        #driver = webdriver.Chrome()
        err = 1

        url = "https://www.patreon.com/posts/129421636/edit"
        driver.get(url)
        #print(driver.page_source, file=open("test.html", "w", encoding="utf-8"))

        email_input_div = driver.find_element(By.CLASS_NAME, "sc-13e8657f-9.dLYKLV")
        input_field = email_input_div.find_element(By.TAG_NAME, "input")
        input_field.send_keys(email)
        err += 1

        continue_button = driver.find_element(By.CLASS_NAME, "cm-dMgEsi.cm-LNraKM.cm-bcdZOb.cm-bephWK.cm-lCfmZu.cm-DFAJDB.cm-zbhPFN.cm-ooBxfa.cm-dupTbP.cm-UsNHpA.cm-TOsLDU")
        continue_button.click()
        err += 1
        sleep(1)

        password_div = driver.find_element(By.CLASS_NAME, "sc-bc18523-0.eZlbva")
        password_input = password_div.find_element(By.CLASS_NAME, "sc-13e8657f-2.iMwXpw")
        password_input.send_keys(password)

        continue_button.click()
        err += 1
        sleep(3)

        title_input = driver.find_element(By.CLASS_NAME, "sc-b73158da-0.kYunmr")
    except:
        driver.quit()
        return f"ERROR: {ERROR_CODES[err]}"
    if title_input.accessible_name == "Title":
        return "Logged in successfuly!"
    driver.quit()

