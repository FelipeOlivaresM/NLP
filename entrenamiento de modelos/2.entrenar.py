from cargar_df import get_mourning_df
import pandas as pd

df = pd.DataFrame(get_mourning_df(0, 1))
print(df.head())
