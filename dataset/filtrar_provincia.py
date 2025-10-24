import pandas as pd


nombre_provincia = "Alacant/Alicante"
df = pd.read_csv("accesibility_data/0802_AccesEdificiosPub.csv")

df_alicante = df[df["provincia"] == nombre_provincia]
df_alicante.to_csv("accesibility_data/alicante.csv", index=False)