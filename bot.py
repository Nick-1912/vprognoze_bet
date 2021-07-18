from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.common.keys
import time
from fuzzywuzzy import fuzz as f
from vprognoze_api import *

CASH = 100
bets = []
done_bets = []


class BOT(object):

    def __init__(self, url_vprognoze_user):
        self.vprognoze_user = url_vprognoze_user
        self.is_headless = False
        self.number = 'number'
        self.password = 'pwd'
        self.driver = self.create_browser()
        self.get_main_page()
        # self.login()

    def create_browser(self):
        chrome_options = Options()
        if self.is_headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome('/home/nick/chromedriver', options=chrome_options)
        driver.set_window_size(1920, 1080)
        return driver

    def login(self):
        self.driver.find_element_by_css_selector('div[class="loginDropTop"]').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('button[class="custom-functional-button"]').click()
        time.sleep(1)
        input_number = self.driver.find_element_by_css_selector('input[type="tel"]')
        input_number.send_keys(self.number)
        input_password = self.driver.find_element_by_css_selector('input[id="auth-form-password"]')
        input_password.send_keys(self.password + selenium.webdriver.common.keys.Keys.ENTER)
        time.sleep(1)
        two_factor_authentication = input('[LOG] Введите код двухфакторной авторизации: ')
        input_two_factor_authentication = self.driver.find_element_by_css_selector('input[id="auth_user_pass"]')
        input_two_factor_authentication.send_keys(two_factor_authentication + selenium.webdriver.common.keys.Keys.ENTER)
        time.sleep(3)

    def get_main_page(self):
        self.driver.get('https://1xstavka.ru/')
        time.sleep(5)

    def get_all_predicts(self):
        global bets
        for predict in get_predicts(get_and_parse_url(self.vprognoze_user)):
            if not is_started(predict=predict):
                teams = get_teams(predict=predict)
                sport = get_tournament(predict=predict).split('.')[0]
                tournament = get_tournament(predict=predict).replace(sport + '.', '')
                persent = get_persent(predict=predict)
                bet_name = convert21x(bet_name=get_bet(predict=predict))
                if bet_name:
                    bet_object = {
                        'teams': teams,
                        'sport': sport,
                        'tournament': tournament,
                        'bet': bet_name,
                        'persent': persent
                    }
                    if bet_object not in bets and bet_object not in done_bets:
                        bets.append(bet_object)

    def find_match(self, bet_object):
        bet_found = 0
        top = self.driver.find_element_by_css_selector('div[class="assideCon_body top5"]'). \
            find_elements_by_css_selector('span[class="sname"]')
        not_top = self.driver.find_elements_by_css_selector('div[class="assideCon_body not_top"]')[1]. \
            find_elements_by_css_selector('span[class="sname"]')
        for match in top + not_top:
            if match.text == bet_object['sport']:
                match.click()
                break
        for tournament in self.driver.find_element_by_css_selector('ul[class="liga_menu"]'). \
                find_elements_by_tag_name('li'):
            if f.WRatio(bet_object['tournament'], tournament.text.split('\n')[0]) > 70:
                tournament.find_element_by_css_selector('span[class="strelochka arr_open"]').click()
        matches = []
        for match in self.driver.find_elements_by_css_selector('ul[class="event_menu"]'):
            matches += match.find_elements_by_tag_name('li')
        for match in matches:
            if f.WRatio(bet_object['teams'], match.find_element_by_css_selector('span[class="gname"]').text) > 70:
                self.driver.get(match.find_element_by_tag_name('a').get_attribute('href'))
                break
        time.sleep(5)
        print(self.driver.current_url)
        # необходима проверка на то, все ли окей
        self.driver.find_elements_by_css_selector('span[class="scoreboard-nav__btn-container"]')[-1].click()
        for bet_1x in (self.driver.find_elements_by_css_selector('div[class="bet_group shortName"]') +
                       self.driver.find_elements_by_css_selector('div[class="bet_group"]')):
            if (bet_1x.find_element_by_css_selector('div[class="bet-title bet-title_justify min"]').text ==
                    bet_object['bet'][0]):
                bet_1x.find_element_by_css_selector('div[class="bet-title bet-title_justify min"]').click()
                for bet_ in bet_1x.find_elements_by_css_selector('span[class="bet_type"]'):
                    if bet_.text == bet_object['bet'][1]:
                        bet_.click()
                        bet_found = 1
                        break
            if bet_found:
                break


if __name__ == '__main__':
    temp = BOT('https://vprognoze.ru/user/WITCHER_TB/')
    temp.get_all_predicts()
    temp.find_match(bet_object=bets[0])
