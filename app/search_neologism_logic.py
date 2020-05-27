# -*- coding: utf-8 -*-
import re
import sqlite3
import urllib.error
import urllib.request
from urllib.parse import quote

from bs4 import BeautifulSoup

TRANSLIT = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'h',
    'ґ': 'g',
    'д': 'd',
    'е': 'e',
    'є': 'ie',
    'ж': 'zh',
    'з': 'z',
    'и': 'y',
    'і': 'i',
    'ї': 'i',
    'й': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ю': 'iu',
    'я': 'ia',
    'ь': 'j'
}


def text_to_list(text):
    return list(set(re.findall(r'\w+', text)))


def upload_to_app_db(new_words):
    with sqlite3.connect('../voc.db') as vocabulary:
        voc = vocabulary.cursor()
        for word in new_words:
            voc.execute("INSERT INTO voc (word) VALUES ('%s');" % word)
        voc.close()
    return True


def search_words_own_vocabulary(text_list):
    """
    This function search neologisms from the text on the own vocabularies and give list of neologisms.
    """
    pre_list_of_neologisms = []
    with sqlite3.connect('../voc.db') as vocabulary:
        voc = vocabulary.cursor()
        voc.execute("CREATE TABLE IF NOT EXISTS [voc] ([id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, [word] STRING);")
        for word in text_list:
            voc.execute("SELECT word FROM voc WHERE word='%s';" % word)
            result = voc.fetchall()
            if not result or word not in result[0][0]:
                pre_list_of_neologisms.append(word)
        voc.close()
    return pre_list_of_neologisms


def search_words_orthographic_vocabulary(text):
    """
    This function search neologisms from the text on the vocabularies site and give list of neologisms.
    """
    for word in text:
        page = urllib.request.urlopen('http://slovnyk.ua/?swrd={}'.format(quote(word))).read()
        soup = BeautifulSoup(page, 'html.parser')
        if not soup.find_all('div', class_='toggle-content'):
            yield word


def search_words_interpretative_vocabulary(text):
    """
    This function search neologisms from the text on the vocabularies site and give list of neologisms.
    """
    for word in text:
        translit = ''.join(TRANSLIT[letter] for letter in word)
        page = urllib.request.urlopen('http://sum.in.ua/s/{}'.format(quote(translit))).read()
        soup = BeautifulSoup(page, 'html.parser')
        if soup.find_all('div', id='search-res'):
            yield word


def search_words_internet_vocabulary(text):
    """
    This function search neologisms from the text on the vocabularies site and give list of neologisms.
    """
    for word in text:
        try:
            page = urllib.request.urlopen('http://ukrlit.org/slovnyk/{}'.format(quote(word))).read()
            soup = BeautifulSoup(page, 'html.parser')
            if soup.find_all('div', class_='main slovnik'):
                continue

        except urllib.error.HTTPError as err:
            if err.code == 404:
                pass

        yield word


def process(text):
    """
    This function, finally, search neologisms from the text and return list of neologisms in the end.
    """
    first_text = text_to_list(text)
    pre_word_list = search_words_own_vocabulary(first_text)
    word_list = search_words_orthographic_vocabulary(pre_word_list)
    word_list_two = search_words_interpretative_vocabulary(word_list)
    result = list(search_words_internet_vocabulary(word_list_two))
    upload_to_app_db(list(set(pre_word_list).symmetric_difference(result)))
    return result
