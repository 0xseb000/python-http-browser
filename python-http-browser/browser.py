from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

# --headless damit kein firefox fenster geöffnet wird und alles in der Konsole ausgegeben wird
options = FirefoxOptions()
options.add_argument('--headless')

# Da Firefox durchgehend abgebrochen wird, logge ich den ouput
service = FirefoxService(
    log_output=open('error.log', 'w'),
    service_args=['--log', 'trace'],
)

driver = webdriver.Firefox(options=options, service=service)

# user kann URL eingeben und driver holt sie
url = input('Enter URL: ')
driver.get(url)

page_title = driver.title
print("Message: ", page_title)

# für später: definieren welcher tag gesucht werden soll
# tag_name = input('Enter Tag: ')
# header = driver.find_element(by=By.TAG_NAME, value=tag_name)

driver.implicitly_wait(10)

input('Press Enter to quit...')
driver.quit()