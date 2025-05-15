import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.title("Cocktail Advisor Chat")

if "history" not in st.session_state:
    st.session_state.history = []

for sender, msg in st.session_state.history:
    with st.chat_message(sender):
        st.markdown(msg)

if user_input := st.chat_input("Ask about cocktails..."):
    st.session_state.history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = requests.post(API_URL, json={"message": user_input})
        answer = response.json()["response"]
    except Exception as e:
        answer = f"Error: {str(e)}"

    st.session_state.history.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.markdown(answer)
