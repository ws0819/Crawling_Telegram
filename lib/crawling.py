from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

class Crawling:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        URL = 'https://www.bandtrass.or.kr/customs/total.do?command=CUS001View&viewCode=CUS00401' # 수출입데이터
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)
        self.driver.get(URL)
        
    def get_search(self, hscode): # 년월 // 금액(달러) 금액(원화) 중량(Kg)
        crawling_dict = {}
        try:
            while True:
                self.driver.find_element(By.ID, 'SelectCd').send_keys(int(hscode))
                self.driver.execute_script('goSearch();')
                table_list = self.driver.find_element(By.ID, 'table_list_1').text
                if table_list:
                    for i in str(table_list).split("\n"):
                        tmp_list = i.split(' ')
                        crawling_dict[tmp_list[0]] = tmp_list[1:]
                if time.sleep(3):
                    break
        except:
            self.driver.refresh()
        return crawling_dict