import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def job():
    # Set the full path for the download directory
    download_directory = os.path.join(os.getcwd(), 'gprkhaptrafriday')

    options = webdriver.ChromeOptions()
    prefs = {
        'download.default_directory': download_directory,
        'plugins.always_open_pdf_externally': True
    }
    options.add_experimental_option('prefs', prefs)
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get("https://epaper.gorkhapatraonline.com/single/friday-suppliment")

    try:
        # Wait for the PDF links to be present
        pdf_links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '.pdf')]")))

        for pdf_link in pdf_links:
            try:
                # Open the link in a new tab
                ActionChains(driver).key_down(Keys.CONTROL).click(pdf_link).key_up(Keys.CONTROL).perform()

                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])

                # Wait for the download button to be visible
                download_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@id='download' and @title='Save']")))

                # Use pyautogui to click on the download button
                ActionChains(driver).move_to_element(download_button).click().perform()

                # Allow some time for the download to complete
                time.sleep(15)

            except (TimeoutException, NoSuchElementException) as e:
                print(f"Error processing PDF link: {e}")

            finally:
                # Close the current tab
                driver.close()

                # Switch back to the main tab
                driver.switch_to.window(driver.window_handles[0])

    finally:
        driver.quit()

# Execute the function directly
job()