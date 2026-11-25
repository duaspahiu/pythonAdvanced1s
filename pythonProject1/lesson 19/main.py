
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="Best Selling Books",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------
# CONNECT CSV AUTOMATICALLY
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent

csv_files = list(
    BASE_DIR.glob("bestsellers_wth_categories_2022_03_27*")
)

if not csv_files:
    st.error("CSV file not found!")
    st.write("Files found:", [f.name for f in BASE_DIR.iterdir()])
    st.stop()

CSV_FILE = csv_files[0]

try:
    books_df = pd.read_csv(CSV_FILE)
    st.success("CSV connected successfully!")

except Exception as error:
    st.error(f"CSV error: {error}")
    st.stop()

# ---------------------------------
# CHECK CSV COLUMNS
# ---------------------------------

required_columns = [
    "Name",
    "Author",
    "User Rating",
    "Reviews",
    "Price",
    "Year",
    "Genre"
]

if not all(column in books_df.columns for column in required_columns):
    st.error("Some required columns are missing!")
    st.write("Available columns:", books_df.columns.tolist())
    st.stop()

# ---------------------------------
# TITLE
# ---------------------------------

st.title("📚 Best Selling Books Dashboard")

st.write(
    "This app analyzes Amazon's top-selling books "
    "from 2009 to 2022."
)

st.caption(f"Connected file: {CSV_FILE.name}")

# ---------------------------------
# ADD NEW BOOK
# ---------------------------------

st.sidebar.header("Add New Book Data")

with st.sidebar.form("book_form"):

    new_name = st.text_input("Book Name")

    new_author = st.text_input("Author")

    new_user_rating = st.slider(
        "User Rating",
        0.0, 5.0, 0.0, 0.1
    )

    new_reviews = st.number_input(
        "Reviews",
        min_value=0,
        step=1
    )

    new_price = st.number_input(
        "Price",
        min_value=0,
        step=1
    )

    new_year = st.number_input(
        "Year",
        min_value=2009,
        max_value=2022,
        step=1
    )

    genres = sorted(books_df["Genre"].dropna().unique())

    new_genre = st.selectbox(
        "Genre",
        genres
    )

    submit_button = st.form_submit_button("Add Book")

    if submit_button:

        if not new_name.strip() or not new_author.strip():

            st.sidebar.error(
                "Please enter book name and author!"
            )

        else:

            new_data = {
                "Name": new_name,
                "Author": new_author,
                "User Rating": new_user_rating,
                "Reviews": new_reviews,
                "Price": new_price,
                "Year": new_year,
                "Genre": new_genre
            }

            books_df = pd.concat(
                [pd.DataFrame([new_data]), books_df],
                ignore_index=True
            )

            books_df.to_csv(
                CSV_FILE,
                index=False
            )

            st.sidebar.success(
                "New book added successfully!"
            )

            st.rerun()

# ---------------------------------
# FILTER OPTIONS
# ---------------------------------

st.sidebar.header("Filter Options")

authors = sorted(books_df["Author"].dropna().unique())

years = sorted(books_df["Year"].dropna().unique())

genres = sorted(books_df["Genre"].dropna().unique())

selected_author = st.sidebar.selectbox(
    "Select Author",
    ["All"] + list(authors)
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + list(years)
)

selected_genre = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + list(genres)
)

# ---------------------------------
# FILTER DATA
# ---------------------------------

filtered_books_df = books_df.copy()

if selected_author != "All":

    filtered_books_df = filtered_books_df[
        filtered_books_df["Author"] == selected_author
    ]

if selected_year != "All":

    filtered_books_df = filtered_books_df[
        filtered_books_df["Year"] == selected_year
    ]

if selected_genre != "All":

    filtered_books_df = filtered_books_df[
        filtered_books_df["Genre"] == selected_genre
    ]

# ---------------------------------
# SUMMARY STATISTICS
# ---------------------------------

st.subheader("📊 Summary Statistics")

total_books = len(filtered_books_df)

unique_titles = filtered_books_df["Name"].nunique()

average_rating = filtered_books_df["User Rating"].mean()

average_price = filtered_books_df["Price"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Books",
    total_books
)

col2.metric(
    "Unique Titles",
    unique_titles
)

col3.metric(
    "Average Rating",
    f"{average_rating:.2f}" if pd.notna(average_rating) else "N/A"
)

col4.metric(
    "Average Price",
    f"${average_price:.2f}" if pd.notna(average_price) else "N/A"
)

# ---------------------------------
# BOOKS ANALYSIS
# ---------------------------------

st.subheader("📈 Books Analysis")

chart1, chart2 = st.columns(2)

with chart1:

    genre_chart = px.pie(
        filtered_books_df,
        names="Genre",
        title="Books by Genre"
    )

    st.plotly_chart(
        genre_chart,
        use_container_width=True
    )

with chart2:

    year_chart = px.histogram(
        filtered_books_df,
        x="Year",
        color="Genre",
        title="Books by Year"
    )

    st.plotly_chart(
        year_chart,
        use_container_width=True
    )

# ---------------------------------
# BOOKS DATABASE
# ---------------------------------

st.subheader("📖 Books Database")

st.dataframe(
    filtered_books_df,
    use_container_width=True
)

# ---------------------------------
# DOWNLOAD CSV
# ---------------------------------

st.download_button(
    label="Download Books CSV",
    data=filtered_books_df.to_csv(
        index=False
    ).encode("utf-8"),
    file_name="books_data.csv",
    mime="text/csv"
)

# ---------------------------------
# FOOTER
# ---------------------------------

st.success("Books Dashboard loaded successfully!")
