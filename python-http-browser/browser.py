from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
import argparse

# Headless Firefox Driver erstellen
def create_driver():
    options = FirefoxOptions()
    # --headless damit kein firefox fenster geöffnet
    options.add_argument('--headless')
    # firefox json view deaktivieren, da dieser die Formatierung verhindert
    options.set_preference("devtools.jsonview.enabled", False)

    # Logged Output in error.log
    service = FirefoxService(
        log_output=open('error.log', 'w'),
        service_args=['--log', 'trace'],
    )

    driver = webdriver.Firefox(options=options, service=service)
    driver.implicitly_wait(10)  # Selenium Zeit geben das Element zu finden
    return driver

def create_parser():
    # Damit --parsing funktioniert, posix für gutes ux
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    # Scrape Command
    scrape_parser = subparser.add_parser('scrape')
    scrape_parser.add_argument('--url')
    scrape_parser.add_argument('--tag')

    # Get Command
    get_parser = subparser.add_parser('get')
    get_parser.add_argument('--url')
    get_parser.add_argument('--param')

    # Post Command
    post_parser = subparser.add_parser('post')
    post_parser.add_argument('--url')
    # action='append' damit --param mehrmals übergeben werden kann
    post_parser.add_argument('--param', action='append')

    # Cookie Liste Command
    cookies = subparser.add_parser('list-cookies')
    cookies.add_argument('--url')

    # Header Command
    header_parser = subparser.add_parser('header')
    header_parser.add_argument('--url')

    # Detect CMS Command
    detect_parser = subparser.add_parser('detect-cms')
    detect_parser.add_argument('--url')

    return parser.parse_args()

def scrape_tag(url, tag):
    driver.get(url)
    return driver.find_element(by=By.TAG_NAME, value=tag).text  # ohne .text wird nur das WebElement ausgegeben

def get(url, params):
    driver.get(url + '?' + params)
    return driver.find_element(by=By.TAG_NAME, value='body').text

def post(url, params):
    driver.get(url)
    # Wenn es mehrere Parameter gibt
    for current_param in params:
        key, value = current_param.split('=')
        field = driver.find_element(by=By.NAME, value=key)
        field.send_keys(value)

    # Auf den Form button klicken
    submit_button = driver.find_element(by=By.TAG_NAME, value='button')
    submit_button.click()
    return driver.find_element(by=By.TAG_NAME, value='body').text

def list_cookies(url):
    driver.get(url)
    cookies = driver.get_cookies()
    return '\n'.join([f"\033[32m{cookie['name']}\033[0m : {cookie['value']}" for cookie in cookies])

def header(url):
    driver.get(url)
    # execute_async_script wird verwendet, da fetch() asynchron ist
    # callback signalisiert Selenium wenn der Request fertig ist
    # Object.fromEntries() konvertiert die Headers direkt in ein Dictionary
    headers = driver.execute_async_script(
        """
        const callback = arguments[arguments.length - 1];
        const url = arguments[0];
        fetch(url).then(response => callback(Object.fromEntries(response.headers)));
        """
        , url)

    # Jeden Header auf einer eigenen Zeile ausgeben
    return '\n'.join(f'\033[1m\033[31m{key} :\033[0m {value}' for key, value in headers.items())

def detect_cms(url):
    driver.get(url)
    source = driver.page_source
    used_cms = None

    # Einfachste Methode: Generator Meta-Tag auslesen
    # Nicht immer zuverlässig, da viele Sites diesen Tag entfernen
    try:
        generator = driver.find_element(by=By.CSS_SELECTOR, value='meta[name="generator"]')
        used_cms = generator.get_attribute('content')
    except Exception:
        pass

    # Fallback: Bekannte CMS Signaturen im Quellcode suchen
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

    return f'\033[1mCMS found:\033[32m {used_cms} \033[0m'

# Startfunktion
def run():
    output = None

    if args.command == 'scrape':
        output = scrape_tag(args.url, args.tag)
    elif args.command == 'get':
        output = get(args.url, args.param)
    elif args.command == 'post':
        output = post(args.url, args.param)
    elif args.command == 'list-cookies':
        output = list_cookies(args.url)
    elif args.command == 'header':
        output = header(args.url)
    elif args.command == 'detect-cms':
        output = detect_cms(args.url)

    print(f"\033[1m\033[34mOUTPUT:\033[0m\n{output if output else 'No output'}")


driver = create_driver()
args = create_parser()

try:
    run()
finally:
    driver.quit()




