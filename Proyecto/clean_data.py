import re
import pandas as pd

output_path = "./twitter_data/catched_tweets_2.csv"
df = pd.read_csv(output_path)

for i, row in df.iterrows():
    df.at[i, 'text'] = re.sub(' +', ' ', re.sub(r"http\S+", "", str(row['text']).replace("\n", " "))).strip()

df.to_csv(output_path, index=False, encoding="utf-8")
