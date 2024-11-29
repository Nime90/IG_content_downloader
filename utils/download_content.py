def download_content_gc(video_url):
    import google_colab_selenium as gs
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import time, os,requests
    from bs4 import BeautifulSoup
    #create results folder if does not exists
    res_folder='/content/results'
    #if os.path.exists(res_folder): shutil.rmtree(res_folder)
    os.makedirs(res_folder, exist_ok=True)

    #video_url= 'https://www.instagram.com/p/DChnh9yxQ0q/?hl=en&img_index=1'#'https://www.instagram.com/p/DC11wzFsGul/?hl=en'
    #initiate webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--window-size=1920,1080")  # Set the window size
    chrome_options.add_argument("--disable-infobars")  # Disable the infobars
    chrome_options.add_argument("--disable-popup-blocking")  # Disable pop-ups
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
    chrome_options.add_argument("--incognito")  # Use Chrome in incognito mode
    chrome_options.add_argument(f'--download-dir={res_folder}')  

    driver = gs.Chrome(options=chrome_options)
    driver.get('https://fastdl.app/en')
    driver.implicitly_wait(10) 

    while True:
        try:
            input_element=driver.find_element(By.CSS_SELECTOR,'input')
            driver.implicitly_wait(10)
            input_element.click()

            driver.implicitly_wait(10) 
            input_element.send_keys(video_url)
            driver.implicitly_wait(10) 
            button = driver.find_element(By.CSS_SELECTOR, 'button.search-form__button[type="submit"]')
            button.click()
            driver.implicitly_wait(10)
            time.sleep(3)
            break
        except:
            time.sleep(0.5)
            pass

    while True:
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, "a.button.button--filled.button__download")
            button_list=[]
            for button in buttons:
                driver.implicitly_wait(5) 
                button_list.append(button.get_attribute('href'))
            for i,url in enumerate(button_list):
                if '.mp4' in url: extension='.mp4'
                else: extension='.jpg'
                r = requests.get(url)
                results_directory=res_folder+'/'+video_url.split('/')[-2]+'_'+str(i)+extension
                with open(results_directory, 'wb') as f:
                    f.write(r.content)
            Last_created_file=str(video_url.split('/')[-2]+'_'+str(i)+extension)
            if Last_created_file in [f for f in os.listdir('results') if os.path.isfile(os.path.join('results', f))]:
                break
        except:
            time.sleep(0.5)
            pass

    #capturing additional_info
    while True:
        try:
            additional_info=driver.find_elements(By.CLASS_NAME, "output-list__info")
            additional_info_list = additional_info[0].text.split('\n')
            if len(additional_info_list)>0:
                break
        except:
            time.sleep(0.5)
            pass
    #get caption
    caption = BeautifulSoup(requests.get(video_url).text, 'html.parser').find_all('meta', property="og:description")[0]['content']

    driver.quit()
    files = [f for f in os.listdir('results') if os.path.isfile(os.path.join('results', f))]
    
    return files, caption, additional_info_list


def download_content(video_url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import time, os,requests
    from bs4 import BeautifulSoup


    #create results folder if does not exists
    res_folder=os.getcwd()+'/results'
    os.makedirs(res_folder, exist_ok=True)
    #initiate webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Optional: run in headless mode
    prefs = {"download.default_directory" : res_folder}
    chrome_options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://fastdl.app/en')
    driver.implicitly_wait(10) 
    
    while True:
        try:
            input_element=driver.find_element(By.CSS_SELECTOR,'input')
            driver.implicitly_wait(10)
            input_element.click()

            driver.implicitly_wait(10) 
            input_element.send_keys(video_url)
            driver.implicitly_wait(10) 
            button = driver.find_element(By.CSS_SELECTOR, 'button.search-form__button[type="submit"]')
            button.click()
            driver.implicitly_wait(10)
            time.sleep(3)
            break
        except:
            time.sleep(0.5)
            pass

    while True:
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, "a.button.button--filled.button__download")
            button_list=[]
            for button in buttons:
                driver.implicitly_wait(5) 
                button_list.append(button.get_attribute('href'))
            for i,url in enumerate(button_list):
                if '.mp4' in url: extension='.mp4'
                else: extension='.jpg'
                r = requests.get(url)
                results_directory=res_folder+'/'+video_url.split('/')[-2]+'_'+str(i)+extension
                with open(results_directory, 'wb') as f:
                    f.write(r.content)
            Last_created_file=str(video_url.split('/')[-2]+'_'+str(i)+extension)
            if Last_created_file in [f for f in os.listdir('results') if os.path.isfile(os.path.join('results', f))]:
                break
        except:
            time.sleep(0.5)
            pass

    #capturing additional_info
    while True:
        try:
            additional_info=driver.find_elements(By.CLASS_NAME, "output-list__info")
            additional_info_list = additional_info[0].text.split('\n')
            if len(additional_info_list)>0:
                break
        except:
            time.sleep(0.5)
            pass
    #get caption
    caption = BeautifulSoup(requests.get(video_url).text, 'html.parser').find_all('meta', property="og:description")[0]['content']

    driver.quit()
    files = [f for f in os.listdir('results') if os.path.isfile(os.path.join('results', f))]
    return files, caption, additional_info_list