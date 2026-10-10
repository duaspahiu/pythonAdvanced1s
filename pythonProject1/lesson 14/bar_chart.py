import pandas as pd
import matplotib.pyplot as plt

df  = pd.read_csv('data1.csv')

filtred_df = df[df["Average IQ"]>=100]

filtred_df = filtred_df.sort_values(by="Average IQ",ascending=false)

print(filtred_df)

plt.figure(figsize=(14,8))



bars = plt.bar(filtred_df["Country"],color="skyblue")

plt.tittle("Average IQ by Country")

plt.show()
