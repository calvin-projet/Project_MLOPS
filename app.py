from flask import Flask, request, jsonify, send_file, render_template
import os
import pandas as pd
import pickle
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import CountVectorizer
import re

app = Flask(__name__)
model = pickle.load(open('data/model_xgb.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='GET':
        return render_template('page.html')
    
    elif request.method == 'POST':
        df_anime = pd.read_csv("data/Anime_data.csv")
        df_anime = df_anime[:10000]
        df_anime = df_anime.dropna(subset=["Rating"])
        
        df_anime = df_anime.drop('Aired', axis=1)
        df_anime = df_anime.drop('Anime_id', axis=1)
        df_anime = df_anime.drop('Link', axis=1)
        df_anime = df_anime.drop('Source', axis=1)
        df_anime = df_anime.drop('Episodes', axis=1)
        df_anime = df_anime.drop('Popularity', axis=1)
        df_anime = df_anime.drop('ScoredBy', axis=1)
        df_anime = df_anime.drop('Members', axis=1)
        
        Title = request.form['title']
        Genre = request.form['genre']
        Type = request.form['type']
        Producer = request.form['producer']
        Studio = request.form['studio']
        
        df_anime.loc[0] = ({'Title': str(Title), 'Genre': str(Genre), 'Type': str(Type), 'Producer': str(Producer), 'Studio': str(Studio)})

        df_anime['Synopsis'] = df_anime['Synopsis'].fillna("unknown")
        
        df_anime['Genre'] = df_anime['Genre'].fillna("['unknown']")

        df_anime['Genre'] = df_anime['Genre'].str.replace('[', '')
        df_anime['Genre'] = df_anime['Genre'].str.replace(']', '')
        df_anime['Genre'] = df_anime['Genre'].str.replace("'", '')
        dummies = df_anime["Genre"].str.get_dummies(', ').add_prefix('genre_')
        df_anime = pd.concat([df_anime, dummies], axis=1)
        df_anime = df_anime.drop('Genre', axis=1)

        df_anime['Producer'] = df_anime['Producer'].fillna("['unknown']")
        df_anime['Producer'] = df_anime['Producer'].str.replace('[', '')
        df_anime['Producer'] = df_anime['Producer'].str.replace(']', '')
        df_anime['Producer'] = df_anime['Producer'].str.replace("'", '')
        dummies = df_anime["Producer"].str.get_dummies(', ').add_prefix('producer_')
        df_anime = pd.concat([df_anime, dummies], axis=1)
        df_anime = df_anime.drop('Producer', axis=1)
        
        df_anime['Studio'] = df_anime['Studio'].fillna("['unknown']")
        df_anime['Studio'] = df_anime['Studio'].str.replace('[', '')
        df_anime['Studio'] = df_anime['Studio'].str.replace(']', '')
        df_anime['Studio'] = df_anime['Studio'].str.replace("'", '')
        dummies = df_anime["Studio"].str.get_dummies(', ').add_prefix('studio_')
        df_anime = pd.concat([df_anime, dummies], axis=1)
        df_anime = df_anime.drop('Studio', axis=1)
        
        dummies = df_anime["Type"].str.get_dummies(', ').add_prefix('type_')
        df_anime = pd.concat([df_anime, dummies], axis=1)
        df_anime = df_anime.drop('Type', axis=1)
        
        df_temp = df_anime[['Title', 'Synopsis']]
        
        df_temp["Title"] = df_temp["Title"].apply(lambda x: re.sub(r'\s*(\r\n\s*)+|\[Written by .*?\]+|\(Source: .*?\)\s*', '', x))
        df_temp["Title"] = df_temp["Title"].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))
        df_temp["Title"] = df_temp["Title"].apply(lambda x : word_tokenize(x))
        df_temp["Title"] = df_temp["Title"].apply(lambda words : [word for word in words if word not in nltk.corpus.stopwords.words('english')])
        model_wc = Word2Vec(df_temp['Title'], vector_size=100, window=5, min_count=1, workers=4)
        def get_title_vector(title):
            words = title.lower().split()
            vectors = [model_wc.wv[word] for word in words if word in model_wc.wv.key_to_index]
            if len(vectors) > 0:
                return sum(vectors) / len(vectors)
            else:
                return np.zeros(model_wc.vector_size)
        
        df_anime["Title"] = df_anime["Title"].apply(get_title_vector)
        scaler = MinMaxScaler()
        df_anime["Title"] = scaler.fit_transform(df_anime["Title"].tolist())
        
        df_anime = df_anime.drop('Synopsis', axis=1)
        df_anime = df_anime.drop('Rating', axis=1)
        
        Prediction = model.predict(df_anime.iloc[[0]])
        
        return render_template('predict-rating.html',title=Title, genre=Genre, type=Type, producer=Producer, studio=Studio, prediction=Prediction)

if __name__ == '__main__':
    app.run(debug=True, port=8085)