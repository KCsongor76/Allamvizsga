import os
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from backend.database.Database.Database import Database
from backend.recsys.RecSys import RecSys

movies_df = Database.read_mysql_to_dataframe(query="SELECT * FROM movies")
movies = RecSys.prepare_movies(movies_df)
movies['combined_features'] = movies['genre'] + ' ' + movies['actors']
combined_features = np.array(movies['combined_features'])


model = SentenceTransformer('all-MiniLM-L6-v2')
path = 'SBERT_data/embeddings_g_a.pkl'

# Check if the path exists
if os.path.exists(path):
    with open(path, 'rb') as f:
        combined_embeddings = pickle.load(f)
    similarity_sbert_combined = cosine_similarity(combined_embeddings)
    cos_sim_data_combined = pd.DataFrame(similarity_sbert_combined)
else:
    # Assuming model and combined_features are defined elsewhere in the actual code
    combined_embeddings = model.encode(combined_features, show_progress_bar=True)
    similarity_sbert_combined = cosine_similarity(combined_embeddings)
    cos_sim_data_combined = pd.DataFrame(similarity_sbert_combined)

    # Create directory if it doesn't exist
    os.makedirs('SBERT_data', exist_ok=True)

    # Save embeddings to a file using pickle
    with open('SBERT_data/embeddings_g_a.pkl', 'wb') as f:
        pickle.dump(combined_embeddings, f)

    # Save similarity_sbert to a file using pickle
    with open('SBERT_data/similarity_sbert_g_a.pkl', 'wb') as f:
        pickle.dump(similarity_sbert_combined, f)

    # Save cos_sim_data to a file using pickle
    with open('SBERT_data/cos_sim_data_g_a.pkl', 'wb') as f:
        pickle.dump(cos_sim_data_combined, f)


# Prepare data for recommendations
data = movies[['title', 'genre']]
# indices = pd.Series(movies.index, index=movies['title'])


# Define the get_recommendations function with debug prints
def get_recommendations(genres, actors, N=10):
    # Create a query string from the genres and actors lists
    query = ' '.join(genres) + ' ' + ' '.join(actors)
    # Encode the query string using SBERT
    query_embedding = model.encode([query])
    # Compute similarity between the query embedding and all movie embeddings
    query_sim_scores = cosine_similarity(query_embedding, combined_embeddings).flatten()
    # Get the top N most similar movie indices
    sim_scores = list(enumerate(query_sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:N]
    movie_indices = [i[0] for i in sim_scores]
    final_data = data.iloc[movie_indices]
    titles = final_data['title'].tolist()
    movies = []
    for _title in titles:
        movie = Database.db_process(query="SELECT * FROM movies WHERE title = %s",
                                    params=(_title,))
        movies.append(RecSys.movie_to_dict(movie))
    return movies


# Example usage
genres = ['Action', 'Adventure']
actors = ['HarrisonFord', 'MarkHamill']
top_movies_sbert = get_recommendations(genres, actors)
print(top_movies_sbert)
