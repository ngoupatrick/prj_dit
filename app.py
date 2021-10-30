import streamlit as st
from multiapp import MultiApp
from apps import home, data, model, take_video, take_picture, test_face, achats, random_achat, recommend # import your app modules here

app = MultiApp()

st.markdown("""
# RECOMMANDATION SYSTEM

""")
#This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).

# Add all your application here
app.add_app("Recommandation Content based", recommend.app)
#app.add_app("Photo", take_picture.app)
app.add_app("Photo", take_picture.app)
app.add_app("Achats", achats.app)
app.add_app("Video", take_video.app)
#app.add_app("Generer Achat", random_achat.app)
#app.add_app("Home", home.app)
#app.add_app("Data", data.app)
#app.add_app("Model", model.app)
# The main app
app.run()
