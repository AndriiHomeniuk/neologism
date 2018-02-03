# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import urllib.error
import sqlite3


TRANSLIT = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "h",
    "ґ": "g",
    "д": "d",
    "е": "e",
    "є": "ie",
    "ж": "zh",
    "з": "z",
    "и": "y",
    "і": "i",
    "ї": "i",
    "й": "i",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ю": "iu",
    "я": "ia",
    "ь": "j"
}


def get_file_from_site():
    """
    This function help get file with some text from site and save this file on the server for next process.
    """
    pass


def open_file():
    """
    This function help open file with some text, that was saved on the server.
    """
    pass


def text_to_list(text):
    """
    This function help split text to list for next process.
    """
    text_list = []
    for word in text.split(' '):
        if word:
            if not word[-1].isalpha():
                word = word[:-1]
            text_list.append(word.lower())
    return list(set(text_list))


def search_words_own_vocabulary(text_list):
    """
    This function search neologisms from the text on the own vocabularies and give list of neologisms.
    """
    pre_list_of_neologisms = []
    vocabulary = sqlite3.connect("voc.db")
    voc = vocabulary.cursor()
    for words in text_list:
        voc.execute("SELECT word FROM voc WHERE word='%s'" % words)
        result = voc.fetchall()
        if not result:
            pre_list_of_neologisms.append(words)
        elif words not in result[0][0]:
            pre_list_of_neologisms.append(words)
    voc.close()
    vocabulary.close()
    return pre_list_of_neologisms


def search_words_orthographic_vocabulary(text):
    """
    This function search neologisms from the text on the vocabularies site and give list of neologisms.
    """
    list_of_neologisms = []
    for word in text:
        page = urllib.request.urlopen("http://slovnyk.ua/?swrd={}".format(quote(word))).read()
        soup = BeautifulSoup((page), 'html.parser')
        if not soup.find_all('table', class_='sfm_table'):
            list_of_neologisms.append(word)
    return list_of_neologisms


def search_words_interpretative_vocabulary(text):
    """
    This function search neologisms from the text on the vocabularies site and give list of neologisms.
    """
    list_of_neologisms = []
    for word in text:
        translit = ""
        for letter in word:
             translit += TRANSLIT[letter]
        page = urllib.request.urlopen("http://sum.in.ua/s/{}".format(quote(translit))).read()
        soup = BeautifulSoup((page), 'html.parser')
        if soup.find_all('div', id='search-res'):
            list_of_neologisms.append(word)
    return list_of_neologisms


def search_words_internet_vocabulary(text):
    """
    This function search neologisms from the text on the vocabularies site and give list of neologisms.
    """
    list_of_neologisms = []
    for word in text:
        try:
            page = urllib.request.urlopen("http://ukrlit.org/slovnyk/{}".format(quote(word))).read()
            soup = BeautifulSoup((page), 'html.parser')
            if soup.find_all('div', class_='main slovnik'):
                continue
        except urllib.error.HTTPError as err:
            if err.code == 404:
                pass
        list_of_neologisms.append(word)
    return list_of_neologisms


def list_to_file(list_of_neologisms): # done
    """
    This function write list of neologisms to the file, that will be download by user.
    """
    with open('neologism_file.txt', 'a', encoding="UTF-8") as neologism_file:
        neologism_file.write(str(list_of_neologisms))


def give_file_to_site():
    """
    This function return file with saved neologisms for donwloading.
    """
    pass


def process(text):
    """
    This function, finally, search neologisms from the text and return list of neologisms in the end.
    """
    first_text = text_to_list(text)
    pre_word_list = search_words_own_vocabulary(first_text)
    word_list = search_words_orthographic_vocabulary(pre_word_list)
    word_list_two = search_words_interpretative_vocabulary(word_list)
    word_list_three = search_words_internet_vocabulary(word_list_two)
    return word_list_three

