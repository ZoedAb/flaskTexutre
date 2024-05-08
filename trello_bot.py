from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

import time
from datetime import date
import os
import json
import zipfile
import glob
import base64
import shutil
CHROME_DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
EDGE_DRIVER_PATH = os.path.join(os.getcwd(), "msedgedriver.exe")
DOWNLOAD_PATH = os.path.join(os.getcwd(), "Download")
OP = webdriver.ChromeOptions()
# OP = webdriver.EdgeOptions()
OP.add_experimental_option("prefs", {
  "download.default_directory": DOWNLOAD_PATH,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
OP.add_argument('--headless=new')
DRIVER = None
# OP = webdriver.EdgeOptions()
# DRIVER = webdriver.Edge(options=OP)
# service = webdriver.ChromeService(executable_path=CHROME_DRIVER_PATH)


#OP = webdriver.EdgeOptions()

#service = webdriver.EdgeService(executable_path = EDGE_DRIVER_PATH)

#OP.add_extension(CHROME_DRIVER_PATH)
#OP.add_argument('--headless')






def screenshotPage():
    time.sleep(2)
    date_str = date.today().strftime("%m-%d-%Y")
    fpath = os.path.join(os.getcwd(), 'downloads\{}.png'.format(date_str))
    print(fpath)
    DRIVER.get_screenshot_as_file(fpath)


def addTask(task):
    time.sleep(2)
    DRIVER.find_element(
        By.XPATH, value="//textarea[@aria-label='À faire']/ancestor::div[@data-testid='list']/descendant::div[@data-testid='list-footer']/child::button").click()
    task_text_area = DRIVER.find_element(
        By.XPATH, value="//ol[@data-testid='list-cards']/descendant::textarea")
    task_text_area.clear()
    task_text_area.send_keys(task)
    DRIVER.find_element(By.XPATH, value="//button[@type='submit']").click()
    time.sleep(5)


def login():
    with open('config.json') as configFile:
        credentials = json.load(configFile)
        time.sleep(3)
        #DRIVER.find_element(By.XPATH, value="//a[@href='/https://id.atlassian.com/login?application=trello&continue=https%3A%2F%2Ftrello.com%2Fauth%2Fatlassian%2Fcallback%3Fdisplay%3DeyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%253D%253D&display=eyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%3D%3D']").click()
        DRIVER.find_element(By.CSS_SELECTOR, value="button[class='styles_authLink__UkM93 styles_elevated__qKQOV css-kxamqc']").click()
        
        time.sleep(2)
        DRIVER.find_element(By.CSS_SELECTOR, value="button[class='styles_secondaryClear__32mUA styles_l__vHx1i styles_rect__lTWI7']").click()
        time.sleep(4)
        wait = WebDriverWait(DRIVER, 60)  # wait up to 10 seconds
        username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))
        username = DRIVER.find_element(
            By.CSS_SELECTOR, value="input[type='email']")
        username.clear()
        username.send_keys(credentials["USERNAME"])
        
        #DRIVER.find_element(By.CSS_SELECTOR,value="button[type='submit']").click()
        time.sleep(1)
        password = DRIVER.find_element(
            By.CSS_SELECTOR, value="input[type='password']")
        #username.clear()
        password.clear()
        password.send_keys(credentials["PASSWORD"])
        time.sleep(2)
        DRIVER.find_element( By.CSS_SELECTOR,value="button[class='css-y0q9se']").click()
        
        #DRIVER.find_element_by_css_selector("input[type='submit']").click()
        
        # password = DRIVER.find_element(
        #     By.CSS_SELECTOR, value="input[name='password']")
        # password.clear()
        # password.send_keys(credentials["PASSWORD"])
        # time.sleep(5)
        # DRIVER.find_element_by_css_selector("button[type='submit']").click()


def navigateToBoard(task):
    time.sleep(5)
    text = DRIVER.find_element(
            By.CSS_SELECTOR, value="textarea[class='styles_promptInput__8HpWq']")
    text.clear()
    text.send_keys(task)
    time.sleep(2)
    DRIVER.find_element( By.CSS_SELECTOR,value="button[class='styles_actionBtn__QIunN styles_generateBtn__ThjPL']").click()
    wait = WebDriverWait(DRIVER, 60)  # wait up to 10 seconds
    buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'output button[title="Download"]')))
    
    time.sleep(3)
    #buttons = DRIVER.find_elements(By.CSS_SELECTOR, 'output button[title="Select"]')
        # Wait for all three buttons to be present
    start_time = time.time()
    timeout = 60  # Timeout in seconds
    while time.time() - start_time < timeout:
        buttons = DRIVER.find_elements(By.CSS_SELECTOR, 'output button[title="Select"]')
        if len(buttons) >= 4:
            break
        time.sleep(1)
    print(f"Buttons found {len(buttons)} .")
    for i in range(0, len(buttons)):
        try:
            buttons[i].click()
        except ElementClickInterceptedException:
            print(f"Button {i} is not clickable.")    
        time.sleep(3)  # Wait for the download button to appear
        download_buttons = DRIVER.find_elements(By.CSS_SELECTOR, 'output button[title="Download"]')
        if download_buttons:
            download_buttons[0].click()  # Assuming there is only one download button per select button
            time.sleep(5)  # Assuming some time is needed for the download to complete
            print(f"Button download {i} is clicked.")   
    #buttons[0].click()
    #time.sleep(8)
# button = DRIVER.find_element(By.XPATH, '//output//button[@title="Select"][1]')
    # button = DRIVER.find_element(By.CSS_SELECTOR, 'output button[title="Select"]:nth-of-type(2)')
    # button.click()

def unzip_file(zip_filepath, dest_dir):
    time.sleep(5)
   
    start_time = time.time()
    timeout = 60  # Timeout in seconds
    while time.time() - start_time < timeout:
        zip_files = glob.glob(os.path.join(DOWNLOAD_PATH, '*.zip'))
        if len(zip_files) >= 4:
            break
        time.sleep(1)
    print(f"zip_files found {len(zip_files)} .")
    if zip_files:
        for zip_filepath in zip_files:
            with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                zip_ref.extractall(dest_dir)
            print(f'Successfully unzipped {zip_filepath} to {dest_dir}')
    else:
        print('No zip files found in the specified directory.')

    # with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
    #     zip_ref.extractall(dest_dir)
def sendImage():
    time.sleep(5)
    image_path = os.path.join(DOWNLOAD_PATH, "albedo.png")
    base64_image = ""
    # Read the image in binary mode, encode it to base64, and decode it to string
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        #print(base64_image)
    with open('textfile.txt', 'w') as text_file:
        text_file.write(base64_image)
    deleteFolder()
    return base64_image

def sendAllImages():
    #time.sleep(5)
    image_files = [f for f in os.listdir(DOWNLOAD_PATH) if f.endswith('.png')]
    images_list = []
    images_json = {}
    for image_file in image_files:
        image_path = os.path.join(DOWNLOAD_PATH, image_file)
        with open(image_path, 'rb') as file:
            base64_image = base64.b64encode(file.read()).decode('utf-8')
            filename = os.path.splitext(image_file)[0]
            #images_list.append({filename: base64_image})
            images_json[str(filename)] = base64_image

    return images_json
def extractAndSendImages():
    time.sleep(5)
    #zip_files = glob.glob(os.path.join(DOWNLOAD_PATH, '*.zip'))
    start_time = time.time()
    timeout = 60  # Timeout in seconds
    while time.time() - start_time < timeout:
        zip_files = glob.glob(os.path.join(DOWNLOAD_PATH, '*.zip'))
        if len(zip_files) >= 4:
            break
        time.sleep(1)
    images_json = {}
    i = 0
    for zip_filepath in zip_files:
        dest_dir = DOWNLOAD_PATH  # specify the destination directory
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
        print(f'Successfully unzipped {zip_filepath} to {dest_dir}')

        images_list = sendAllImages()
        images_json['image'+str(i)] = images_list
        i= i +1

    return images_json
def deleteFolder():
    if os.path.exists(DOWNLOAD_PATH):
        shutil.rmtree(DOWNLOAD_PATH)
def main(task):
    global DRIVER
    try:
        
        #if not DRIVER:
        DRIVER = webdriver.Chrome(options=OP)
        #DRIVER = webdriver.Edge(options=OP)
        DRIVER.set_window_size(1600, 1200)
        DRIVER.get("https://poly.cam/tools/ai-texture-generator")
        deleteFolder()
        #screenshotPage()
        login()
        # #
        navigateToBoard(task)
        #unzip_file(DOWNLOAD_PATH,DOWNLOAD_PATH)
        DRIVER.close()
        return extractAndSendImages()
        #addTask(task)
        #screenshotPage()
        input("Bot Operation Completed. Press any key...")
        
    except Exception as e:
        print(e)
        DRIVER.close()


if __name__ == "__main__":
    print(CHROME_DRIVER_PATH)
    #user = input("Enter Task:")
    #main(user)
    #unzip_file(DOWNLOAD_PATH,DOWNLOAD_PATH)
    
