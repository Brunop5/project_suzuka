from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import os
from time import sleep
from selenium.webdriver.common.keys import Keys
import re




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

        password_input = driver.find_elements(By.CLASS_NAME, "sc-13e8657f-2.iMwXpw")[1]
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

        create_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/main/div[1]/div/div/div/div[1]/div[2]/div/div/button")
        create_button.click()

        post_choice = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div/div/div/div/div/ul/li[1]/a")
        post_choice.click()
        sleep(3)
        
        err = "Internal Error (couldn't find title input field). Contact Bruno"
        title_input = driver.find_element(By.CLASS_NAME, "sc-b73158da-0.kYunmr")
    except:
        messages.append(err)
        driver.quit()
        return

    if title_input.accessible_name == "Title":
        messages.append("Logged in successfuly!")
        return driver


def transform_links(text):
    # Pattern to match markdown links [text](url)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    # Replace each markdown link with "link name : url" format
    def replace_link(match):
        link_name = match.group(1)
        url = match.group(2)
        return f"{link_name} : {url}"
    
    # Replace all links in the text
    return re.sub(pattern, replace_link, text)


def patreon_post(title, text, cookie_reset):
    messages = []
    mail, password  = os.getenv("PATREON_MAIL"), os.getenv("PATREON_PSSWD")
    if mail == None or password == None:
        messages.append("Creditentials missing in .env file!")
        return
    try:
        driver = test_patreon_login(mail, password, messages, cookie_reset)
        if driver == None:
            return messages
        sleep(4)
        title_input = driver.find_element(By.CLASS_NAME, "sc-b73158da-0.kYunmr")
        title_input.send_keys(title)

        # Transform the text before sending it
        transformed_text = transform_links(text)
        
        text_input = driver.find_element(By.CLASS_NAME, "ProseMirror.remirror-editor")
        # Split the text by newlines and send each part with a RETURN key
        for line in transformed_text.split('\n'):
            text_input.send_keys(line)
            text_input.send_keys(Keys.RETURN)

        if cookie_reset:
            print("If you see this, you got to the last checkpoint with debug, and the script should be working correctly.\nYou have 50 seconds to check or try anything, then the browser window closes.")
            sleep(50)
            driver.quit()
            return messages
        
        next_button = driver.find_element(By.CLASS_NAME, "cm-dMgEsi.cm-LNraKM.cm-bcdZOb.cm-bephWK.cm-lCfmZu.cm-DFAJDB.cm-zbhPFN.cm-dupTbP.cm-UsNHpA.cm-TOsLDU")
        next_button.click()
        sleep(2)

        publish = driver.find_element(By.CLASS_NAME, "cm-dMgEsi.cm-LNraKM.cm-bcdZOb.cm-bephWK.cm-lCfmZu.cm-DFAJDB.cm-zbhPFN.cm-dupTbP.cm-UsNHpA.cm-TOsLDU")
        publish.click()
        messages.append("Post successfully published!")
        driver.quit()
    except Exception as e:
        messages.append(e)
        driver.quit()

    return messages