from app.yandex import YaPage, YandexImagesPage
from app.logger import logger
from selenium.webdriver.remote.webelement import WebElement
from urllib.parse import unquote_plus
from selenium import webdriver


class TestYandex:

    def test_1(self, browser: webdriver):
        logger.info("******************** ПЕРВЫЙ ТЕСТ ********************")

        logger.info("1. Зайти на https://ya.ru/")
        yandex_main_page = YaPage(browser)
        yandex_main_page.init_page()
        yandex_main_page.wait_for_page_loads()
        assert browser.current_url == "https://ya.ru/"

        logger.info("2. Проверить наличия поля поиска")
        input_box: WebElement = yandex_main_page.get_input_box()
        assert input_box is not None

        logger.info("3. Ввести в поиск Тензор")
        yandex_main_page.input_text("Тензор")

        logger.info("4. Проверить, что появилась таблица с подсказками (suggest)")
        suggestions: WebElement = yandex_main_page.get_suggestions()
        assert suggestions is not None

        logger.info("5. Нажать enter")
        yandex_main_page.click_on_the_search_button()

        logger.info("6. Проверить, что появилась страница результатов поиска")
        assert "тензор" in unquote_plus(browser.current_url, "utf-8").lower()

        logger.info("7. Проверить 1 ссылка ведет на сайт tensor.ru")
        first_link = yandex_main_page.get_first_search_result_link()
        assert "tensor.ru" in first_link

    def test_2(self, browser: webdriver):
        logger.info("******************** ВТОРОЙ ТЕСТ ********************")

        logger.info("1. Зайти на https://ya.ru/")
        yandex_main_page = YaPage(browser)
        yandex_main_page.init_page()
        yandex_main_page.wait_for_page_loads()
        assert browser.current_url == "https://ya.ru/"

        logger.info("2. Проверить, что кнопка меню присутствует на странице")
        all_services_button = yandex_main_page.get_all_services_button()
        assert all_services_button is not None

        logger.info("3. Открыть меню, выбрать “Картинки”")
        yandex_main_page.go_to_images_service()
        yandex_main_page.wait_for_page_loads()

        logger.info("4. Проверить, что перешли на url https://yandex.ru/images/")
        yandex_img_page = YandexImagesPage(browser)
        assert browser.current_url == yandex_img_page.root_page  # "https://yandex.ru/images/"

        logger.info("5. Открыть первую категорию")
        # получаем список категорий изображений
        img_cats = yandex_img_page.get_images_categories()
        # получаем ссылку на первую категорию
        first_cat_link = list(img_cats[0].values())[0]
        # открываем ссылку и переходим на новую открывшуюся вкладку
        yandex_img_page.open_new_page(first_cat_link)
        # проверка совпадения адреса новой вкладки со ссылкой категории
        yandex_img_page.wait_for_page_loads()
        assert browser.current_url == first_cat_link

        logger.info("6. Проверить, что название категории отображается в поле поиска")
        yandex_img_page.wait_for_page_loads()
        # получаем текст из строки поиска
        input_text = yandex_img_page.get_input_box_text()
        # сравниваем текст поиска с названием первой категории
        first_cat_text = list(img_cats[0].keys())[0]
        assert input_text == first_cat_text

        logger.info("7. Открыть 1 картинку")
        # получаем элементы изображений
        thumbs = yandex_img_page.get_thumbs_in_images()
        # открываем первое изображение
        thumbs[0].click()

        logger.info("8. Проверить, что картинка открылась")
        # получаем адрес источника открытого изображения
        img_1_src = yandex_img_page.get_opened_image_source()
        # проверяем наличие адреса, т.е. открылось ли изображение
        assert img_1_src is not None

        logger.info("9. Нажать кнопку вперед")
        # получаем кнопки навигации по изображениям
        prev_img_btn, next_img_btn = yandex_img_page.get_image_nav_btns()
        # нажимаем на кнопку следующего изображения
        next_img_btn.click()

        logger.info("10. Проверить, что картинка сменилась")
        # получаем адрес источника открытого изображения
        img_2_src = yandex_img_page.get_opened_image_source()
        # проверяем наличие адреса, т.е. открылось ли изображение
        assert img_2_src is not None

        logger.info("11. Нажать назад")
        # нажимаем на кнопку предыдущего изображения
        prev_img_btn.click()

        logger.info("12. Проверить, что картинка осталась из шага 8")
        # получаем адрес источника открытого изображения
        img_3_src = yandex_img_page.get_opened_image_source()
        # проверяем равенство ссылок первого открытого изображения и того же изображения после навигации
        assert img_3_src == img_1_src




