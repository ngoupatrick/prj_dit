import random
import pandas as pd
import streamlit as st
from backend.file_manager import *
from _deepface import DeepFace
import os
from datetime import datetime

def app():
    btn_generer = st.button(label="generer les achats")
    if btn_generer:
        alea_achat()
    
def alea_achat():
    data = {
        "age":[],
        "sexe":[],
        "race":[],
        "img_client":[],
        "code_achat":[],
        "code_produit":[],
        "date": [],
        "quantite": []
    }
    df = pd.DataFrame(data)
    df.age = df.age.astype(int)
    
    n_achat = 10
    path_produit = "loreal_final.csv"
    folder_img = "./image_client"
    ls_image=files_in_folder(folder=folder_img)
    df_produit = pd.read_csv(path_produit)
    index_produit = df_produit.index
    
    for n in range(n_achat):
        idx_p = random.choice(index_produit)#choosen product
        img_choose = random.choice(ls_image)#choosen image of person
        
        path_img = os.path.join(folder_img,img_choose)
        infomation = analyse(path_image=path_img)
        data_here = {
            "age":int(infomation["age"]),
            "sexe":infomation["gender"],
            "race":infomation["race"],
            "img_client":img_choose,
            "code_achat":generate_achat_code(),
            "code_produit":df_produit.loc[idx_p,"code_produit"],
            "date": datetime.now(),
            "quantite": 1.0
        }
        df=df.append(data_here, ignore_index=True)
        
    st.write(df)
    df.to_csv("achat_test.csv", index=False)
        
def generate_achat_code():
    return "achat_"+str(datetime.now().microsecond)   

def analyse(path_image):
    if not os.path.isfile(path=path_image): return None
    try:
        analysis = DeepFace.analyze(img_path = path_image, actions = ["age", "gender", "emotion", "race"], detector_backend="mtcnn")        
        return get_analyse(analysis=analysis)
    except: return None
    
def get_analyse(analysis):
    return {
        "age": analysis['age'],
        "gender": analysis['gender'],
        "emotion": analysis['dominant_emotion'],
        "race": analysis['dominant_race']
        }