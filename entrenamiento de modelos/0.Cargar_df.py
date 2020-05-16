import pandas as pd
from os import walk
import os


def get_mourning_df(create_new_file):
    mourning_folder = './datos mourning'
    mourning_df_path = mourning_folder + '/dataset listo/mourning_full_df.csv'
    mourning_df = pd.DataFrame(columns=['text', 'lang', 'mourning'])
    if create_new_file == 0 and os.path.exists(mourning_df_path) == True:
        mourning_df = pd.read_csv(mourning_df_path, encoding='utf8', dtype=str, engine='python')
    elif create_new_file == 1 or os.path.exists(mourning_df_path) == False:
        path, subfolders, files_list = list(walk(mourning_folder))[0]
        for file in files_list:
            file_name, file_ext = file.split(".")
            if file_ext == 'csv':
                file_path = path + "/" + file_name + "." + file_ext
                df = pd.read_csv(file_path, encoding='utf8', dtype=str, engine='python')
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

    mourning_df.drop_duplicates(subset=['text'], inplace=True)
    mourning_df.to_csv(mourning_df_path, index=False, encoding="utf-8")
    return mourning_df


get_mourning_df(1)
