import undetected_chromedriver as uc
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class AvitoParse:
    def __init__(self, url:str, items:list, price=0, count=100, chrome_version=None):
        self.url = url
        self.price = price
        self.items = items
        self.count = count
        self.chrome_version = chrome_version
        self.data = []

    def __set_up(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = uc.Chrome(version_main=self.chrome_version, options=options)
    
    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        while self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]') and self.count > 0:
            self.__parse_page()
            self.driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]').click()
            self.count -= 1

    def __parse_page(self):
        titles = self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
        for i in titles:
            name = i.find_element(By.CSS_SELECTOR, '[itemprop="name"]').text
            description = i.find_element(By.CSS_SELECTOR, '[class*="iva-item-descriptionStep-C0ty1"]').text
            url = i.find_element(By.CSS_SELECTOR, '[itemprop="url"]').get_attribute('href')
            price = i.find_element(By.CSS_SELECTOR, '[itemprop="price"]').get_attribute('content')
            data = {
                'name':name,
                'description':description,
                'url':url,
                'price':price
            }
            if any(i.lower() in description for i in self.items) and int(price) <= self.price :
                self.data.append(data)
                print([name, description, url, price])
        self.__save_data()

    def __save_data(self):
        with open('items.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()

if __name__=='__main__':
    url='https://www.avito.ru/sankt-peterburg?localPriority=0&q=%D1%82%D0%B5%D0%BB%D0%B5%D0%B2%D0%B8%D0%B7%D0%BE%D1%80'
    AvitoParse(url=url,count=10, items=['телевизор'],price=3000 ).parse()
