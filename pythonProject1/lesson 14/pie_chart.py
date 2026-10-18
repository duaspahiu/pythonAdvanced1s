import  pandas as pd

import  matplotlib.pyplot as plt

df = pd.read_csv("data1.csv")


average_iq_by = df.groupby("Continent")["Average IQ"].mean()

plt.figure(figsize=(10,6))

average_iq_by.plot(kind="line",marker='o', color='skyblue')


plt.title("Average Iq ")
plt.show()