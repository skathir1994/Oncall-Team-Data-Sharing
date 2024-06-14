import os
import pandas as pd
import win32com.client as win32
from selenium import webdriver
import time
from time import sleep
from selenium.webdriver.common.by import By


#################################
#fetching midway cookie
def get_mwinit_cookie():
    MidwayConfigDir = os.path.join(os.path.expanduser("~"), ".midway")
    MidwayCookieJarFile = os.path.join(MidwayConfigDir, "cookie")
    fields = []
    keyfile = open(MidwayCookieJarFile, "r")
    for line in keyfile:
        # parse the record into fields (separated by whitespace)
        fields = line.split()
        if len(fields) != 0:
            # get the yubi session token and expire time
            if fields[0] == "#HttpOnly_midway-auth.amazon.com":
                session_token = fields[6].replace("\n", "")
                expires = fields[4]
            # get the user who generated the session token
            elif fields[0] == "midway-auth.amazon.com":
                username = fields[6].replace("\n", "")
    keyfile.close()
    # make sure the session token hasn't expired
    if time.gmtime() > time.gmtime(int(expires)):
        raise SystemError("Your Midway token has expired. Run mwinit to renew")
    # construct the cookie value required by calls to k2
    cookie = {"username": username, "session": session_token}
    return cookie


# Create the webdriver object. Here the
# chromedriver is present in the driver
# folder of the root directory.
# driver = webdriver.Chrome(r".D:\Users\skathir\Desktop\Python code for oncall daily data\chromedriver_win\chromedriver")
driver = webdriver.Chrome()

# options = webdriver.ChromeOptions()
# options.add_experimental_option('w3c', False)
# driver = webdriver.Chrome(r'./chromedriver.exe', options=options)
midway_url = 'https://midway-auth.amazon.com'
cookie = get_mwinit_cookie()
driver.get(midway_url)
cookie_dict1 = {'domain': '.midway-auth.amazon.com',
                'name': 'user_name',
                'value': cookie['username'],
                'path': '/',
                'httpOnly': False,
                'secure': True}

cookie_dict2 = {
    'domain': '.midway-auth.amazon.com',
    'name': 'session',
    'value': cookie['session'],
    'path': '/',
    'httpOnly': True,
    'secure': True}

driver.add_cookie(cookie_dict1)
driver.add_cookie(cookie_dict2)

match = False
while not match:
    driver.get(midway_url)
    if driver.current_url == 'https://midway-auth.amazon.com/':
        match = True
    sleep(1)
    driver.refresh()
driver.maximize_window()

##################################

driver.get("https://issues.amazon.com/")
time.sleep(55)
# Maximize the window and let code stall
# for 10s to properly maximise the window.
# driver.maximize_window()
# time.sleep(10)

# Obtain button by link text and click.
button = driver.find_elements(By.XPATH, '//*[@id="view-content-left"]/div[1]/div[1]/div[1]/div/button[1]')
button[0].click()
time.sleep(1)

button = driver.find_elements(By.XPATH, '//*[@id="view-content-left"]/div[1]/div[1]/div[1]/div/ul/li[1]/a')
button[0].click()
time.sleep(1)

button = driver.find_elements(By.XPATH, '//*[@id="submit-custom-export-job"]')
button[0].click()
time.sleep(190)

button = driver.find_elements(By.XPATH, '//*[@id="job-details"]/div/section/div/div/table/tbody/tr/td[1]/a')
button[0].click()
time.sleep(2)
button = driver.find_elements(By.XPATH, '//*[@id="job-details"]/div/section/div/div/table/tbody/tr/td[1]/a')
time.sleep(3)

mydata = pd.read_csv(r"D:\Users\skathir\Downloads\documentSearch_skathir.csv")
print(mydata['Description'])
mydata[['Description','Description1']] = mydata['Description'].str.split('and lister All',expand=True)
print(mydata['Description'])
# mydata.to_csv('oncal_data.csv')


# construct Outlook application instance
olApp = win32.Dispatch('Outlook.Application')
olNS = olApp.GetNameSpace('MAPI')

# construct the email item object
mailItem = olApp.CreateItem(0)
mailItem.Subject = 'Automatic mail for Oncall team ticket data attachment.'
mailItem.BodyFormat = 1
mailItem.Body = '''Hi Team,

Attached  Oncall ticket Data which is having ASIN, MKPL, MerchantID. PFA.

Regards,
KATHIRESAN S

NOTE :
*** This is an automatically generated email. DO NOT Reply to this mail ***
*** Please contact skathir for queries and issues related to these automated reports ***
'''
mailItem.To = 'pricerejects-team@amazon.com'
# mailItem.To = 'skathir@amazon.com'
mailItem.CC = 'pr-managers@amazon.com'

mailItem.Attachments.Add(os.path.join(os.getcwd(), 'oncal_data.csv'))
mailItem.Display()

mailItem.Save()
mailItem.Send()

# File deleting
myfile = (r"D:\\Users\\skathir\\Downloads\documentSearch_skathir.csv")
if os.path.isfile(myfile):
    os.remove(myfile)
    print('Successfully deleted')
else:
    # If it fails, inform the user.
    print("Error: %s file not found")