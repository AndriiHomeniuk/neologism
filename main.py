import urllib3

def get_file_from_site():
	'''
	This function help get file with some text from site and save this file on the server for next process.
	'''
	pass

def open_file():
	'''
	This function help open file with some text, that was saved on the server.
	'''
	pass

def get_text_from_site():
	'''
	This function help get some text from site and save this text on the server.
	'''
	text = text_from_site
	text = "Якийсь тестовий текст з сайту"
	return text

def text_to_list(text):
	'''
	This function help split text to list for next process.
	'''
	text_result = []
	for word in text.split(' '):
		if word:
			if not word[-1].isalpha():
				word = word[:-1]

			text_result.append(word.lower())
	return text_result

def search_words(text_result):
	'''
	This function search neologisms from the text on the vocabularies site and give list of neologisms.
	'''
	pass
	return list_of_neologisms

def list_to_file(list_of_neologisms):
	'''
	This function write list of neologisms to the file, that will be download by user.
	'''
	with open('neologism_file.txt', 'w') as neologism_file:
		neologism_file.write(list_of_neologisms) 

def give_file_to_site():
	'''
	This function return file with saved neologisms for donwloading.
	'''
	pass

def give_list_to_site(list_of_neologisms):
	'''
	This function help save neologisms, that was find to list of neologisms, and print this list to site.
	'''
	pass

if __name__ == '__main__':
	pass
