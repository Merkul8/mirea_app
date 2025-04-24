import random
import time

from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


class ElibraryParser:
    def __init__(self, elibrary_id):
        self.elibrary_id: int = elibrary_id
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        # Скрываем WebDriver статус
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver

    def _human_like_interaction(self):
        """Имитация человеческого поведения"""
        action = ActionChains(self.driver)

        # Случайные движения мыши
        for _ in range(random.randint(2, 4)):
            x = random.randint(0, 300)
            y = random.randint(0, 300)
            action.move_by_offset(x, y).perform()
            time.sleep(random.uniform(0.2, 0.7))

        # Случайный скроллинг
        scroll_px = random.randint(200, 500)
        self.driver.execute_script(f"window.scrollBy(0, {scroll_px});")
        time.sleep(random.uniform(1, 2))

    def _parse_name_and_affiliation(self, text):
        """Корректное разделение имени и аффилиации"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            return "", ""

        name = lines[0]
        affiliation = ' '.join(lines[1:]) if len(lines) > 1 else ""

        # Дополнительная очистка
        name = ' '.join(name.split())
        affiliation = ' '.join(affiliation.split())

        return name, affiliation

    def elibrary_data(self):
        try:
            url = f"https://www.elibrary.ru/author_items_print.asp?authorid={self.elibrary_id}"
            self.driver.get(url)

            # Имитация человеческого поведения
            self._human_like_interaction()

            # Проверка на CAPTCHA
            if "необычно много запросов" in self.driver.page_source:
                print("Обнаружена CAPTCHA, требуется ручное решение")
                input("Пожалуйста, решите CAPTCHA в браузере и нажмите Enter...")
                time.sleep(2)

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Извлечение данных автора
            author_block = soup.find('center').find('font')
            name_and_affiliation = author_block.get_text('\n', strip=True)
            name, affiliation = self._parse_name_and_affiliation(name_and_affiliation)

            # Парсинг публикаций
            publications = []
            for row in soup.find_all('tr')[1:]:  # Пропускаем заголовок таблицы
                cols = row.find_all('td')
                if len(cols) >= 3:
                    pub_num = cols[0].get_text(strip=True)
                    pub_title = cols[1].find('b').get_text(' ', strip=True) if cols[1].find('b') else ''
                    authors = cols[1].find('i').get_text(' ', strip=True) if cols[1].find('i') else ''
                    journal_info = cols[1].contents[-1].strip()
                    citations = cols[2].get_text(strip=True)

                    # Очистка данных
                    journal_info = ' '.join(journal_info.split())

                    publications.append({
                        'number': pub_num,
                        'title': pub_title,
                        'authors': authors,
                        'journal': journal_info,
                        'citations': citations
                    })

            return {
                'name': name,
                'affiliation': affiliation,
                'publications': publications
            }

        except Exception as e:
            print(f"Ошибка при парсинге: {e}")
            return None

        finally:
            self.driver.quit()