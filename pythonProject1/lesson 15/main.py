import pandas as pd
import matplotib.pyplot as plt

df  = pd.read_csv('data1.csv')

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("your_file.csv")
df["date"] = pd.to_datetime(df["date"])

# 1. Overall average
print(f"Average temperature: {df['temperature'].mean():.2f}")

# 2. Monthly averages + bar plot
monthly = df.groupby(df["date"].dt.month)["temperature"].mean()
print(monthly)
monthly.plot(kind="bar")
plt.xlabel("Month")
plt.ylabel("Average temperature")
plt.title("Monthly Average Temperature")
plt.show()

# 3. Hottest and coldest days (entire rows)
print(df.loc[df["temperature"].idxmax()])
print(df.loc[df["temperature"].idxmin()])

# 4a. Line graph over time
df.plot(x="date", y="temperature", kind="line")
plt.title("Temperature Over Time")
plt.show()

# 4b. Seasonal averages
def season(m):
    if m in (12, 1, 2): return "Winter"
    if m in (3, 4, 5): return "Spring"
    if m in (6, 7, 8): return "Summer"
    return "Autumn"

df["season"] = df["date"].dt.month.map(season)
print(df.groupby("season")["temperature"].mean())

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("your_file.csv", skipinitialspace=True)
df.columns = df.columns.str.strip()

# Fix "(0.3)" -> -0.3 and make temperature numeric
df["temperature"] = (
    df["temperature"].astype(str).str.strip()
    .str.replace(r"^\((.*)\)$", r"-\1", regex=True)
    .astype(float)
)

# Build a real date from year + "month/day"
df["date"] = pd.to_datetime(df["year"].astype(str) + "/" + df["day"], format="%Y/%m/%d")

# 1. Overall average
print(f"Average temperature: {df['temperature'].mean():.2f}")

# 2. Monthly averages + bar plot
monthly = df.groupby(df["date"].dt.month)["temperature"].mean()
print(monthly.round(2))
monthly.plot(kind="bar", xlabel="Month", ylabel="Average temperature (°C)",
             title="Monthly Average Temperature")
plt.show()

# 3. Hottest and coldest days (entire rows)
print("Hottest:\n", df.loc[df["temperature"].idxmax()])
print("Coldest:\n", df.loc[df["temperature"].idxmin()])

# 4a. Line graph over time
df.plot(x="date", y="temperature", kind="line", legend=False,
        title="Temperature Over Time", ylabel="Temperature (°C)")
plt.show()

# 4b. Seasonal averages
seasons = {12: "Winter", 1: "Winter", 2: "Winter",
           3: "Spring", 4: "Spring", 5: "Spring",
           6: "Summer", 7: "Summer", 8: "Summer",
           9: "Autumn", 10: "Autumn", 11: "Autumn"}
df["season"] = df["date"].dt.month.map(seasons)
print(df.groupby("season")["temperature"].mean().round(2))