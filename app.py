import numpy as np
import pandas as pd
import streamlit as st
import pickle

st.set_page_config(page_title="Recommendation System",page_icon=":books:", layout='wide',initial_sidebar_state='auto')
st.header("Book Recommendation System")
st.markdown("**Welcome to the Book Recommendation System. You can search for books and get recommendations based on your search.**")
st.markdown("This site uses Collaborative Filtering to recommend books to users. Collaborative Filtering is a technique used by websites like Amazon, Netflix, etc. to recommend items to users based on their past interactions with the system.")

# Load the pickled model
popular = pickle.load(open('popular_books.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
pivot_table = pickle.load(open('pivot_table.pkl', 'rb'))
similarity = pickle.load(open('similarity_scores.pkl', 'rb'))

#top 50 popular books
st.sidebar.title("Popular 50 Books")
if st.sidebar.button("Show Top 50 Books"):
    cols_per_row = 5
    rows = 10
    for row in range(rows):
        cols = st.columns(cols_per_row)
        for col in range(cols_per_row):
            book_idx = row * cols_per_row + col
            if book_idx < len(popular):
                with cols[col]:
                    st.image(popular.iloc[book_idx]['Image-URL-M'])
                    st.text(popular.iloc[book_idx]['Book-Title'])
                    st.text(popular.iloc[book_idx]['Book-Author'])

# Search for a book
def recommandation(book_name):
  index = np.where(pivot_table.index==book_name)[0][0]
  similar_items = sorted(list(enumerate(similarity[index])), key=lambda x:x[1], reverse=True)[1:6]
  data_list = []
  for i in similar_items:
    item = []
    temp_df = books[books['Book-Title']==pivot_table.index[i[0]]]
    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
    item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
    data_list.append(item)
  return data_list

book_list = pivot_table.index.values
st.sidebar.title("Similar Book Suggestions")
selected_book = st.sidebar.selectbox("Search for a book", book_list)
if st.sidebar.button("Search"):
    st.subheader("Book Recommendations")
    cols_per_row = 5
    rows = 1
    for row in range(rows):
        cols = st.columns(cols_per_row)
        for col in range(cols_per_row):
            book_idx = row * cols_per_row + col
            if book_idx < len(recommandation(selected_book)):
                with cols[col]:
                    st.image(recommandation(selected_book)[book_idx][2])
                    st.text(recommandation(selected_book)[book_idx][0])
                    st.text(recommandation(selected_book)[book_idx][1])
#import data
books = pd.read_csv('~/main/Books.csv')
ratings = pd.read_csv('~/main/Ratings.csv')
#users = pd.read_csv('~/main/Users.csv')
st.sidebar.title("Used Data sets")
if st.sidebar.button("Show Data sets"):
    st.subheader("Books Data")
    st.dataframe(books)
    #st.subheader("Ratings Data")
    #st.dataframe(ratings)
    #st.subheader("Users Data")
    #st.dataframe(users)

