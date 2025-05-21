from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv
from tempfile import mkdtemp
import os
from time import sleep
import logging



def setup_driver():
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    
    # Add these options to avoid detection
    firefox_options.add_argument('--width=1920')
    firefox_options.add_argument('--height=1080')
    firefox_options.add_argument('--disable-blink-features=AutomationControlled')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--disable-dev-shm-usage')
    
    # Set user agent
    firefox_options.set_preference('general.useragent.override', 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0')
    
    # Additional preferences to make it look more like a real browser
    firefox_options.set_preference('dom.webdriver.enabled', False)
    firefox_options.set_preference('useAutomationExtension', False)
    # Create the driver
    service = Service(GeckoDriverManager().install())
    print("installed")

    driver = webdriver.Firefox(service=service, options=firefox_options)
    
    # Remove webdriver flags
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver



def test_patreon_login(email, password, messages, cookie_reset):
    try:
        if cookie_reset:
            options = Options()
            service = Service(GeckoDriverManager().install(), log_output=open("gecko.log", "w"))
            driver = webdriver.Firefox(service=service, options=options) 
        else:
            driver = setup_driver()
        
        err = "Internal Error (couldn't load the page). Contact Bruno"

        url = "https://www.patreon.com/login"
        driver.get(url)
        #print(driver.page_source, file=open("test.html", "w", encoding="utf-8"))
        if cookie_reset:
            sleep(5)
        email_input_div = driver.find_element(By.CLASS_NAME, "sc-13e8657f-9.dLYKLV")
        input_field = email_input_div.find_element(By.TAG_NAME, "input")
        input_field.send_keys(email)
        err = "Invalid email"

        continue_button = driver.find_element(By.CLASS_NAME, "cm-dMgEsi.cm-LNraKM.cm-bcdZOb.cm-bephWK.cm-lCfmZu.cm-DFAJDB.cm-zbhPFN.cm-ooBxfa.cm-dupTbP.cm-UsNHpA.cm-TOsLDU")
        continue_button.click()
        sleep(1)

        password_div = driver.find_element(By.CLASS_NAME, "sc-bc18523-0.eZlbva")
        password_input = password_div.find_element(By.CLASS_NAME, "sc-13e8657f-2.iMwXpw")
        password_input.send_keys(password)

        continue_button.click()
        err = "Incorrect password for this email. (if you're sure you typed it correctly, contact Bruno)"
        sleep(3)

        member_button = driver.find_element(By.CLASS_NAME, "sc-a5153103-2.kTGxwx")
        member_button.click() 
        err = "Internal Error (couldn't find the creator button). Contact Bruno"
        sleep(1)

        creator_button = driver.find_element(By.CLASS_NAME, "sc-3888ea22-0.bHlqDk.cm-TsFebD")
        creator_button.click()
        sleep(3)

        create_button = driver.find_element(By.CLASS_NAME, "cm-dMgEsi.cm-LNraKM.cm-bcdZOb.cm-bephWK.cm-MLhcyV.cm-DFAJDB.cm-zbhPFN.cm-dupTbP.cm-UsNHpA.cm-TOsLDU")
        create_button.click()
        sleep(3)

        err = "Internal Error (couldn't find title input field). Contact Bruno"
        title_input = driver.find_element(By.CLASS_NAME, "sc-b73158da-0.kYunmr")
    except:
        messages.append(err)
        driver.quit()

    if title_input.accessible_name == "Title":
        messages.append("Logged in successfuly!")
        return driver

if __name__ == "__main__":
    messages = []
    test_patreon_login("bruno@platek.sk", "test_psswd1234", messages, False)
    print(messages[0])