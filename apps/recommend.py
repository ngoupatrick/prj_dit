import streamlit as st
import pandas as pd
from backend.file_manager import *
from backend.manage_data import *
from backend.content_base import *
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
    cont_achat = st.container()#st.empty()
    if choice!="--":
        image_placeholder = image_cont.empty()
        image_placeholder.image(os.path.join(folder,choice))
        df = get_user_achat(img_user=choice)
        #cont_achat.write(df)
        
        ls_code_produit = {
            "code_produit": [],
            "nb":[]
        }
        try:
            nb_row = df.index
        except: return
        for nx in nb_row:
            try:
                idx_p = ls_code_produit["code_produit"].index(df.loc[nx,"code_produit"])
            except:
                idx_p=-1
            if idx_p==-1:
                ls_code_produit["code_produit"].append(df.loc[nx,"code_produit"])
                ls_code_produit["nb"].append(1.0)
            else:
                ls_code_produit["nb"][idx_p]=float(ls_code_produit["nb"][idx_p])+float(df.loc[nx,"quantite"])
        df_p = pd.DataFrame(ls_code_produit)
        cont_produit.write("Achats cumulés")
        dk_ = df_p.sort_values(by='nb', ascending=False).head(10)
        cont_produit.write(dk_)
        cols = cont_achat.columns(10)
        p=0
        for i in dk_.index:
            dk = get_image_produit(code_produit=dk_.loc[i,"code_produit"])
            cols[p].image(dk.loc[dk.index[0],"photos"])
            p+=1
        
        df_f, df2, cosine_sim2 = funct()
        try:
            nb_row = df_p.index
        except: return
        ls_predict = [get_recommendations(df_f=df_f, df2=df2, code_produit=df_p.loc[nn,"code_produit"],cosine_sim=cosine_sim2) for nn in nb_row]
        #cont_produit.write(ls_predict[0])
        ls_code_produit_final = {
            "code_produit": [],
            "nb":[],
            "nom":[],
            "photos":[]
        }
        
        for ls in ls_predict:
            try:
                nb_row = ls.index
            except: return
            for nx in nb_row:
                try:
                    idx_p = ls_code_produit_final["code_produit"].index(ls.loc[nx,"code_produit"])
                except:
                    idx_p=-1
                if idx_p==-1:
                    ls_code_produit_final["code_produit"].append(ls.loc[nx,"code_produit"])
                    ls_code_produit_final["nom"].append(ls.loc[nx,"nom"])
                    ls_code_produit_final["photos"].append(ls.loc[nx,"photos"])                    
                    ls_code_produit_final["nb"].append(1.0)
                else:
                    ls_code_produit_final["nb"][idx_p]=float(ls_code_produit_final["nb"][idx_p])+1
        df_final = pd.DataFrame(ls_code_produit_final)  
        cont_produit.write("Recommandations basé sur le contenu") 
        dk_ = df_final.sort_values(by='nb', ascending=False).head(10)         
        cont_produit.write(dk_)
        cols = cont_achat.columns(10)
        p=0
        for i in dk_.index:
            dk = get_image_produit(code_produit=dk_.loc[i,"code_produit"])
            cols[p].image(dk.loc[dk.index[0],"photos"])
            p+=1
            
            

