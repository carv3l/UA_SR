from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import sys
import datetime
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By

var_domain = 'practicetestautomation.com/practice-test-login/'

hours_to_apply_reboot = ['7:0:0','13:20:0','20:2:0']

hours_to_apply_reset = ['3:0:0','4:0:0','5:0:0','6:0:0']


user_cred = b'gAAAAABlT2Uawt0mZa25IpkQ24Hzct3ShShtEn7phpKi5k7DoWb_JO0xgutfjlr1Kqcn1TAaeAsfJ4DtDiI4I7wHfBaFARzBGw=='

pwd_cred = b'gAAAAABlT2UaEGSIc9jmXHHSu9emVXjgdmgFQU-_Xa-Kzo8BqgJnUDIuyLT_CpiAWFhVwTIVQPcJNf2yjffryzS6XWcjFpqRkQ=='

delay_time = 3600

previous_timestamp = ""


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def help_menu():
    print("Available Arguments:\n")
    print("(n) now  - Performs the execution of the script now\n")
    print("(a) auto - Performs the execution of the script in the specified times")


def report(action: str,current_time: datetime, data: str):
    print("Writing Log ...")
    f = open("logs/reboopy.log", "a")
    if action == "enter":
        f.write("Entered in: " + str(current_time) + " - For more information on the process, see Geckodriver.log on parent folder \n")
    if action == "copy":
        f.write("Copy Performed in: " + str(current_time) + " - For more information on the copying process, see Geckodriver.log on parent folder \n")
        f.write(f"Content of Copy: {data} \n")
    f.close()


def perform_action(action):
    
    print (f"{bcolors.WARNING}Starting to perform action: {bcolors.ENDC}")
    driver = webdriver.Firefox()
    driver.get('https://'+var_domain)
    driver.implicitly_wait(delay_time)
    username = driver.find_element(By.XPATH, "//input[contains(@id, 'username') and @name='username']")
    driver.implicitly_wait(delay_time)
    username.send_keys(user_cred)
    driver.implicitly_wait(delay_time)
    password = driver.find_element(By.XPATH, "//input[contains(@id, 'password') and @name='password']")
    driver.implicitly_wait(delay_time)
    password.send_keys(pwd_cred)
    driver.implicitly_wait(delay_time)
    driver.implicitly_wait(delay_time)

    print (f"{bcolors.FAIL}ENTERING CREDENTIALS.. {bcolors.ENDC}")
    
    # Click Action of the Submit Button on the page
    
    SUBMIT_BUTTON_XPATH = '//button[contains(@id, "submit") and @class="btn"]'
    
    button = driver.find_element("xpath",SUBMIT_BUTTON_XPATH)
    button.click()

    
    LOGOUT_BUTTON_XPATH = '//a[contains(@class, "wp-block-button__link") and text() ="Log out"]'
    
    LIST_HTML_TAGS = ["h1", "h2", "h3", "h4", "h5", "strong", "span"]

    if(action == "logout"):
        current_date = datetime.datetime.now()

        driver.implicitly_wait(delay_time)

        print (f"{bcolors.FAIL}Logging Out.. {bcolors.ENDC}")

        button = driver.find_element("xpath",LOGOUT_BUTTON_XPATH)
        button.click()
        
        
        # Writing log
        report(action,current_date, "")



    if( action == "copy"):
        
        current_date = datetime.datetime.now()
        print (f"{bcolors.FAIL}Copying data to DUMP.... {bcolors.ENDC}")

        for tag in LIST_HTML_TAGS:
            
            data = driver.find_element("xpath",f"//{tag}").get_attribute("innerHTML")
            
            if len(data) < 0:
                break
            else:
                report(action,current_date,data)
                   

    driver.implicitly_wait(delay_time)
    #Close browser
    driver.quit()

    print(f"{bcolors.OKGREEN} Finished performing {action}.... {bcolors.ENDC}")
    
    
key = sys.argv[2]
fernet = Fernet(key)
user_cred = fernet.decrypt(user_cred).decode()
pwd_cred = fernet.decrypt(pwd_cred).decode()
    
try:
    execution_type = sys.argv[1]

    if execution_type == "n" or execution_type == "now":
        perform_action("copy")
        perform_action("logout")
    elif execution_type == "a" or execution_type == "auto":

        while True:

            HOUR        = datetime.datetime.now().hour   # the current hour
            MINUTE      = datetime.datetime.now().minute # the current minute
            SECONDS     = datetime.datetime.now().second #the current second
            MILISECONDS     = datetime.datetime.now().microsecond #the current second

        # print(HOUR, MINUTE, SECONDS)

            current_timestamp = str(HOUR) + ':' + str(MINUTE) + ':'+ str(SECONDS)
            
            if current_timestamp != previous_timestamp:

                if (MINUTE in [0,15,25,30,45,55]) and (SECONDS in [0]):
                    print(current_timestamp)

                if current_timestamp in hours_to_apply_reboot:
                    print("Entering time")
                    perform_action("enter")

                if current_timestamp in hours_to_apply_reset:
                    print("Copying time")
                    perform_action("copy")
            
            previous_timestamp = current_timestamp
except IndexError:
    help_menu()
