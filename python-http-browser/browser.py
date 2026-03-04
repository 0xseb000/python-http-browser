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

# Ich logge den output in error.log
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

# Cookie Liste
cookies = subparser.add_parser('list-cookies')
cookies.add_argument('--url')

# Header Logik
header_parser = subparser.add_parser('header')
header_parser.add_argument('--url')

detect_parser = subparser.add_parser('detect-cms')
detect_parser.add_argument('--url')

args = parser.parse_args()

driver = webdriver.Firefox(options=options, service=service)
driver.implicitly_wait(10) # Selenium Zeit geben das Element zu finden

output = None

if args.command == 'scrape': # Hier scrapen wir nach Tag
    driver.get(args.url)
    output = driver.find_element(by=By.TAG_NAME, value=args.tag).text # ohne .text wird nur das WebElement ausgegeben

elif args.command == 'get': # Hier verwenden wit get und fügen parameter hinzu
    driver.get(args.url + '?' + args.param)
    output = driver.find_element(by=By.TAG_NAME, value='body').text

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
    output = driver.find_element(by=By.TAG_NAME, value='body').text

elif args.command == 'list-cookies':
    driver.get(args.url)
    cookies = driver.get_cookies()
    for cookie in cookies:
        output = '\n'.join([f"\033[32m{cookie['name']}\033[0m : {cookie['value']}" for cookie in cookies])

elif args.command == 'header':
    driver.get(args.url)
    # execute_async_script wird verwendet, da fetch() asynchron ist
    # callback signalisiert Selenium wenn der Request fertig ist
    # Object.fromEntries() konvertiert die Headers direkt in ein Dictionary
    headers = driver.execute_async_script(
        """
        const callback = arguments[arguments.length - 1];
        const url = arguments[0];
        fetch(url).then(response => callback(Object.fromEntries(response.headers)));
        """
    , args.url)

    # Jeden Header auf einer eigenen Zeile ausgeben
    output = '\n'.join(f'\033[1m\033[31m{key} :\033[0m {value}' for key, value in headers.items())

elif args.command == 'detect-cms':
    driver.get(args.url)
    source = driver.page_source
    used_cms = None

    # generator meta tag sagt aus welches cms verwendet wurde (am einfachsten, aber nicht zuverlässig)
    try:
        generator = driver.find_element(by=By.CSS_SELECTOR, value='meta[name="generator"]')
        used_cms = generator.get_attribute('content')
    except:
        pass

    # wenn generator tag nicht gefunden/versteckt wurde, dann wird nach Signaturen gesucht
    cms_patterns = {
        'WordPress': ['/wp-content/', 'wp-admin/', 'wp-includes/', 'wordpress'],
        'PrestaShop': ['var prestashop', '/modules/prestashop'],
        'Contao': ['bundles/contao', '_contao/', 'contao', 'contao/main.php'],
        'Webflow': ['webflow.com', 'webflow'],
        'Shopify': ['cdn.shopify.com'],
        'Wix': ['static.wixstatic.com'],
    }

    # durch source durchgehen und schauen, ob cms pattern da sind
    for cms, signature in cms_patterns.items():
        if any(sig in source for sig in signature):
            used_cms = cms
            break

    output = f'\033[1mCMS found:\033[32m {used_cms} \033[0m'

print(f"\033[1m\033[34mOUTPUT:\033[0m\n{output if output else 'No output'}")

# Driver beenden nach dem scraping
driver.quit()