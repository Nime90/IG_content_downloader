def coach_urls_finder(coach_profile_url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import time

    urls = []
    #initiate webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Optional: run in headless mode

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(coach_profile_url)
    driver.implicitly_wait(10)
    time.sleep(3)
    elem = driver.find_elements(By.CSS_SELECTOR, 'a')
    for e in elem:
        if '/p/' in str(e.get_attribute('href')) or '/reel/' in str(e.get_attribute('href')) :
            urls.append(str(e.get_attribute('href')))

    driver.quit()
    
    return urls

def coach_urls_finder_gc(coach_profile_url):
    import google_colab_selenium as gs
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import time

    urls = []
    #initiate webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--window-size=1920,1080")  # Set the window size
    chrome_options.add_argument("--disable-infobars")  # Disable the infobars
    chrome_options.add_argument("--disable-popup-blocking")  # Disable pop-ups
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
    chrome_options.add_argument("--incognito")  # Use Chrome in incognito mode
    driver = gs.Chrome(options=chrome_options)
    driver.get(coach_profile_url)
    driver.implicitly_wait(10)
    time.sleep(5)

    elem = driver.find_elements(By.CSS_SELECTOR, 'a')
    for e in elem:
        if '/p/' in str(e.get_attribute('href')) or '/reel/' in str(e.get_attribute('href')) :
            urls.append(str(e.get_attribute('href')))

    driver.quit()
    
    return urls