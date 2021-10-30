import streamlit as st
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@st.experimental_singleton
def funct(file = "loreal_final.csv"):
    df_f = pd.read_csv("loreal_final.csv")
    #prepare the dataframe
    df_f.drop_duplicates(inplace=True) 
    df_f.prix.fillna(0, inplace=True)
    df_f.description.fillna("", inplace=True)
    df_f.prix = df_f.prix.apply(lambda x: str(x).split(" ")[0].replace(",","."))
    df_f.prix.astype(float)
    col = ["section","sous-section","categorie","photos", "nom", "description", "url_scrap", "code_produit"]
    df_f[col].astype(str)
    
    df_f.prix.fillna(0.0, inplace=True)
    df_f.description.fillna("", inplace=True)
    
    df2 = df_f.copy()
    features = ['categorie', 'nom', '_description']
    
    #prepare columns for prepocessing
    df2.categorie = df2.categorie.apply(lambda x: str(x).split(" "))
    df2.nom = df2.nom.apply(lambda x: str(x).split(" "))
    df2["_description"] = df2.description.apply(replace_car)
    df2["_description"] = df2["_description"].apply(lambda x: str(x).split(" "))
    
    for feature in features:
        df2[feature] = df2[feature].apply(clean_data)
    
    #create a mix of all char found in ['categorie', 'nom', '_description']
    df2['soup'] = df2.apply(create_soup, axis=1)
    
    final_stopwords_list = stopwords.words('french')

    count = CountVectorizer(stop_words=final_stopwords_list)
    count_matrix = count.fit_transform(df2['soup'])
    
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    
    return df_f, df2, cosine_sim2
    
def replace_car(x):
    v = str(x).replace("-"," ").replace("_", " ").replace(",", " ").strip()
    return v

# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
        
def create_soup(x):
    return ' '.join(x['categorie']) + ' ' + ' '.join(x['nom']) + ' ' + ' '.join(x['_description'])

#use: 
#We use this if the user have already buy something
# Function that takes code_product as input and outputs most similar product
def get_recommendations(df_f, df2,code_produit, cosine_sim):
    indices = pd.Series(df2.index, index=df2['code_produit'])
    nb=30#number of max best records found
    # Get the index of the product that matches the code_product
    idx = indices[code_produit]
    if isinstance(idx, pd.Series):
        k =  idx.head(1)
        idx = k.iloc[0]

    # Get the pairwsie similarity scores of all products with that product
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the product based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the [nb] most similar product
    sim_scores = sim_scores[1:nb+1]

    # Get the product indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar product based on code_product given
    return df_f[['code_produit', "nom", 'photos']].iloc[movie_indices]