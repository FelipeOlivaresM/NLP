"""Splitting text data into tokens."""
# Modificado de https://github.com/TianHuaBooks/Count/blob/master/count_words.py
import re
import numpy as np
import pandas as pd 
import math as mt

counts = dict()  # diccionario de pares { <word>: <count> }
cantwordbo = [] #Cantidad de palabras por libro
numdocs = dict() #Numero de docs que tiene la palabras
idf = dict() #IDF
tfidf = dict() #TFIDF
vocabulario = [] #WORDS

def sent_tokenize(text):
    """Split text into sentences."""

    # Split text by sentence delimiters (remove delimiters)
    sentenses = re.split(r"[\n|\r]", text)

    #print("# of lines:{}".format(len(sentenses)))

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
    

    # Conversion a minuscula
    text = sent.lower()
    palabras_libro=dict()
    
    # Dividir el texto en tokens (palabras), quitando la puntuacion.
    # Usar expresiones regulares para dividr segun caracteres no-alfanumericos '\w'
    matchObjs = re.findall(r'[\w]+', text)
    
    n_palabras=len(matchObjs)
    
    #print(matchObjs)
    # Conteo usando el diccionario.
    for obj in matchObjs:
        if obj in counts:
            counts[obj] += 1  # Adiciona 1 a una entrada existente
        else:
            counts[obj] = 1  # Crea un nuevo indice/palabra en el diccionario.
            vocabulario.append(obj)
            
            
        if obj in palabras_libro: # Frecuencia en el texto
            palabras_libro[obj] += 1  # Adiciona 1 a una entrada existente
        else:
            palabras_libro[obj] = 1  # Crea un nuevo indice/palabra en el diccionario.
            if obj in numdocs: # Obtencion de parametro df  
                numdocs[obj] += 1  # Adiciona 1 a una entrada existente
            else:
                numdocs[obj] = 1  # Crea un nuevo indice/palabra en el diccionario.
    
    for k in palabras_libro:
        palabras_libro[k]=palabras_libro.get(k)/n_palabras
    cantwordbo.append(palabras_libro)
    print("Frecuencia TF")
    print(palabras_libro)
    print("\n")
    print("DF")    
    print(numdocs) 
    print("DF")    
    
    return counts

def Calcular_idf(num_libros):
    # Recorrer Dicionario para actualizar parametro IDF
    tam = len(cantwordbo)
    print("TAMAÑO")
    print(tam)
    dict2 = cantwordbo[0]
    print(dict2)
    var = dict2.get('amazon') * 2
    print(var)
    print 
    """ for i in range(tam):
        for palabra in vocabulario:
            idf[palabra]= mt.log(num_libros/numdocs.get(palabra))
            dict2 = cantwordbo[i]
            tfidf[palabra]= dict2.get(palabra)*(mt.log(num_libros/numdocs.get(palabra))) """
    for palabra in vocabulario:
        idf[palabra]= mt.log(num_libros/numdocs.get(palabra))
        tfidf[palabra]= var * (mt.log(num_libros/numdocs.get(palabra)))
        
    print("\n IDF")
    print("\n")
    ordenamientoidf = sorted(idf.items(), key=lambda pair: pair[1], reverse=True)
    WORDS = list(idf.keys())
    DFL = list(numdocs.values())
    IDFL = list(idf.values())
    TFIDFL = list(tfidf.values())
    
    print("LISTA")
    print(idf)
    print("\n")
    print(cantwordbo[2])
    
    #print(ordenamiento)    
    print("Words")
    for i in range(len(ordenamientoidf)):
        print("{0:15s} {1:3f} {2:3f} {3:3f}".format(WORDS[i], DFL[i], IDFL[i], TFIDFL[i]))

    

def test_run():
    """Called on Test Run."""
    with open("mycorpus.txt", "r") as f:
        text = f.read()
        # print("--- Sample text ---", text, sep="\n")

    sentences = sent_tokenize(text)
    num_libros=len(sentences)
    print("\n--- Sentences ---")
    
    #print(sentences)
    cont = 1
    print("\n--- Words ---")
    for sent in sentences:
        print(".............................................................................................")
        print("\n")
        print("Libro # ", cont)
        #print(sent)
        print("\n")
        #Diccionario con las palabras y el total de veces que aparecen
        word_tokenize(sent)
        #Se convierten los valores del diccionario a una lista.
        print("\n")
        #print(values)
        #Enviar lista para realizar calculos e imprimir primera tabla
        print("\n")
        #print(word)
        #print(sorted_counts)
        cont += 1
        
    Calcular_idf(num_libros)
    #print("VOCABULARIO")
    #for i in vocabulario:
    #    print(i)

if __name__ == "__main__":
    test_run()
