# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import urllib.error
import io


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


def get_text_from_site():
    """
    This function help get some text from site and save this text on the server.
    """
    # text = text_from_site
    text = "Гарне вікно в буржуазії хоча алюр кричить безіре"
    return text


def text_to_list(text): # done
    """
    This function help split text to list for next process.
    """
    text_list = []
    for word in text.split(' '):
        if word:
            if not word[-1].isalpha():
                word = word[:-1]
            text_list.append(word.lower())
    return text_list


def search_words_own_vocabulary(text_list): # done
    """
    This function search neologisms from the text on the own vocabularies and give list of neologisms.
    """
    pre_list_of_neologisms = []
    with io.open('o_voc.txt', 'r', encoding="UTF-8") as file:
        file = file.readlines()
        for word in file:
            file_text = word.split()
        for word in text_list:
            if word not in file_text:
                pre_list_of_neologisms.append(word)
                file_text.append(word)
    return pre_list_of_neologisms


def search_words_orthographic_vocabulary(pre_list_of_neologisms): # done
    """
    This function search neologisms from the text on the vocabularies site and give list of neologisms.
    """
    first_list_of_neologisms = []
    for word in pre_list_of_neologisms:
        page = urllib.request.urlopen("http://slovnyk.ua/?swrd={}".format(quote(word))).read()
        soup = BeautifulSoup((page), 'html.parser')
        if not soup.find_all('table', class_='sfm_table'):
            first_list_of_neologisms.append(word)
    return first_list_of_neologisms


def search_words_interpretative_vocabulary(first_list_of_neologisms): # done
    """
    This function search neologisms from the text on the vocabularies site and give list of neologisms.
    """
    second_list_of_neologisms = []
    for word in first_list_of_neologisms:
        translit = ""
        for letter in word:
             translit += TRANSLIT[letter]
        page = urllib.request.urlopen("http://sum.in.ua/s/{}".format(quote(translit))).read()
        soup = BeautifulSoup((page), 'html.parser')
        if soup.find_all('div', id='search-res'):
            second_list_of_neologisms.append(word)
    return second_list_of_neologisms


def search_words_internet_vocabulary(second_list_of_neologisms): # done
    """
    This function search neologisms from the text on the vocabularies site and give list of neologisms.
    """
    list_of_neologisms = []
    for word in second_list_of_neologisms:
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


def searching_words(text_list):
    """
    This function search neologisms and append all lists of neologisms to one final list
    """
    # final_list_of_neologisms = []
    # checker = 0
    # while checker <= len(text_list):
    #     for word in text_list:
    #
    # search_words_own_vocabulary()
    # search_words_orthographic_vocabulary()
    # search_words_interpretative_vocabulary()
    # search_words_internet_vocabulary()
    #
    # return final_list_of_neologisms


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


def give_list_to_site(list_of_neologisms):
    """
    This function help save neologisms, that was find to list of neologisms, and print this list to site.
    """
    pass


if __name__ == '__main__':
    text = "Гарне вікно в буржуазії, хоча алюр кричить безіре"
    first_text = text_to_list(text)
    pre_word_list = search_words_own_vocabulary(first_text)
    word_list = search_words_orthographic_vocabulary(pre_word_list)
    word_list_two = search_words_interpretative_vocabulary(word_list)
    word_list_three = search_words_internet_vocabulary(word_list_two)
    # list_to_file(word_list_three)
    print(word_list_three)
