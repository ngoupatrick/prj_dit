import streamlit as st
import pandas as pd
from backend.file_manager import *
from datetime import datetime

def app():
    st.write("Achats")
    ls_image = ["--"]
    folder = "./image_client"
    ls_image.extend(files_in_folder(folder=folder))
    col_info, col_achat = st.columns([1,2])
    choice = col_info.selectbox(label="Picture", options=ls_image)
    image_cont = col_info.container()
    cont_produit = col_achat.container()
    cont_achat = st.empty()
    if choice!="--":
        image_placeholder = image_cont.empty()
        image_placeholder.image(os.path.join(folder,choice))
     
    df_produit = load_produit()
    #st.write(df_produit.code_produit.value_counts())
        
    #form_prodduit = cont_produit.form("Produits")
    code_achat = generate_achat_code()
    cont_produit.write(f"Achat: {code_achat}")
    choix_code = cont_produit.selectbox(label="Code produit", options=df_produit["code_produit"])
    nom_produit = cont_produit.empty()
    photo_produit = cont_produit.empty()
    
    if choix_code:
        v = df_produit[df_produit["code_produit"]==choix_code]
        nom_produit.write(v["nom"][v.index[0]])
        photo_produit.image(v["photos"][v.index[0]])
        
    #submitted = form_prodduit.form_submit_button("Basket")
    btn_achat = cont_produit.button(label="ADD")
    if btn_achat:
        if choice=="--":
            st.error("Choose a client")
            return
        if not choix_code:
            st.error("Choose a product")
            return 
        df_achat = add_achat({"img_client":choice,"code_achat":code_achat,"code_produit":choix_code,"date": datetime.now(),"quantite":1})
        print(df_achat)
        cont_achat.write(df_achat)
        
def generate_achat_code():
    return "achat_"+str(datetime.now().microsecond)

@st.cache(ttl=3600)           
def load_produit(file = "loreal_final.csv"):
    return pd.read_csv(file)        
    
def data_achat_test():
    data = {
        "img_client":[],
        "code_achat":[],
        "code_produit":[],
        "date": [],
        "quantite": []
    }
    return pd.DataFrame(data)

  
def add_achat(line):
    df_achat = st.session_state.get('_df_achat')
    if df_achat is None:
        df_achat=data_achat_test()   
    df_achat=df_achat.append(line, ignore_index=True) 
    st.session_state['_df_achat'] = df_achat.copy()
    return df_achat