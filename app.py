import streamlit as st
import pandas as pd
import numpy as np
from itertools import cycle

pt_table = pd.read_pickle('user book data.pkl')
book_details = pd.read_pickle('book details.pkl')
with open('similarity score.npy', 'rb') as f:
    similarity_score = np.load(f)
book_names = pt_table.index.values.tolist()


def recommend(book_name):
    book_index = np.where(pt_table.index == book_name)[0][0]
    distances = similarity_score[book_index]
    similar_items = sorted(list(enumerate(distances)),
                           key=lambda x: x[1], reverse=True)[1:7]
    suggestion = []
    for i in similar_items:
        suggestion.append(pt_table.index[i[0]])
    return suggestion


st.set_page_config(page_title="Book recommender system")
st.title("Book recommender system")
option = st.selectbox("Enter or select a book name", book_names, index=0)
if st.button("Recommend"):
    recommendation = recommend(option)
    cols = cycle(st.columns(3))
    for recom in recommendation:
        next(cols).image(book_details[book_details['Book-Title'] == recom]['Image-URL-M'].values[0],
                         f"{book_details[book_details['Book-Title']==recom]['Book-Title'].values[0]} by {book_details[book_details['Book-Title']==recom]['Book-Author'].values[0]}", width=150)
        print(book_details[book_details['Book-Title']
              == recom]['Image-URL-M'].values[0])
