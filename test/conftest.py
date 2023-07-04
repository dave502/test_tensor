import pytest
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import logging


@pytest.fixture(scope="session")
def browser():
    logger = logging.getLogger(__name__)
    logger.debug("Creating the driver...")
    firefox_path = "/usr/bin/firefox"
    options = FirefoxOptions()
    # options.add_argument('--headless')
    options.binary_location = firefox_path
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    yield driver
    driver.quit()
