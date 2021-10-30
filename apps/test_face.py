import streamlit as st
from deepface import DeepFace


def app():
    #filename = st.text_input(label="File Location:")
    filename = "./image_client/paul.jpg"
    analysis = DeepFace.analyze(img_path = filename, actions = ["age", "gender", "emotion", "race"])
    st.write(analysis)