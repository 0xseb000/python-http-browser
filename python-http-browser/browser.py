from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
import argparse

options = FirefoxOptions()
# --headless damit kein firefox fenster geöffnet
options.add_argument('--headless')
# firefox json view ausblenden, da dieser die Formatierung verhindert
options.set_preference("devtools.jsonview.enabled", False)

# Da Firefox durchgehend abgebrochen wird, logge ich den ouput
service = FirefoxService(
    log_output=open('error.log', 'w'),
    service_args=['--log', 'trace'],
)

# Damit --parsing funktioniert, posix für gutes ux
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

# Scrape Logik
scrape_parser = subparser.add_parser('scrape')
scrape_parser.add_argument('--url')
scrape_parser.add_argument('--tag')

# Get Logik
get_parser = subparser.add_parser('get')
get_parser.add_argument('--url')
get_parser.add_argument('--param')

# Post Logik
post_parser = subparser.add_parser('post')
post_parser.add_argument('--url')
post_parser.add_argument('--param', action='append')

args = parser.parse_args()

driver = webdriver.Firefox(options=options, service=service)
driver.implicitly_wait(10) # Selenium Zeit geben das Element zu finden

output = None

if args.command == 'scrape': # Hier scrapen wir nach Tag
    driver.get(args.url)
    output = driver.find_element(by=By.TAG_NAME, value=args.tag) # tag in value einsetzen

elif args.command == 'get': # Hier verwenden wit get und fügen parameter hinzu
    driver.get(args.url + '?' + args.param)
    output = driver.find_element(by=By.TAG_NAME, value='body')

elif args.command == 'post':
    driver.get(args.url)

    # Wenn es mehrere Parameter gibt
    for current_param in args.param:
        key, value = current_param.split('=')
        field = driver.find_element(by=By.NAME, value=key)
        field.send_keys(value)

    # Auf den Form button klicken
    submit_button = driver.find_element(by=By.TAG_NAME, value='button')
    submit_button.click()
    output = driver.find_element(by=By.TAG_NAME, value='body')


# .text extrahiert den Text aus dem WebElement
print(f"\033[33mOutput:\033[0m", output.text)

# Driver beenden nach dem scraping
driver.quit()