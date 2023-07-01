import streamlit as st
from model import combo,recommend 

st.title("movie recommendetion system")

option = st.selectbox('How would you like to be contacted?',combo['title']) 
if st.button('Recommend'):
    titles = recommend(option)
    for i in range(0,5):
        st.write(titles[i])
    
