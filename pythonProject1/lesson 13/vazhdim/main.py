import pandas as pd

df = pd.read_ecv('data1.csv')


print(df.info())

# na shfaq 5 rreshat e pare
print(df.head())


country_data=df['Country']

print(country_data)


subset = df[['Country','average IQ']]

print(subset)


filtred_df = subset[subset['average IQ']<100]
print(filtred_df)

null_mask = df.insull()

nul_count = null_mask.sum()

print(null_count)


df.dropna(inplace=true)
print(df.info())
print("-------------------")
duplicated_count = df.duplicated().sum()
print(duplicated_count)


average_iq_continent = df.groupby('contunent')['average IQ'].mean()

print(average_iq_continent)

sordetd_avg_by_continent = average_iq_continent.sort_values(ascending=false)

print(sordetd_avg_by_continent)

total_nobal_by_country=df.groupby('country')['nobal prices'].sum()

print(total_nobal_by_country)

soretd_total_nobel_by_country = total_nobal_by_country.sort_values(ascending=false)

print(sordetd_total_nobel_by_country)

sorted = sorted_total_nobal_by_contry[sordetd_total_nobel_by_country !=0]

print(sorted)