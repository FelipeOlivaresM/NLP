# -----------------------------------------------------------------------------
# balance_data: 0 para retornar dataframe sin balancear o 1 para retornar
# dataframe balanceado.
# lematizacion: lematiza los textos usando nltk 0 para no lematizar y 1
# para retornar el texto lematizado.
# -----------------------------------------------------------------------------
def get_mourning_df(balance_data, lematizacion):
    from gensim.utils import any2unicode as unicode
    from nltk.stem import SnowballStemmer
    from sklearn.utils import resample
    import os, re, sys, pandas, unidecode

    mourning_folder = './datos mourning'
    mourning_df = pandas.DataFrame(columns=['text', 'lang', 'mourning'])
    path, subfolders, files_list = list(os.walk(mourning_folder))[0]
    files_list.sort()

    for i in range(len(files_list)):
        sys.stdout.write("\rPreparando df " + str(round(((i + 1) / (len(files_list))) * 100, 2)) + "%")
        sys.stdout.flush()
        file_name, file_ext = files_list[i].split(".")

        if file_ext == 'csv':
            file_path = path + "/" + file_name + "." + file_ext
            df = pandas.read_csv(file_path, encoding='utf8', dtype=str, engine='python')
            numero_de_archivo = int(file_name.split("_")[0])

            if numero_de_archivo == 1 or numero_de_archivo == 2:
                df = df.filter(['text', 'lang', 'mourning'])
                df['mourning'] = df.mourning.map({'4': '0', '1': '1'})
                mourning_df = mourning_df.append(df)

            if numero_de_archivo == 3:
                df = df.filter(['text', 'lang', 'tag'])
                df.columns = ['text', 'lang', 'mourning']
                df['mourning'] = df.mourning.map({'no mourning': '0', 'mourning': '1'})
                mourning_df = mourning_df.append(df)

            if numero_de_archivo == 4:
                df = df.filter(['tweet', 'lang', 'mourning'])
                df.columns = ['text', 'lang', 'mourning']
                df['mourning'] = df.mourning.map({'no mourning': '0', 'mourning': '1'})
                mourning_df = mourning_df.append(df)

    del df
    print("")
    mourning_df.dropna()
    mourning_df.drop_duplicates(subset=['text'], inplace=True)
    mourning_df = mourning_df.loc[mourning_df['mourning'].isin(['1', '0'])]
    mourning_df = mourning_df.loc[mourning_df['lang'].isin(['es', 'en'])]
    mourning_df.reset_index(drop=True, inplace=True)

    for i, row in mourning_df.iterrows():
        sys.stdout.write("\rNormalizando df " + str(round(((i + 1) / (mourning_df.shape[0])) * 100, 2)) + "%")
        sys.stdout.flush()
        mourning_df.at[i, 'text'] = (
            re.sub(' +', ' ', re.sub("http\S+", "", re.sub('\s+', ' ', str(mourning_df.at[i, 'text']))))
        ).strip()

    print("")

    if balance_data == 1:
        mourning_df["Sello"] = 0
        for i, row in mourning_df.iterrows():
            sys.stdout.write(
                "\rCreando sellos de balanceamiento " +
                str(round(((i + 1) / (mourning_df.shape[0])) * 100, 2))
                + "%"
            )
            sys.stdout.flush()
            mourning_df.at[i, 'sello'] = str(mourning_df.at[i, 'lang']) + '_' + str(mourning_df.at[i, 'mourning'])
        print("\nBalanceando df")
        min_len1 = int(min(mourning_df['sello'].value_counts()))
        df_0 = resample(mourning_df[mourning_df.sello == 'es_0'], replace=False, n_samples=min_len1, random_state=1)
        df_1 = resample(mourning_df[mourning_df.sello == 'es_1'], replace=False, n_samples=min_len1, random_state=1)
        df_2 = resample(mourning_df[mourning_df.sello == 'en_0'], replace=False, n_samples=min_len1, random_state=1)
        df_3 = resample(mourning_df[mourning_df.sello == 'en_1'], replace=False, n_samples=min_len1, random_state=1)
        mourning_df = pandas.concat([df_0, df_1, df_2, df_3])
        mourning_df = mourning_df.filter(['text', 'lang', 'mourning'])
        mourning_df.reset_index(drop=True, inplace=True)

    if lematizacion == 1:
        stemmer_en = SnowballStemmer('english')
        stemmer_es = SnowballStemmer('spanish')
        for i, row in mourning_df.iterrows():
            sys.stdout.write(
                "\rLematizando df " + str(round(((i + 1) / (mourning_df.shape[0])) * 100, 2)) + "%"
            )
            sys.stdout.flush()
            if mourning_df.at[i, 'text'] is str and mourning_df.at[i, 'lang'] == 'es':
                mourning_df.at[i, 'text'] = stemmer_es.stem(unidecode.unidecode(
                    unicode(mourning_df.at[i, 'text'].lower(), "utf-8"))
                )
            elif mourning_df.at[i, 'text'] is str and mourning_df.at[i, 'lang'] == 'en':
                mourning_df.at[i, 'text'] = stemmer_en.stem(unidecode.unidecode(
                    unicode(mourning_df.at[i, 'text'].lower(), "utf-8"))
                )
        mourning_df.reset_index(drop=True, inplace=True)
        print("")

    print("Df mourning entregado\n")
    mourning_df.reset_index(drop=True, inplace=True)
    return mourning_df


# -----------------------------------------------------------------------------
# balance_data: 0 para retornar dataframe sin balancear o 1 para retornar
# dataframe balanceado.
# lematizacion: lematiza los textos usando nltk 0 para no lematizar y 1
# para retornar el texto lematizado.
# -----------------------------------------------------------------------------
def get_feelings_df(balance_data, lematizacion):
    from gensim.utils import any2unicode as unicode
    from nltk.stem import SnowballStemmer
    from sklearn.utils import resample
    import os, re, sys, pandas, unidecode

    feelings_folder = './datos sentimientos'
    feelings_df = pandas.DataFrame(columns=['text', 'lang', 'sentiment'])
    path, subfolders, files_list = list(os.walk(feelings_folder))[0]
    files_list.sort()

    for i in range(len(files_list)):
        sys.stdout.write("\rPreparando df  " + str(round(((i + 1) / (len(files_list))) * 100, 2)) + "%")
        sys.stdout.flush()
        file_name, file_ext = files_list[i].split(".")

        if file_ext == 'csv':
            file_path = path + "/" + file_name + "." + file_ext
            df = pandas.read_csv(file_path, encoding='utf8', dtype=str, engine='python')
            numero_de_archivo = int(file_name.split("_")[0])

            if numero_de_archivo == 1:
                df = df.filter(['airline_sentiment', 'text'])
                df.columns = ['sentiment', 'text']
                df['lang'] = 'en'
                df['sentiment'] = df.sentiment.map({'positive': '0', 'negative': '1', 'neutral': '2'})
                feelings_df = feelings_df.append(df)

            if numero_de_archivo == 2 or numero_de_archivo == 3 or numero_de_archivo == 4:
                df = df.filter(['sentiment', 'text'])
                df['lang'] = 'en'
                df['sentiment'] = df.sentiment.map({'positive': '0', 'negative': '1', 'neutral': '2'})
                feelings_df = feelings_df.append(df)

            if numero_de_archivo == 5 or numero_de_archivo == 6 or numero_de_archivo == 7:
                df = df.filter(['polarity', 'text'])
                df.columns = ['sentiment', 'text']
                if numero_de_archivo in [5, 6]: df['lang'] = 'es'
                if numero_de_archivo == 7: df['lang'] = 'en'
                df['sentiment'] = df.sentiment.map({'positive': '0', 'negative': '1', 'neutral': '2'})
                feelings_df = feelings_df.append(df)

            if numero_de_archivo == 8:
                df = df.filter(['sentiment', 'text'])
                df.columns = ['sentiment', 'text']
                df['lang'] = 'es'
                df['sentiment'] = df.sentiment.map({'positive': '0', 'negative': '1', 'neutral': '2'})
                feelings_df = feelings_df.append(df)

    del df
    print("")
    feelings_df.dropna()
    feelings_df.drop_duplicates(subset=['text'], inplace=True)
    feelings_df = feelings_df.loc[feelings_df['sentiment'].isin(['0', '1', '2'])]
    feelings_df = feelings_df.loc[feelings_df['lang'].isin(['es', 'en'])]
    feelings_df.reset_index(drop=True, inplace=True)

    for i, row in feelings_df.iterrows():
        sys.stdout.write("\rNormalizando df " + str(round(((i + 1) / (feelings_df.shape[0])) * 100, 2)) + "%")
        sys.stdout.flush()
        feelings_df.at[i, 'text'] = (
            re.sub(' +', ' ', re.sub("http\S+", "", re.sub('\s+', ' ', str(feelings_df.at[i, 'text']))))
        ).strip()

    print("")

    if balance_data == 1:
        feelings_df.dropna()
        feelings_df["Sello"] = 0
        for i, row in feelings_df.iterrows():
            sys.stdout.write(
                "\rCreando sellos de balanceamiento " +
                str(round(((i + 1) / (feelings_df.shape[0])) * 100, 2))
                + "%"
            )
            sys.stdout.flush()
            feelings_df.at[i, 'sello'] = str(feelings_df.at[i, 'lang']) + '_' + str(feelings_df.at[i, 'sentiment'])
        print("\nBalanceando df")
        min_len1 = int(min(feelings_df['sello'].value_counts()))
        df_0 = resample(feelings_df[feelings_df.sello == 'en_0'], replace=False, n_samples=min_len1, random_state=1)
        df_1 = resample(feelings_df[feelings_df.sello == 'en_1'], replace=False, n_samples=min_len1, random_state=1)
        df_2 = resample(feelings_df[feelings_df.sello == 'en_2'], replace=False, n_samples=min_len1, random_state=1)
        df_3 = resample(feelings_df[feelings_df.sello == 'es_0'], replace=False, n_samples=min_len1, random_state=1)
        df_4 = resample(feelings_df[feelings_df.sello == 'es_1'], replace=False, n_samples=min_len1, random_state=1)
        df_5 = resample(feelings_df[feelings_df.sello == 'es_2'], replace=False, n_samples=min_len1, random_state=1)
        feelings_df = pandas.concat([df_0, df_1, df_2, df_3, df_4, df_5])
        feelings_df = feelings_df.filter(['text', 'lang', 'sentiment'])
        feelings_df.reset_index(drop=True, inplace=True)

    if lematizacion == 1:
        stemmer_en = SnowballStemmer('english')
        stemmer_es = SnowballStemmer('spanish')
        for i, row in feelings_df.iterrows():
            sys.stdout.write("\rLematizando df " + str(round(((i + 1) / (feelings_df.shape[0])) * 100, 2)) + "%")
            sys.stdout.flush()
            if feelings_df.at[i, 'text'] is str and feelings_df.at[i, 'lang'] == 'es':
                feelings_df.at[i, 'text'] = stemmer_es.stem(unidecode.unidecode(
                    unicode(feelings_df.at[i, 'text'].lower(), "utf-8"))
                )
            elif feelings_df.at[i, 'text'] is str and feelings_df.at[i, 'lang'] == 'en':
                feelings_df.at[i, 'text'] = stemmer_en.stem(unidecode.unidecode(
                    unicode(feelings_df.at[i, 'text'].lower(), "utf-8"))
                )
        feelings_df.reset_index(drop=True, inplace=True)
        print("")

    print("Df sentiments entregado\n")
    feelings_df.reset_index(drop=True, inplace=True)
    return feelings_df
