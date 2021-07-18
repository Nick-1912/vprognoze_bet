import requests
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from fuzzywuzzy import fuzz as f
from data import *

CASH = 100
bets = []
# {'sport_name': str, 'tournament_name': str, 'teams_name': str, 'predict': str, 'amount': str}

a = requests.get('https://vprognoze.ru/forecast/newbie/fcutennis/9429414-kudermetova-muhova.html')
soup = bs4.BeautifulSoup(a.text, 'lxml')
if soup.find('table', class_="table express-table"):
    pass
else:
    sport_name = soup.find('div', class_="view-match__place").text
    tournament_name = soup.find('div', class_="view-match__league").text
    teams = soup.find_all('div', class_="view-match__team-name")
    teams_name = teams[0].text + ' - ' + teams[1].text
    predict_ = soup.find_all('div', class_="tip-line__info ui-badge")
    bets.append({'sport_name': sport_name, 'tournament_name': tournament_name,
                 'teams_name': teams_name, 'predict': predict_[0].text, 'amount': predict_[1].text})


chrome_options = Options()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/home/nick/chromedriver', options=chrome_options)
driver.set_window_size(1920, 1080)


for bet in bets:
    driver.get('https://1xstavka.ru/')
    time.sleep(5)

    top = driver.find_element_by_css_selector('div[class="assideCon_body top5"]').\
        find_elements_by_css_selector('span[class="sname"]')
    not_top = driver.find_elements_by_css_selector('div[class="assideCon_body not_top"]')[1].\
        find_elements_by_css_selector('span[class="sname"]')

    for temp in top + not_top:
        print(temp.text)
        if temp.text == bet['sport_name']:
            temp.click()
            break
    tournaments = driver.find_element_by_css_selector('ul[class="liga_menu"]').\
        find_elements_by_tag_name('li')

    count = 1
    for tournament in tournaments:
        str2 = tournament.text.split('\n')[0]
        ratio = f.WRatio(bet['tournament_name'], str2)
        if ratio > 70:
            print(count, ratio)
            tournament.find_element_by_css_selector('span[class="strelochka arr_open"]').click()
        count += 1
    print('~~~')
    # matches = driver.find_elements_by_css_selector('span[class="gname"]')
    matches = driver.find_elements_by_css_selector('ul[class="event_menu"]')
    matches_ = []
    for match in matches:
        matches_ += match.find_elements_by_tag_name('li')
    count = 1
    for match in matches_:
        match_name = match.find_element_by_css_selector('span[class="gname"]')
        ratio = f.WRatio(bet['teams_name'], match_name.text)
        if ratio > 70:
            print(count, ratio)
            driver.get(match.find_element_by_tag_name('a').get_attribute('href'))
            break
        count += 1

    time.sleep(5)

    bets_1x = driver.find_elements_by_css_selector('span[class="bet_type"]')
    for bet_1x in bets_1x:
        if bet['predict'] == bet_1x.text:
            bet_1x.click()
            cash = CASH * float(bet['amount'])
            CASH -= cash
            driver.find_element_by_css_selector('input[class="c-spinner__input bet_sum_input"]').send_keys(str(cash))
            break
    else:
        pass
