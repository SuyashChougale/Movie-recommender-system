import numpy as np
import pandas as pd

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

combo = movies.merge(credits,on='title')
combo = combo[['id','title','overview','keywords','cast','crew','genres']]

combo = combo.dropna()

import ast
def convert(obj):
    l = []
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l
combo['genres'] = combo['genres'].apply(convert)
combo['keywords'] = combo['keywords'].apply(convert)


def convert2(obj):
    l = []
    counter  = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            l.append(i['name'])
            counter +=1
        else:
            break
    return l
combo['cast'] = combo['cast'].apply(convert2)

def convert3(obj):
    l = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
            return l
combo['crew'] = combo['crew'].apply(convert3)

combo = combo.dropna()

combo['cast'] = combo['cast'].apply(lambda x:[i.replace(" ","") for i in x])
combo['crew'] = combo['crew'].apply(lambda x:[i.replace(" ","") for i in x])
combo['keywords'] = combo['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
combo['genres'] = combo['genres'].apply(lambda x:[i.replace(" ","") for i in x])
combo['overview'] = combo['overview'].apply(lambda x:[i.split() for i in x])

combo['tags'] = combo['cast']+combo['crew']+combo['genres']+combo['keywords']+combo['overview']
combo = combo[['id','title','tags']]

def convert4(obj):
    l = ""
    for i in obj:
        l = l+" "+str(i) 
    return l

combo['tags'] = combo['tags'].apply(convert4)
combo['tags'] = combo['tags'].apply(lambda x: x.lower())

from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
st = PorterStemmer()
def stemming(obj):
    y = []
    for i in obj.split():
        y.append(st.stem(i))
    y = " ".join(y)
    return y
combo['tags'] = combo['tags'].apply(stemming)

cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(combo['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

def recommend(obj):
    movie_ind = combo[combo['title'] == obj].index[0]
    distance = list(enumerate(similarity[movie_ind]))
    distance = sorted(distance,reverse=True,key=lambda x:x[1])[1:6]
    l = [ ]
    for i in distance:
        l.append(combo.iloc[i[0]].title)
    return l


# recommend('Batman Begins')
