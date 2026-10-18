import pandas as pd

import matplotlib.pyplot as plt

df = pd.read_csv("data1.csv")


nobel_prizes_By_continent = df.groupby("continent")["nobel prices"].sum()

no_of_continents = nobel_prizes_By_continent.count()

print(no_of_continents)

colors = ["gold","lightcoral","yellow","thistle","orange","lightskyblue","aquamrine","burlywood"]

plt.figure(figisize=(10,10))


nobel_prizes_By_continent.plot(kind="pie",colors=colors, autopct='%1.1f%%')
plt.title("Distribution of nobel prizes by continent")
plt.show()