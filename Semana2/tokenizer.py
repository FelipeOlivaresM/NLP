"""Splitting text data into tokens."""
#Modificado de https://github.com/TianHuaBooks/Count/blob/master/count_words.py
import re

def sent_tokenize(text):
	"""Split text into sentences."""
		
	# Split text by sentence delimiters (remove delimiters)
	sentenses = re.split(r"[\n|\r]", text)
	
	print("# of lines:{}".format(len(sentenses)))
	
	# Remove leading and trailing spaces from each sentence
	results = []
	for sen in sentenses:
		s = sen.strip()
		if len(s):
			results.append(s)
			
	return results

def word_tokenize(sent):
	"""Split a sentence into words."""
	
	# Split sent by word delimiters (remove delimiters)
	words = re.findall(r"[\w]+", sent)
	
	return  words



def test_run():
	"""Called on Test Run."""
	with open("input.txt", "r") as f:
		text = f.read()
		print("--- Sample text ---", text, sep="\n")
	
	sentences = sent_tokenize(text)
	print("\n--- Sentences ---")
	print(sentences)
	
	print("\n--- Words ---")
	for sent in sentences:
		print(sent)
		print(word_tokenize(sent))
		print()  # blank line for readability
		
if __name__ == "__main__":
	test_run()