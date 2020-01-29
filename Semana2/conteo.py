#Modificado de https://github.com/TianHuaBooks/Count/blob/master/count_words.py
import re

def count_words(text):
	"""Cuenta cuantas veces una palabra occure en el texto"""
	counts = dict()  # diccionario de pares { <word>: <count> } 
	
	# Conversion a minuscula
	text2 = text.lower()
	
	# Dividir el texto en tokens (palabras), quitando la puntuacion.
	# Usar expresiones regulares para dividr segun caracteres no-alfanumericos '\w'
	matchObjs = re.findall(r'[\w]+', text2)
	print(matchObjs)
	# Conteo usando el diccionario.
	for obj in matchObjs:
		if obj in counts:
			counts[obj] += 1 #Adiciona 1 a una entrada existente
		else:
			counts[obj] = 1 #Crea un nuevo indice/palabra en el diccionario.
	
	return counts


def test_run():
	with open("input.txt", "r") as f:
		text = f.read()
		counts = count_words(text)
		sorted_counts = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
		
		print("10 most common words:\nWord\tCount")
		for word, count in sorted_counts[:10]:
			print("{}\t{}".format(word, count))
		
		print("\n10 least common words:\nWord\tCount")
		for word, count in sorted_counts[-10:]:
			print("{}\t{}".format(word, count))


if __name__ == "__main__":
	test_run()