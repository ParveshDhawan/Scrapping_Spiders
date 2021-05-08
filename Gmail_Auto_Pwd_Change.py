from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

n = int(input("How Many IDs : "))
if n <= 0:
    print('No ID Inserted')
elif n == 1:
    # Loading Driver
    driver = webdriver.Chrome(r'D:\Scrapper_Scripts\2chromedriver.exe')
    driver.maximize_window() #maximize window
    time.sleep(2)

    driver.get('https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3ABBC%2C16%3A538e5cef37df3662%2C10%3A1596955257%2C16%3A57c01b6ec405542d%2C36c055c3e86eb6a1970a6277228223af4b7669955081ffd1b434e3631cee46f9%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%2280866a4b6c964b7390fb3632f6f4b4c0%22%7D&response_type=code&flowName=GeneralOAuthFlow')
    print('Login to slackoverflow')
    time.sleep(5)

    #email
    Email = input("Enter Email ID:")
    print("Email ID: " + Email)
    email = driver.find_element_by_xpath("//input[@type='email']")
    email.click()
    email.send_keys(Email)
    driver.find_element_by_xpath("//span[contains(text(),'Next')]/parent::button").click()
    time.sleep(5)

    #password
    Old_paswd = input("Enter Old Password:")
    pwd = driver.find_element_by_xpath("//input[@type='password']")
    pwd.click()
    pwd.send_keys(Old_paswd)
    driver.find_element_by_xpath("//span[contains(text(),'Next')]/parent::button").click()
    time.sleep(5)
    driver.get('https://accounts.google.com/signin/v2/challenge/pwd?continue=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Fpassword%3Fcontinue%3Dhttps%3A%2F%2Fmyaccount.google.com%2Fsecurity&service=accountsettings&osid=1&rart=ANgoxcc8aZJ8Eq-U6SWnJ9Vb4Gsh0nnCWbwILR5YRqDm5O5FlbulrfyyQ6AgTlATFz4mZvF3JeMYyEdVDSoJR0w104iZJnQCEQ&TL=AM3QAYaRgTqlekhMbN0kwwi3E5YOWVMWRpQCan3EEwvIywV65crpFV_pOwUc6YAu&flowName=GlifWebSignIn&cid=1&flowEntry=ServiceLogin')

    #password Gmail
    time.sleep(5)
    pwd = driver.find_element_by_xpath("//input[@type='password']")
    pwd.click()
    pwd.send_keys(Old_paswd)
    driver.find_element_by_xpath("//span[contains(text(),'Next')]/parent::button").click()

    #New Password
    time.sleep(5)
    New_paswd = input("Enter New Password:")
    pwd = driver.find_element_by_xpath("//input[@name='password']")
    pwd.click()
    pwd.send_keys(New_paswd)
    pwd = driver.find_element_by_xpath("//input[@name='confirmation_password']")
    pwd.click()
    pwd.send_keys(New_paswd)
    driver.find_element_by_xpath("//div[@class='qNeFe RH9rqf']/div[@role='button']").click()
    time.sleep(4)
    print('Password Changed for Email ID :',Email)
    driver.quit()
    
elif n > 1:
    ids = [str(input()) for i in range(0, n)]
    #Same pass or not
    results = str(input("Does Passwords Same or Different (y):"))
    if results == 'y':
        Old_paswd = input("Enter Old Password:")
        New_paswd = input("Enter New Password:")
        for i in range(0,n):
            # Loading Driver
            driver = webdriver.Chrome(r'D:\Scrapper_Scripts\2chromedriver.exe')
            driver.maximize_window() #maximize window
            time.sleep(2)

            driver.get('https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3ABBC%2C16%3A538e5cef37df3662%2C10%3A1596955257%2C16%3A57c01b6ec405542d%2C36c055c3e86eb6a1970a6277228223af4b7669955081ffd1b434e3631cee46f9%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%2280866a4b6c964b7390fb3632f6f4b4c0%22%7D&response_type=code&flowName=GeneralOAuthFlow')
            time.sleep(5)

            #email
            Email = ids[i]
            print("Email ID: " + Email)
            email = driver.find_element_by_xpath("//input[@type='email']")
            email.click()
            email.send_keys(Email)
            driver.find_element_by_xpath("//span[contains(text(),'Next')]/parent::button").click()
            time.sleep(5)

            #password
            pwd = driver.find_element_by_xpath("//input[@type='password']")
            pwd.click()
            pwd.send_keys(Old_paswd)
            driver.find_element_by_xpath("//span[contains(text(),'Next')]/parent::button").click()
            time.sleep(5)
            driver.get('https://accounts.google.com/signin/v2/challenge/pwd?continue=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Fpassword%3Fcontinue%3Dhttps%3A%2F%2Fmyaccount.google.com%2Fsecurity&service=accountsettings&osid=1&rart=ANgoxcc8aZJ8Eq-U6SWnJ9Vb4Gsh0nnCWbwILR5YRqDm5O5FlbulrfyyQ6AgTlATFz4mZvF3JeMYyEdVDSoJR0w104iZJnQCEQ&TL=AM3QAYaRgTqlekhMbN0kwwi3E5YOWVMWRpQCan3EEwvIywV65crpFV_pOwUc6YAu&flowName=GlifWebSignIn&cid=1&flowEntry=ServiceLogin')

            #password Gmail
            time.sleep(5)
            pwd = driver.find_element_by_xpath("//input[@type='password']")
            pwd.click()
            pwd.send_keys(Old_paswd)
            driver.find_element_by_xpath("//span[contains(text(),'Next')]/parent::button").click()

            #New Password
            time.sleep(5)
            pwd = driver.find_element_by_xpath("//input[@name='password']")
            pwd.click()
            pwd.send_keys(New_paswd)
            pwd = driver.find_element_by_xpath("//input[@name='confirmation_password']")
            pwd.click()
            pwd.send_keys(New_paswd)
            driver.find_element_by_xpath("//div[@class='qNeFe RH9rqf']/div[@role='button']").click()
            time.sleep(4)
            print('Password Changed for Email ID :',Email)
            driver.quit()
    else :
        for i in range(0,n):
            # Loading Driver
            driver = webdriver.Chrome(r'D:\Scrapper_Scripts\chromedriver.exe')
            driver.maximize_window() #maximize window
            time.sleep(2)

            driver.get('https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3ABBC%2C16%3A538e5cef37df3662%2C10%3A1596955257%2C16%3A57c01b6ec405542d%2C36c055c3e86eb6a1970a6277228223af4b7669955081ffd1b434e3631cee46f9%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%2280866a4b6c964b7390fb3632f6f4b4c0%22%7D&response_type=code&flowName=GeneralOAuthFlow')
            time.sleep(5)

            #email
            Email = ids[i]
            print("Email ID: " + Email)
            email = driver.find_element_by_xpath("//input[@type='email']")
            email.click()
            email.send_keys(Email)
            driver.find_element_by_xpath("//span[contains(text(),'Next')]/parent::button").click()
            time.sleep(5)

            #password
            Old_paswd = input("Enter Old Password:")
            pwd = driver.find_element_by_xpath("//input[@type='password']")
            pwd.click()
            pwd.send_keys(Old_paswd)
            driver.find_element_by_xpath("//span[contains(text(),'Next')]/parent::button").click()
            time.sleep(5)
            driver.get('https://accounts.google.com/signin/v2/challenge/pwd?continue=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Fpassword%3Fcontinue%3Dhttps%3A%2F%2Fmyaccount.google.com%2Fsecurity&service=accountsettings&osid=1&rart=ANgoxcc8aZJ8Eq-U6SWnJ9Vb4Gsh0nnCWbwILR5YRqDm5O5FlbulrfyyQ6AgTlATFz4mZvF3JeMYyEdVDSoJR0w104iZJnQCEQ&TL=AM3QAYaRgTqlekhMbN0kwwi3E5YOWVMWRpQCan3EEwvIywV65crpFV_pOwUc6YAu&flowName=GlifWebSignIn&cid=1&flowEntry=ServiceLogin')

            #password Gmail
            time.sleep(5)
            pwd = driver.find_element_by_xpath("//input[@type='password']")
            pwd.click()
            pwd.send_keys(Old_paswd)
            driver.find_element_by_xpath("//span[contains(text(),'Next')]/parent::button").click()

            #New Password
            time.sleep(5)
            New_paswd = input("Enter New Password:")
            pwd = driver.find_element_by_xpath("//input[@name='password']")
            pwd.click()
            pwd.send_keys(New_paswd)
            pwd = driver.find_element_by_xpath("//input[@name='confirmation_password']")
            pwd.click()
            pwd.send_keys(New_paswd)
            driver.find_element_by_xpath("//div[@class='qNeFe RH9rqf']/div[@role='button']").click()
            time.sleep(4)
            print('Password Changed for Email ID :',Email)
            driver.quit()