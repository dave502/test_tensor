from app.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from app.logger import logger, debugging, debuglog

_debugging_ = debugging()


class YandexBase(BasePage):
    """
    Класс с общими элементами для сервисов яндекса
    """
    LOCATOR_YANDEX_INPUT_FIELD = (By.XPATH, '//input[@name="text"]')
    LOCATOR_YANDEX_INPUT_SUGGESTIONS = (By.XPATH, '//li[contains(@class,"mini-suggest__item")]')
    LOCATOR_YANDEX_SEARCH_BUTTON = (By.XPATH, '//button[contains(@class, "search") and @type="submit" ]')

    @property
    def root_page(self):
        """
        главная страница сервиса
        :return:
        """
        raise NotImplementedError

    @debuglog(_debugging_, "Getting input field...")
    def get_input_box(self) -> WebElement:
        """
        получить строку поиска
        """
        input_field = self.find_element(self.LOCATOR_YANDEX_INPUT_FIELD)
        return input_field

    @debuglog(_debugging_, "Getting input field's text...")
    def get_input_box_text(self) -> str:
        """
        получить текст из строки поиска
        """
        input_field = self.get_input_box()
        return input_field.get_attribute('value')

    @debuglog(_debugging_, "Entering text to input field...")
    def input_text(self, text: str) -> WebElement:
        """
        ввести текст в строку посика
        """
        search_field = self.get_input_box()
        search_field.click()
        search_field.send_keys(text)
        return search_field

    @debuglog(_debugging_, "Getting suggestions...")
    def get_suggestions(self) -> WebElement:
        """
        получить выпадающие подсказки к строке поиска
        """
        search_suggestions = self.find_element(self.LOCATOR_YANDEX_INPUT_SUGGESTIONS)
        return search_suggestions

    @debuglog(_debugging_, "Pressing the Find button...")
    def click_on_the_search_button(self) -> None:
        """
        нажать кнопку поиска
        """
        self.find_element(self.LOCATOR_YANDEX_SEARCH_BUTTON, time_out=5).click()


class YaPage(YandexBase):
    """
    Страница ya.ru
    """
    root_page = "https://ya.ru/"

    LOCATOR_YANDEX_SEARCH_RESULTS = (By.XPATH, '//li[contains(@class,"serp-item")]'
                                               '//a[contains(@class,"Link_theme_normal") '
                                               'and not (contains(@class,"sitelinks")) ]')
    LOCATOR_YANDEX_ALL_SERVICES_BUTTON = (By.XPATH, '//a[@href="https://yandex.ru/all" and @role="button"]/..')
    LOCATOR_YANDEX_NAVIGATION_BAR = (By.XPATH, '//nav')
    LOCATOR_YANDEX_NAVIGATION_LINK = (By.XPATH, '//a[div[contains(text(), "<item_text>")]]')

    @debuglog(_debugging_, "Getting search result links...")
    def get_search_results_links(self, link: str, limit: int = 5) -> list[str]:
        """
        получить результаты поиска содержащие указанную ссылку
        limit - количество получаемых результатов
        """
        search_results = self.find_elements(self.LOCATOR_YANDEX_SEARCH_RESULTS)
        links = []
        for _, search_item in zip(range(limit), search_results):
            href = search_item.get_attribute('href')
            if link not in href:
                break
            else:
                links.append(href)
        return links

    @debuglog(_debugging_, "Getting first search result link...")
    def get_first_search_result_link(self) -> WebElement:
        """
        получить ссылку первого результата поиска
        """
        search_result = self.find_element(self.LOCATOR_YANDEX_SEARCH_RESULTS)
        href = search_result.get_attribute('href')
        return href

    @debuglog(_debugging_, "Getting services button...")
    def get_all_services_button(self) -> WebElement:
        """
        получить кнопку меню со всеми сервисами яндекса
        """
        input_box = self.get_input_box()
        input_box.click()
        all_services_button = self.find_element(self.LOCATOR_YANDEX_ALL_SERVICES_BUTTON)
        return all_services_button

    @debuglog(_debugging_, "Getting to Images service...")
    def go_to_images_service(self) -> None:
        services_button = self.get_all_services_button()
        services_button.click()
        imgs_button = self.get_service_link("Картинки")
        old_windows_count = len(self.driver.window_handles)
        imgs_button.click()
        self.wait_for_new_window_loads(old_windows_count)

    # def get_navigation_menu(self) -> WebElement:
    #     """
    #     получить панель навигации
    #     """
    #     nav_bar = self.find_element(self.LOCATOR_YANDEX_NAVIGATION_BAR)
    #     return nav_bar

    @debuglog(_debugging_, "Getting service navigation link...")
    def get_service_link(self, link_text: str) -> WebElement:
        """
        получить элемент панели навигации
        link_text - текст элемента навигации
        """
        locator_yandex_service_link: tuple[str, str] = self.LOCATOR_YANDEX_NAVIGATION_LINK[0], \
            self.LOCATOR_YANDEX_NAVIGATION_LINK[1].replace('<item_text>', link_text)
        nav_link: WebElement = self.find_element(locator_yandex_service_link)
        return nav_link


class YandexImagesPage(YandexBase):
    """
    Страница сервиса Картинки
    """

    root_page = "https://yandex.ru/images/"

    LOCATOR_YANDEX_IMG_CATEGORIES = (By.XPATH, '//div[@data-grid-name="im"]')
    LOCATOR_YANDEX_IMG_LINKS = (By.XPATH, '//a[@class="serp-item__link"]/img')
    LOCATOR_YANDEX_NEXT_IMG = (By.XPATH, '//div[contains(@class, "CircleButton_type_next")]')
    LOCATOR_YANDEX_PREV_IMG = (By.XPATH, '//div[contains(@class, "CircleButton_type_prev")]')

    @debuglog(_debugging_, "Getting images categories...")
    def get_images_categories(self):
        """
        получить элементы категорий изображений
        """
        img_cats = self.find_elements(self.LOCATOR_YANDEX_IMG_CATEGORIES)
        img_catefories = [
            {item.get_attribute('data-grid-text'): item.find_element(By.XPATH, './a').get_attribute('href')} for
            item in
            img_cats]
        return img_catefories

    @debuglog(_debugging_, "Getting images thumbs...")
    def get_thumbs_in_images(self):
        """
        получить элементы изображений
        """
        images = self.find_elements(self.LOCATOR_YANDEX_IMG_LINKS)
        return images

    @debuglog(_debugging_, "Getting images navigation button...")
    def get_image_nav_btns(self):
        """
        получить элементы навигации изображений
        """
        prev_img_btn = self.find_element(self.LOCATOR_YANDEX_PREV_IMG)
        next_img_btn = self.find_element(self.LOCATOR_YANDEX_NEXT_IMG)
        return prev_img_btn, next_img_btn

    @debuglog(_debugging_, "Getting opened image's source url...")
    def get_opened_image_source(self):
        """
        получить источник открытого изображения
        """
        locator = (By.XPATH, f'//img[@class="MMImage-Origin"]')
        source = self.find_element(locator).get_attribute('src')
        return source
