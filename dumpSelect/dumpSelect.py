#import lib
from selenium import  webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

#init log file
logFile = open('./en_nabu_product_list_dump.txt', 'w')

def printf(str):
    logFile.write(str)
    logFile.write("\n")
    print str

#Brower setup
chromeDriverPath = './webdriver/chromedriver_2.14.exe'
driver = webdriver.Chrome(executable_path=chromeDriverPath)
driver.implicitly_wait(30)
driver.maximize_window()

#Test case here
nabuSRF_URL = 'https://stgesupport.trendmicro.com/srf/srfnabu.aspx?locale=en'
driver.get(nabuSRF_URL)
driver.find_element_by_css_selector("option.productIssue").click()
driver.find_element_by_id("textareaDescription").clear()
driver.find_element_by_id("textareaDescription").send_keys("test")
driver.find_element_by_id("btnGoToStep2").click()


#get product control
selProduct = Select(driver.find_element_by_id("selectProductName"))
products = selProduct.options

for p in products:
    if not p.get_attribute("value"):
        continue

    selProduct.select_by_value(p.get_attribute("value"))
    printf(p.get_attribute("value"))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "selectProductVersion")))

    selVer = Select(driver.find_element_by_id("selectProductVersion"))
    pv = selVer.options

    for v in pv:
        if not v.get_attribute("value"):
            continue

        selVer.select_by_value(v.get_attribute("value"))
        printf('  '+v.get_attribute("text"))

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "selectOperatingSystem")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "selectProductLanguage")))

        selOS = Select(driver.find_element_by_id("selectProductLanguage"))
        selLanguage = Select(driver.find_element_by_id("selectOperatingSystem"))

        pos = selOS.options
        pln = selLanguage.options

        for os in pos:
            printf('    '+os.get_attribute("text"))

        for ln in pln:
            printf('    '+ln.get_attribute("text"))

#Close
logFile.close()
driver.quit()