import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from  plugins.ai_run import extract_student_data

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")          
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

url = "https://webprosindia.com/kvsrit/"

def scrap(username, password):
    drv = webdriver.Chrome(options=options)
    drv.get(url)
    try:
            step_1 = drv.find_element(By.NAME, "txtId2")
            step_1.send_keys(username)
            step_2 = drv.find_element(By.NAME, "txtPwd2")
            step_2.send_keys(password, Keys.RETURN)
    except TimeoutException:
            print("ERROR : Finding login page elements.")
    try:
            WebDriverWait(drv, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "capIframe")))
    except TimeoutException:
            print("ERROR : Login failed (or) Iframe not found.")
    time.sleep(3)
    soup = BeautifulSoup(drv.page_source, "html.parser")
    target_1 = soup.find(id="divProfile_BioData")
    target_2 = soup.find(id="divProfile_Present")
    target_3 = soup.find(id="divProfile_Fees")
    content_1 = (target_1.get_text(" ", strip=True) if target_1 else None) 
    content_2 = (target_2.get_text(" ", strip=True) if target_2 else None) 
    content_3 = (target_3.get_text(" ", strip=True) if target_3 else None)

    profile = {
           "Data" : content_1,
           "Attendance" : content_2,
           "Fees": content_3
    }

    result = extract_student_data(profile)
    if result is None:
           print("Result is empty.")
    else:
           return result
    # print(json.dumps(result, indent=2, ensure_ascii=False))