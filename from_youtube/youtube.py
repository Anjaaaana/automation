import schedule
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 

def job():
     #to save downloaded pdf to running directory
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': os.getcwd(), 'plugins.always_open_pdf_externally': True}
    chrome_options.add_experimental_option('prefs', prefs)
    #chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=chrome_options)

    #download pdf from himalayantimes
    driver.get("https://thehimalayantimes.com/")
    driver.maximize_window()
    time.sleep(5)
    folder= driver.find_element(By.XPATH,"//div[@class='extraLink HideMobile']//a[text()='E-Paper']").click()
    driver.switch_to.window(driver.window_handles[1])
    driver.implicitly_wait(50)
    time.sleep(5)
    Continue=driver.find_element(By.XPATH,"//p[text()='Continue']").click()
    time.sleep(5)
    download=driver.find_element(By.XPATH,"//div[@class='x-container toolbarIcon toolbarIconRight x-sized'][5]/div[@class='x-inner'][1]").click()
    #download=driver.find_element(By.XPATH,"//div[@id='ext-container-195']/..").click()
    #pg.leftClick(1138,172,1,1)
    driver.implicitly_wait(50)
    selectAll=driver.find_element(By.XPATH,"//div[text()='Select All']").click()
    driver.implicitly_wait(50)
    downloadd=driver.find_element(By.XPATH,"//div[text()='Download']").click()
    driver.implicitly_wait(50)
    ok=driver.find_element(By.XPATH,"//div[@style='text-align:center;']//input").click()
    driver.implicitly_wait(50)
    driver.switch_to.window(driver.window_handles[2])
    pdf=driver.find_element(By.TAG_NAME,'a').click()
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(10)
    driver.quit()

    
    time.sleep(5)
    
    #to automate download pdf from gorkhapatra

    driver1 = webdriver.Chrome(chrome_options=chrome_options)        
    driver1.get("https://epaper.gorkhapatraonline.com/")
    driver1.implicitly_wait(60)
    driver1.maximize_window()
    time.sleep(5)
    folder= driver1.find_element(By.XPATH,"//a//img[@alt='rising-nepal']").click()
    driver.switch_to.window(driver.window_handles[1])
    driver1.implicitly_wait(30)
    a=driver1.find_element(By.XPATH,"//div[@class='paperdesign'][1]").click()
    driver.switch_to.window(driver.window_handles[2])
    driver1.switch_to.window(driver1.window_handles[1])
    driver1.implicitly_wait(30)   
    d=driver1.find_element(By.XPATH,"//button[@id='download' and @title='Download']").click()
    driver1.implicitly_wait(50)
    time.sleep(15)
    driver1.quit()
    
    #delete the downloaded pdf from current directory

def delete_pdf_file():
        
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver2 = webdriver.Chrome(options=chrome_options)

            
    pdf_file_extension=".pdf"
    cwd=os.getcwd()
    pdf_files=[f for f in os.listdir(cwd) if f.endswith(pdf_file_extension)]
    if pdf_files:
            # Delete all PDF files that were created 
        for pdf_file in pdf_files:
            file_path = os.path.join(cwd, pdf_file)
            os.remove(file_path)
            print("PDF file deleted: ", file_path)
        else:
            print("No PDF files found in the current working directory.")
        
    driver2.quit()


# run above code on certain time
schedule.every().day.at("08:21").do(job)

#schedule time to delete the downloaded pdf
schedule.every().day.at("23:00").do(delete_pdf_file)

while True:
    schedule.run_pending()
    time.sleep(1)

