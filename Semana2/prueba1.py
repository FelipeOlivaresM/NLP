"""Splitting text data into tokens."""
# Modificado de https://github.com/TianHuaBooks/Count/blob/master/count_words.py
import re
import numpy as np
import pandas as pd


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
    """Cuenta cuantas veces una palabra occure en el texto"""
    counts = dict()  # diccionario de pares { <word>: <count> }

    # Conversion a minuscula
    text = sent.lower()

    # Dividir el texto en tokens (palabras), quitando la puntuacion.
    # Usar expresiones regulares para dividr segun caracteres no-alfanumericos '\w'
    matchObjs = re.findall(r'[\w]+', text)
    print(matchObjs)
    # Conteo usando el diccionario.
    for obj in matchObjs:
        if obj in counts:
            counts[obj] += 1  # Adiciona 1 a una entrada existente
        else:
            counts[obj] = 1  # Crea un nuevo indice/palabra en el diccionario.
    
    return counts

def sumarnums(llave, valor):

    tablal = []
    tablav = []
    print(valor)
    print("\n Imprimir tablas \n")
    for ll in llave:
        tablal.append(ll)
    print("\n Llaves")
    print(tablal)

    for ll in valor:
        tablav.append(ll)
    print("\n Valor")
    print(tablav)
    tablal.extend(tablav)
    print ("Con metodo .extend()")
    print (tablal)
    
    for tablita in tablal:
        print("\n", tablita)

def test_run():
    """Called on Test Run."""
    with open("input.txt", "r") as f:
        text = f.read()
        # print("--- Sample text ---", text, sep="\n")

    sentences = sent_tokenize(text)
    print("\n--- Sentences ---")
    #print(sentences)
    cont = 1
    print("\n--- Words ---")
    for sent in sentences:
        print(".............................................................................................")
        print("\n")
        print("Libro # ", cont)
        print(sent)
        print("\n")
        #Diccionario con las palabras y el total de veces que aparecen
        word = word_tokenize(sent)
        #Se convierten los valores del diccionario a una lista.
        keys = word.keys()
        values = word.values()
        print("\n")
        print("TUPLAS")
        print(values)
        #Enviar lista para realizar calculos e imprimir primera tabla
        print("\n")
        tablaimpresa = sumarnums(keys,values)
    
        sorted_counts = sorted(word.items(), key=lambda pair: pair[1], reverse=True)
        print("\n")
        print(word)
        print("\n")
        print("10 most common words:\nWord\tCount")

        for word, count in sorted_counts[:10]:
            print("{}\t{}".format(word, count))

        print("\n10 least common words:\nWord\tCount")
        for word, count in sorted_counts[-10:]:
            print("{}\t{}".format(word, count))

        print("\n")
        print(sorted_counts)
        print()  # blank line for readability
        cont += 1


if __name__ == "__main__":
    test_run()
