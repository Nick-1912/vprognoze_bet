import requests
from bs4 import BeautifulSoup
import datetime


def get_and_parse_url(url):
    return BeautifulSoup(requests.get(url).text, 'lxml')


def get_predicts(soup):
    return soup.find_all('div', class_="mini-tip__head")


def get_teams(predict):
    return predict.find('a', class_="mini-tip__teams").text


def get_tournament(predict):
    return predict.find('div', class_="mini-tip__league").text


def get_bet(predict):
    return predict.find('div', class_="mini-tip__bet").text.split(' @')[0]


def get_persent(predict):
    return predict.find('div', class_="mini-tip__profit").text[5:-1]


def is_started(predict):
    predict_date = predict.find('div', class_="ui-date__day").text.split('-')
    predict_time = predict.find('div', class_="ui-date__hour").text.split(':')
    if (datetime.datetime.now() - datetime.datetime(year=2021,
                                                    month=int(predict_date[1]),
                                                    day=int(predict_date[0]),
                                                    hour=int(predict_time[0]),
                                                    minute=int(predict_time[1]))).total_seconds() < -500:
        return False
    else:
        return True


def convert21x(bet_name):
    if 'ФОРА' in bet_name:
        if 'по очкам' in bet_name:
            return [
                'Фора',
                bet_name.replace('ФОРА', '').replace('по очкам (', '').replace(')', '')
            ]
        elif 'по партиям' in bet_name:
            return [
                'Фора по партиям',
                bet_name.replace('ФОРА', '').replace('по партиям (', '').replace(')', '')
            ]
        elif 'по сетам' in bet_name:
            return [
                'Фора по сетам',
                bet_name.replace('ФОРА', '').replace('по сетам (', '').replace(')', '')
            ]
        else:
            return [
                'Фора',
                bet_name.replace('ФОРА', '').replace('(', '').replace(')', '')
            ]
    elif 'ТБ' in bet_name:
        if 'ИТБ' in bet_name:
            if 'по очкам' in bet_name:
                if bet_name[3] == 1:
                    return [
                        'Индивидуальный тотал 1-го',
                        bet_name.replace('ИТБ1 по очкам (', '').replace(')', '') + ' Б'
                    ]
                elif bet_name[3] == 2:
                    return [
                        'Индивидуальный тотал 2-го',
                        bet_name.replace('ИТБ2 по очкам (', '').replace(')', '') + ' Б'
                    ]
            else:
                if bet_name[3] == 1:
                    return [
                        'Индивидуальный тотал 1-го',
                        bet_name.replace('ИТБ1 (', '').replace(')', '') + ' Б'
                    ]
                elif bet_name[3] == 2:
                    return [
                        'Индивидуальный тотал 2-го',
                        bet_name.replace('ИТБ2 (', '').replace(')', '') + ' Б'
                    ]
        elif 'по очкам' in bet_name:
            return [
                'Тотал',
                bet_name.replace('ТБ по очкам (', '').replace(')', '') + ' Б'
            ]
        elif 'по партиям' in bet_name:
            return [
                'Тотал партий',
                bet_name.replace('ТБ по партиям (', '').replace(')', '') + ' Б'
            ]
        elif 'по сетам' in bet_name:
            return [
                'Тотал сетов',
                bet_name.replace('ТБ по сетам (', '').replace(')', '') + ' Б'
            ]
        else:
            return [
                'Тотал',
                bet_name.replace('ТБ (', '').replace(')', '') + ' Б'
            ]
    elif 'ТМ' in bet_name:
        if 'ИТМ' in bet_name:
            if 'по очкам' in bet_name:
                if bet_name[3] == 1:
                    return [
                        'Индивидуальный тотал 1-го',
                        bet_name.replace('ИТМ1 по очкам (', '').replace(')', '') + ' М'
                    ]
                elif bet_name[3] == 2:
                    return [
                        'Индивидуальный тотал 2-го',
                        bet_name.replace('ИТМ2 по очкам (', '').replace(')', '') + ' М'
                    ]
            else:
                if bet_name[3] == 1:
                    return [
                        'Индивидуальный тотал 1-го',
                        bet_name.replace('ИТМ1 (', '').replace(')', '') + ' М'
                    ]
                elif bet_name[3] == 2:
                    return [
                        'Индивидуальный тотал 2-го',
                        bet_name.replace('ИТМ2 (', '').replace(')', '') + ' М'
                    ]
        elif 'по очкам' in bet_name:
            return [
                'Тотал',
                bet_name.replace('ТМ по очкам (', '').replace(')', '') + ' М'
            ]
        elif 'по партиям' in bet_name:
            return [
                'Тотал партий',
                bet_name.replace('ТМ по партиям (', '').replace(')', '') + ' М'
            ]
        elif 'по сетам' in bet_name:
            return [
                'Тотал сетов',
                bet_name.replace('ТМ по сетам (', '').replace(')', '') + ' М'
            ]
        else:
            return [
                'Тотал',
                bet_name.replace('ТМ (', '').replace(')', '') + ' М'
            ]
    elif 'Тотал' in bet_name:
        if 'по геймам' in bet_name:
            if 'больше' in bet_name:
                return [
                    'Тотал',
                    bet_name.replace('Тотал по геймам больше (', '').replace(')', '') + ' Б'
                ]
            else:
                return [
                    'Тотал',
                    bet_name.replace('Тотал по геймам меньше (', '').replace(')', '') + ' М'
                ]
        else:
            return None
    elif 'с ОТ' in bet_name:
        return [
            'Победа в матче',
            bet_name.replace(' с ОТ', '')
        ]
    elif 'Точный счет' in bet_name:
        return [
            'Точный счет',
            bet_name.replace('Точный счет ', '').replace(':', '-')
        ]
    elif 'П' in bet_name:
        return [
            '1X2',
            bet_name
        ]
    elif 'Обе команды забьют' in bet_name:
        return [
            'Обе забьют',
            bet_name.replace('Обе команды забьют: ', '')
        ]
    elif 'Двойной шанс' in bet_name:
        return [
            'Двойной шанс',
            bet_name.replace('Двойной шанс ', '')
        ]
    return None


if __name__ == '__main__':
    predicts1 = get_predicts(get_and_parse_url('https://vprognoze.ru/user/MoneyMachine/'))
    print(get_teams(predict=predicts1[0]))
    print(get_tournament(predict=predicts1[0]))
    print(is_started(predict=predicts1[0]))
    print(get_persent(predict=predicts1[0]))
    print(convert21x(bet_name=get_bet(predict=predicts1[0])))
