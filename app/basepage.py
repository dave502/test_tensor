from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver


class BasePage:

    @property
    def root_page(self):
        raise NotImplementedError

    def __init__(self, driver: webdriver, time_out: int = 10) -> None:
        self.driver: webdriver = driver
        self.action_time_out: int = time_out

    def __new__(cls, driver: webdriver):
        if isinstance(driver, webdriver.firefox.webdriver.WebDriver):
            return super(BasePage, cls).__new__(cls)
        else:
            raise ValueError

    def init_page(self) -> None:
        """
        Go to main page
        :return:
        """
        self.driver.get(self.root_page)

    def find_element(self, locator: tuple[str, str], time_out: int | None = None) -> WebElement:
        """
        get element from page
        :param locator: locator for element
        :param time_out: max time for searching element
        :return: WebElement
        """
        return WebDriverWait(self.driver, time_out if time_out is not None else self.action_time_out). \
            until(EC.presence_of_element_located(locator), message=f"Can't find element by locator {locator}")

    def find_elements(self, locator: tuple[str, str], time_out: int | None = None) -> list[WebElement]:
        """
        get list of elements from page
        :param locator: locator for elements
        :param time_out: max time for searching elements
        :return: list of WebElements
        """
        return WebDriverWait(self.driver, time_out if time_out is not None else self.action_time_out). \
            until(EC.presence_of_all_elements_located(locator), message=f"Can't find elements by locator {locator}")

    def wait_for_page_loads(self, time_out: int | None = None) -> None:
        """
        wait until page completely loads
        :param time_out: max time for waiting
        :return:
        """
        return WebDriverWait(self.driver, time_out if time_out is not None else self.action_time_out). \
            until(lambda driver: ("redirect" not in driver.current_url) and
                                 (driver.execute_script('return document.readyState') == 'complete'))

    def wait_for_new_window_loads(self, old_windows_count: int, time_out: int | None = None) -> None:
        """
        wait until new window opens in next tab and assign new window to driver
        :param old_windows_count: previous count of windows
        :param time_out:  max time for waiting
        :return:
        """
        WebDriverWait(self.driver, time_out if time_out is not None else self.action_time_out).\
            until(EC.number_of_windows_to_be(old_windows_count+1))
        next_window_handle: str = self.driver.window_handles[old_windows_count]
        self.driver.switch_to.window(next_window_handle)

    def press_enter_on_element(self, element: WebElement) -> None:
        """
        perform a ketboard Enter press for the element
        :param element: element for getting press Enter event
        :return:
        """
        element.send_keys(Keys.ENTER)

    def open_link(self, element: WebElement) -> str:
        """
        открыть ссылку элемента в новой вкладке
        :param element: элемент со ссылкой href
        :return: handler нового окна
        """
        href = element.get_attribute('href')
        return self.open_new_page(href)

    def open_new_page(self, link: str) -> str:
        """
        open new window in next tab and assign new window to driver
        :param link: url for new window
        :return: handler
        """
        windows_before = self.driver.window_handles
        self.driver.execute_script(f'window.open("{link}","_blank");')
        WebDriverWait(self.driver, 120).until(EC.new_window_is_opened(windows_before))
        wnd_handles: list[str] = self.driver.window_handles
        new_window_handler: str = self.driver.window_handles[len(wnd_handles) - 1]
        self.driver.switch_to.window(new_window_handler)
        return new_window_handler
