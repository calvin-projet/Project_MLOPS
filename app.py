from flask import Flask, request, jsonify, send_file, render_template
import os
import pandas as pd
import pickle

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
        
        df_anime = df_anime.drop('Title', axis=1)
        df_anime = df_anime.drop('Aired', axis=1)
        df_anime = df_anime.drop('Anime_id', axis=1)
        df_anime = df_anime.drop('Link', axis=1)
        df_anime = df_anime.drop('Source', axis=1)
        df_anime = df_anime.drop('Episodes', axis=1)
        df_anime = df_anime.drop('Popularity', axis=1)
        df_anime = df_anime.drop('ScoredBy', axis=1)
        df_anime = df_anime.drop('Members', axis=1)
        df_anime = df_anime.drop('Synopsis', axis=1)
        df_anime = df_anime.drop(['Rating'], axis=1)
        
        Genre = request.form['genre']
        Type = request.form['type']
        Producer = request.form['producer']
        Studio = request.form['studio']
        
        df_anime.loc[0] = ({'Genre': str(Genre), 'Type': str(Type), 'Producer': str(Producer), 'Studio': str(Studio)})

        
        df_anime['Genre'] = df_anime['Genre'].fillna("['unknown']")
        df_anime['Producer'] = df_anime['Producer'].fillna("['unknown']")
        df_anime['Studio'] = df_anime['Studio'].fillna("['unknown']")
        df_anime['Type'] = df_anime['Type'].fillna("['unknown']")
        
        df_anime['Genre'] = df_anime['Genre'].str.replace('[', '')
        df_anime['Genre'] = df_anime['Genre'].str.replace(']', '')
        df_anime['Genre'] = df_anime['Genre'].str.replace("'", '')
        
        df_anime['Producer'] = df_anime['Producer'].str.replace('[', '')
        df_anime['Producer'] = df_anime['Producer'].str.replace(']', '')
        df_anime['Producer'] = df_anime['Producer'].str.replace("'", '')
        
        df_anime['Studio'] = df_anime['Studio'].str.replace('[', '')
        df_anime['Studio'] = df_anime['Studio'].str.replace(']', '')
        df_anime['Studio'] = df_anime['Studio'].str.replace("'", '')
        
        df_anime['Type'] = df_anime['Type'].str.replace('[', '')
        df_anime['Type'] = df_anime['Type'].str.replace(']', '')
        df_anime['Type'] = df_anime['Type'].str.replace("'", '')
        
        dummies = df_anime["Studio"].str.get_dummies(', ').add_prefix('studio_')
        df_anime = pd.concat([df_anime, dummies], axis=1)
        df_anime = df_anime.drop('Studio', axis=1)
        
        dummies = df_anime["Type"].str.get_dummies(', ').add_prefix('type_')
        df_anime = pd.concat([df_anime, dummies], axis=1)
        df_anime = df_anime.drop('Type', axis=1)
        
        dummies = df_anime["Producer"].str.get_dummies(', ').add_prefix('producer_')
        df_anime = pd.concat([df_anime, dummies], axis=1)
        df_anime = df_anime.drop('Producer', axis=1)
        
        dummies = df_anime["Genre"].str.get_dummies(', ').add_prefix('genre_')
        df_anime = pd.concat([df_anime, dummies], axis=1)
        df_anime = df_anime.drop('Genre', axis=1)
        
        Prediction = model.predict(df_anime.iloc[[0]])
        
        return render_template('predict-rating.html', genre=Genre, type=Type, producer=Producer, studio=Studio, prediction=Prediction)

if __name__ == '__main__':
    app.run(debug=True, port=8085)