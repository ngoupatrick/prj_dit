import pandas as pd
import streamlit as st


@st.experimental_singleton
def get_user_achat(img_user,  ch_data_achat="achat_test.csv"):
    df =pd.read_csv(ch_data_achat)
    df = df[df["img_client"]==img_user]
    return df.copy()

def get_image_produit(code_produit, ch_df_produit="loreal_final.csv"):
    df =pd.read_csv(ch_df_produit)
    df = df[df["code_produit"]==code_produit]
    return df.head(1).copy()