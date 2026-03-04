from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
import argparse

# --headless damit kein firefox fenster geöffnet wird und alles in der Konsole ausgegeben wird
options = FirefoxOptions()
options.add_argument('--headless')

# Da Firefox durchgehend abgebrochen wird, logge ich den ouput
service = FirefoxService(
    log_output=open('error.log', 'w'),
    service_args=['--log', 'trace'],
)

# Damit --parsing funktioniert, posix für gutes ux
parser = argparse.ArgumentParser()
parser.add_argument('--url')
parser.add_argument('--tag')
args = parser.parse_args()

driver = webdriver.Firefox(options=options, service=service)
driver.get(args.url)

# Selenium Zeit geben das Element zu finden
driver.implicitly_wait(10)

# wir holen den Tag mit dem --tag aus dem Argument
tag_output = driver.find_element(by=By.TAG_NAME, value=args.tag)

# Ohne .text wird nur das Web Element ausgegeben
print(f"\033[33mOutput tag:\033[0m", tag_output.text)

# Driver beenden nach dem scraping
driver.quit()