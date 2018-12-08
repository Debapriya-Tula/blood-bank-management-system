
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import socket

#for keeping user logged in
from selenium.webdriver.chrome.options import Options
import os,sys

message_text='Hello World!' # message you want to send
no_of_message=10 # no. of time you want the message to be send
moblie_no_list=[917002888905] # list of phone number can be of any length

def element_presence(by,xpath,time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)

def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except :
        is_connected()


options = Options()
#options.add_argument("user-data-dir="+ os.path.dirname(os.path.abspath('chromedriver')+'/chromedriver'))

options.add_argument("user-data-dir="+os.path.dirname(sys.argv[0]))
#options.add_argument("user-data-dir=C:\\Users\\Username\\AppData\\Local\\Google\\Chrome\\User Data")  For windows

#'/home/debapriya/Pictures/software/chromedriver'
driver = webdriver.Chrome(os.path.dirname(os.path.abspath('chromedriver')+'/chromedriver'),chrome_options = options)
#driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://api.whatsapp.com")
sleep(10) #wait time to scan the code in second

def send_whatsapp_msg(admin_no,user_no,text):
    driver.get("https://api.whatsapp.com/send?phone={}&source={}&text={}".format(user_no,admin_no,text))
    try:
        driver.switch_to_alert().accept()
    except Exception as e:
        print(e)

    try:
        element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]',30)
        txt_box=driver.find_element(By.XPATH , '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        global no_of_message
        for x in range(no_of_message):
            txt_box.send_keys(text)
            txt_box.send_keys("")

    except Exception as e:
        print("invalid phone no :"+str(phone_no))
#for moblie_no in moblie_no_list:

#The admin phone number should be asked in user form
admin_phone_no = '917002888905'

#Should be filled from the view only
user_phone_no = '918374331632'
try:
    send_whatsapp_msg(admin_phone_no,user_phone_no,message_text)

except Exception as e:
    sleep(10)
    is_connected()


driver.quit()
