"""
Copyright (c) 2024 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
from abc import ABCMeta, abstractmethod
from typing import Dict, Union, List, TypedDict, Callable
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from web_render.tool import log
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from .extends import auth_http_proxy
import undetected_chromedriver as uc
import platform
import subprocess


logger = log(__name__)

current_platform = platform.system()

if current_platform == "Windows":
    def get_google_chrome_version():
        try:
            cmd = 'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
            version = result.strip()
            return version
        except subprocess.CalledProcessError as e:
            logger.info(f"Error executing google-chrome-stable: {e}")
            return None
elif current_platform == "Linux":
    logger.info("Running on Linux")
    def get_google_chrome_version():
        try:
            cmd = ["google-chrome-stable", "--version"]
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
            version = result.strip()
            return version
        except subprocess.CalledProcessError as e:
            logger.info(f"Error executing google-chrome-stable: {e}")
            return None
elif current_platform == "Darwin":
    logger.warning(f"Platform {current_platform} not support")
else:
    logger.warning(f"Platform {current_platform} not support")


def get_chromedriver_version(chromedriver_path):
    try:
        cmd = [chromedriver_path, "--version"]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        version = result.strip().split()[1]
        return version
    except subprocess.CalledProcessError as e:
        logger.info(f"Error executing Chromedriver: {e}")
        return None


class IWebWait(TypedDict):
    name: str
    params: Dict


class AbstractRender(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, browser):
        self.browser = browser

    @abstractmethod
    def set_url(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_content(self, *args, **kwargs):
        pass

    @abstractmethod
    def quit(self, *args, **kwargs):
        pass


class SeleniumRender(AbstractRender):

    def __init__(self, browser: WebDriver, timeout_web_wait=10):
        self.browser = browser
        self._web_driver_wait = WebDriverWait(self.browser, timeout_web_wait)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def _web_wait(self, items: Union[IWebWait, List[IWebWait]]):
        if isinstance(items, list):
            for item in items:
                target: Callable = web_wait_class[item['name']](**item['params'])
                self._web_driver_wait.until(target)

        if isinstance(items, dict):
            target: Callable = web_wait_class[items['name']](**items['params'])
            self._web_driver_wait.until(target)

    def web_wait(self, items: Union[IWebWait, List[IWebWait]]):
        self._web_wait(items)

    def set_url(self, url, web_wait: Union[IWebWait, List[IWebWait], None]=None,
                execute_script=None, execute_async_script=None):
        self.browser.get(url)

        if web_wait:
            self._web_wait(web_wait)

        if execute_script:
            self.browser.execute_script(execute_script)

        if execute_async_script:
            self.browser.execute_async_script(execute_async_script)

    def get_content(self):
        return self.browser.page_source

    def quit(self):
        self.browser.quit()
        logger.info(f"Close {self.browser}")


def make_selenium_webdriver(config: Dict):
    co = Options()
    if config.get("PROXY_SERVER"):
        co.add_argument(f"--proxy-server={config['PROXY_SERVER']}")
    if config.get("AUTH_PROXY_SERVER"):
        auth, ip = config.get("AUTH_PROXY_SERVER").strip().split("@")
        host, port = ip.split(":")
        login, pwd = auth.split(":")
        co.add_encoded_extension(auth_http_proxy(host, port, login, pwd))
    if config.get('HEADLESS'):
        co.add_argument('--headless=new')

    co.add_argument('--disable-blink-features=AutomationControlled')
    co.add_argument('--no-sandbox')
    co.add_argument('--disable-dev-shm-usage')
    co.add_argument("start-maximized")

    if config.get('INCOGNITO'):
        co.add_argument("--incognito")
    if config.get('USER_DATA_DIR'):
        co.add_argument(f"user-data-dir={config.get('USER_DATA_DIR')}")
    co.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    co.add_experimental_option("excludeSwitches", ["enable-automation"])
    co.add_experimental_option('useAutomationExtension', False)

    if config.get("LOGGING_PREFS"):
        co.set_capability('goog:loggingPrefs', config.get("LOGGING_PREFS"))

    chrome_prefs = dict()
    if config.get("LANGUAGE"):
        # example en,en_US
        chrome_prefs['intl.accept_languages'] = config.get("LANGUAGE")

    if config.get('DISABLE_IMAGE'):
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    if config.get('DISABLE_WEBRTC'):
        chrome_prefs["webrtc.ip_handling_policy"] = "disable_non_proxied_udp"
        chrome_prefs["webrtc.multiple_routes_enabled"] = False
        chrome_prefs["webrtc.nonproxied_udp_enabled"] = False

    co.add_experimental_option("prefs", chrome_prefs)

    download_driver = Service(ChromeDriverManager(
        driver_version=config.get('CHROME_DRIVER_VERSION')
    ).install())

    # -- Version
    google_chrome_version = get_google_chrome_version()
    if google_chrome_version:
        logger.info(f"Google Chrome version: {google_chrome_version}")

    chromedriver_version = get_chromedriver_version(download_driver.path)
    if chromedriver_version:
        logger.info(f"Chromedriver version: {chromedriver_version}")
    ### --

    if config.get('UNDETECTED_CHROMEDRIVER'):
        driver = uc.Chrome(headless=config.get('HEADLESS'))
    else:
        driver = webdriver.Chrome(service=download_driver, options=co)

    if config.get('FULLSCREEN_WINDOW'):
        driver.fullscreen_window()

    if config.get('SET_WINDOW_SIZE'):
        width, height = [int(x) for x in config.get('SET_WINDOW_SIZE').split("x")]
        driver.set_window_size(width, height)

    if config.get('LOAD_TIMEOUT'):
        driver.set_page_load_timeout(config['LOAD_TIMEOUT'])
    return driver


class CheckElementInDOM:

    def __init__(self, selectors: List[str]):
        self.selectors = selectors

    def check_element(self, driver: WebDriver):
        for selector in self.selectors:
            try:
                driver.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                return False
        return True

    def __call__(self, driver: WebDriver):
        return self.check_element(driver)


class CheckElementsInDOM:

    def __init__(self, selectors: List[str]):
        self.selectors = selectors

    def check_elements(self, driver: WebDriver):
        quantity = len(self.selectors)
        x = 0
        for selector in self.selectors:
            try:
                driver.find_element(By.CSS_SELECTOR, selector)
                x += 1
            except NoSuchElementException:
                x -= 1

        if quantity == x:
            return True

        return False

    def __call__(self, driver: WebDriver):
        return self.check_elements(driver)

class CheckNumberElementsInPage:

    def __init__(self, selector, count):
        self.css_selector: str = selector
        self.quantity: int = count

    def check_elements(self, driver: WebDriver):
        elements = driver.find_elements(By.CSS_SELECTOR, self.css_selector)
        if len(elements) >= self.quantity:
            return True
        return False

    def __call__(self, driver: WebDriver):
        return self.check_elements(driver)


web_wait_class = {
    "CheckElementInDOM" : CheckElementInDOM,
    "CheckElementsInDOM": CheckElementsInDOM,
    "CheckNumberElementsInPage": CheckNumberElementsInPage
}
