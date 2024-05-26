import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from backend.database.Database.Database import Database

# Load the ratings and movies data from CSV files
# ratings_df = pd.read_csv('../ratings.csv')
# movies_df = pd.read_csv('../movies_metadata.csv')

# ratings_df = Database.read_mysql_to_dataframe(query="SELECT * FROM ratings")
movies_df = Database.read_mysql_to_dataframe(query="SELECT * FROM movies")

# create an empty DataFrame
movies = pd.DataFrame()
movies['id'] = movies_df['movieId']
movies['title'] = movies_df['title']
movies['year'] = movies_df['year']
movies['genre'] = movies_df['genre'].apply(lambda x: x.replace('|', ' '))
movies['director'] = movies_df['director'].str.replace(' ', '').str.replace(',', ' ')
movies['actors'] = movies_df['actors'].str.replace(' ', '').str.replace(',', ' ')
movies['plot'] = movies_df['plot'].fillna('')
movies.isnull().sum()
movies.fillna('', inplace=True)
movies = movies[['id', 'title', 'genre', 'actors', 'plot']]
print(movies)
print("-----------------------")

# text_data = np.array(movies['plot'])
#
# model = SentenceTransformer('all-MiniLM-L6-v2')
# embeddings = model.encode(text_data, show_progress_bar=True)
#
# similarity_sbert = cosine_similarity(embeddings)

# cos_sim_data = pd.DataFrame(similarity_sbert)
# Load cos_sim_data from the saved file
with open('SBERT_data/cos_sim_data.pkl', 'rb') as f:
    cos_sim_data = pickle.load(f)
print(cos_sim_data)
print("---------------")

# # Save embeddings to a file using pickle
# with open('SBERT_data/embeddings.pkl', 'wb') as f:
#     pickle.dump(embeddings, f)
#
# # Save similarity_sbert to a file using pickle
# with open('SBERT_data/similarity_sbert.pkl', 'wb') as f:
#     pickle.dump(similarity_sbert, f)
#
# # Save cos_sim_data to a file using pickle
# with open('SBERT_data/cos_sim_data.pkl', 'wb') as f:
#     pickle.dump(cos_sim_data, f)

df = movies.reset_index()
data = movies[['title', 'genre']]
indices = pd.Series(movies.index, index=movies['title'])
print("indices")
print(indices)
print("------------------")


def get_recommendations(title, N=10):
    idx = indices[title]
    sim_scores = list(enumerate(cos_sim_data[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:N + 1]
    movie_indices = [i[0] for i in sim_scores]
    sim_scores = pd.DataFrame(sim_scores, columns=['index', 'similarity_score'])
    final_data = data.iloc[movie_indices]
    final_data = final_data.merge(sim_scores, left_index=True, right_on='index')
    final_data['similarity_score'] = round(final_data['similarity_score'], 2)
    del final_data['index']
    return final_data


top_movies_sbert = get_recommendations('Star Wars: Episode III - Revenge of the Sith', 15)
print(top_movies_sbert)
