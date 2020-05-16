# -----------------------------------------------------------------------------
# create_new_file: 0 para usar un archivo existente si es posible
# o 1 para crear de nuevo
# balance_data: 0 para retornar dataframe sin balancear o 1 para retornar
# dataframe balanceado.
# -----------------------------------------------------------------------------
def get_mourning_df(create_new_file, balance_data):
    from sklearn.utils import resample
    import os, re, sys, pandas
    mourning_folder = './datos mourning'
    mourning_df_path = mourning_folder + '/dataset listo/mourning_full_df.csv'
    mourning_df = pandas.DataFrame(columns=['text', 'lang', 'mourning'])
    print("")
    if create_new_file == 0 and os.path.exists(mourning_df_path) == True:
        print('Cargando datos')
        mourning_df = pandas.read_csv(mourning_df_path, encoding='utf8', dtype=str, engine='python')
    elif create_new_file == 1 or os.path.exists(mourning_df_path) == False:
        path, subfolders, files_list = list(os.walk(mourning_folder))[0]
        for i in range(len(files_list)):
            sys.stdout.write(
                "\rPreparando dataframe " + str(round(((i + 1) / (len(files_list))) * 100, 2)) + "%")
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
                elif numero_de_archivo == 3:
                    df = df.filter(['text', 'lang', 'tag'])
                    df.columns = ['text', 'lang', 'mourning']
                    df['mourning'] = df.mourning.map({'no mourning': '0', 'mourning': '1'})
                    mourning_df = mourning_df.append(df)
                elif numero_de_archivo == 4:
                    df = df.filter(['tweet', 'lang', 'mourning'])
                    df.columns = ['text', 'lang', 'mourning']
                    df['mourning'] = df.mourning.map({'no mourning': '0', 'mourning': '1'})
                    mourning_df = mourning_df.append(df)
            elif file_ext == 'json':
                file_path = path + "/" + file_name + "." + file_ext
                numero_de_archivo = file_name.split("_")[0]
                if numero_de_archivo == 1 or numero_de_archivo == 2:
                    pass
                elif numero_de_archivo == 3:
                    pass
                elif numero_de_archivo == 4:
                    pass
        print("")
        mourning_df.reset_index(drop=True, inplace=True)
        for i, row in mourning_df.iterrows():
            sys.stdout.write(
                "\rNormalizacion de datos completada al " + str(
                    round(((i + 1) / (mourning_df.shape[0])) * 100, 2)
                ) + "%"
            )
            sys.stdout.flush()
            mourning_df.at[i, 'text'] = (re.sub(
                ' +', ' ', re.sub("http\S+", "", str(mourning_df.at[i, 'text']).replace("\n", " "))
            )).strip()
        print("")
    mourning_df.drop_duplicates(subset=['text'], inplace=True)
    if balance_data == 1:
        print("Balanceando datos")
        min_len1 = int(min(mourning_df['mourning'].value_counts()))
        df_0 = resample(mourning_df[mourning_df.mourning == '0'], replace=False, n_samples=min_len1, random_state=1)
        df_1 = resample(mourning_df[mourning_df.mourning == '1'], replace=False, n_samples=min_len1, random_state=1)
        mourning_df = pandas.concat([df_0, df_1])
        mourning_df = mourning_df.loc[mourning_df['lang'].isin(['es', 'en'])]
        min_len2 = int(min(mourning_df['lang'].value_counts()))
        df_2 = resample(mourning_df[mourning_df.lang == 'en'], replace=False, n_samples=min_len2, random_state=1)
        df_3 = resample(mourning_df[mourning_df.lang == 'es'], replace=False, n_samples=min_len2, random_state=1)
        mourning_df = pandas.concat([df_2, df_3])
        mourning_df.sort_values('lang', inplace=True)
        mourning_df.to_csv(mourning_df_path, index=False, encoding="utf-8")
        print("Datos entrgados")
        return mourning_df
    elif balance_data == 0:
        mourning_df.to_csv(mourning_df_path, index=False, encoding="utf-8")
        print("Datos entrgados")
        return mourning_df
