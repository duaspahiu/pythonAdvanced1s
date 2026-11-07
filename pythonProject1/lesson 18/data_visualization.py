import streamlit as st
import pandas as pd

from pythonProject1.perseritje.loops import names

books_df=pd.read_csv("bestsellers_with_categories_2022_03_27.csv")


st.title("bestselling books analysis")
st.write("this app analyzes the Amazon top Selling books from 2009 to 2022")

st.subheader("summary statisctic")
total_books = books_df.shape[0]
unique_titles = books_df['Name'].nunique()
average_rating =books_df['User Rating'].mean()
average_price =books_df['Price'].mean()

col1, col2, col3,col4 = st.columns(4)

col1.metric("total books",total_books)
col1.metric("unique books",unique_titles)
col1.metric("AVG",f"{average_rating:.2f}")
col1.metric("AVG price",f"{average_price:}")

st.subheader("dataset preview")
st.write(books_df())

col1,col2 = st.columns(2)

with co11:
    st.header("top 10 authors")
    top_authors = books_df['author'].value_counts().head(10)
    st.bar_chart(top_authors)

with col2:
    st.header("top 10 titles")
    top_titles = books_df['Name'].value.counts().head(10)
    st.bar_chart(top_titles)

st.subheader("Genre Distribution")
fig = px.pie(books_df,names="Genre",title="most liked genre( 2009-2022")",color="Genre",
            color_discrete_sequence=px.colors.seqential.plasma),
st.ploty_chart(fig)

st.subheader("Number of fiction vs non fiction books over the years")
size = books_df.groupby(['year','Genre']).size().reset_index(name="Counts")
fig2 = px.bar(size, x="Year",y="Genre",color="Genre",
              color_discrete_sequence=px.colors.
st.ploty_chart(fig2)

st.subheader("top 15 authors counts of books published")
top_authors
top_authors.colums = []
