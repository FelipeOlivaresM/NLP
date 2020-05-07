import pandas as pd
import sys

# pip3 install -r requirements.txt <---- por si da flojera instalarlos a mano.


output_path1 = "./twitter_data/datos_en_bruto/catched_tweets_originales.csv"
output_path_m1 = "./twitter_data/datos_para_tageo_mourning/prefiltered_mourning.csv"
output_path_m2 = "./twitter_data/datos_para_tageo_mourning/prefiltered_not_mourning.csv"

df = pd.read_csv(output_path1, encoding='utf8', dtype=str, engine='python')

tags_muerte = [
    'mourning', ' rip ', 'rest in peace', 'glory of god', 'cry for the departure', 'luto', 'descansa en paz',
    'gloria de dios', 'lloran por la pertida', 'llorar por la partida', 'god be with you', 'que dios esté contigo',
    'sorry for your absence', 'lamento tu ausencia', 'no te preocupes por las lágrimas que derramas en su nombre',
    'lágrimas de dolor', 'tears of pain', 'rezo porque estés en el reino de dios',
    'i pray for you to be in the kingdom of god',
    'nos veremos de nuevo en el reino de dios',
    'i will see you again in the kingdom of god'
]

df_mourning = pd.DataFrame(columns=df.columns)
df_no_mourning = pd.DataFrame(columns=df.columns)

print("")
for i, row in df.iterrows():
    sys.stdout.write("\rProgreso: " + str(round(((i + 1) / (df.shape[0])) * 100, 4)) + "%")
    sys.stdout.flush()
    text = df.at[i, 'text']
    if any(word in text for word in tags_muerte):
        df_mourning = df_mourning.append(df.iloc[i])
    else:
        df_no_mourning = df_no_mourning.append(df.iloc[i])

print("")
del df

df_mourning.sort_values('id')
df_mourning.to_csv(output_path_m1, index=False, encoding="utf-8")
del df_mourning

df_no_mourning.sort_values('id')
df_no_mourning.to_csv(output_path_m2, index=False, encoding="utf-8")
del df_no_mourning
