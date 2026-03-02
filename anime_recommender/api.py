import joblib
import pandas as pd
import warnings
from django.http import JsonResponse, request
import numpy as np
from scipy.sparse import coo_matrix, vstack

warnings.filterwarnings("ignore")
import os
import pandas as pd
import joblib

# Get project root (one level above your first anime_recommender folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # anime_recommender/anime_recommender
PROJECT_ROOT = os.path.dirname(BASE_DIR)              # anime_recommender

# Correct data paths
RATINGS_PATH = os.path.join(PROJECT_ROOT, 'anime_recommender', 'data', 'ratings.csv')
ANIME_PATH = os.path.join(PROJECT_ROOT, 'anime_recommender', 'data', 'anime.csv')

ANIME_MAP_PATH = os.path.join(PROJECT_ROOT, 'anime_recommender', 'ml_models', 'anime_map.pkl')
USER_MAP_PATH = os.path.join(PROJECT_ROOT, 'anime_recommender', 'ml_models', 'user_map.pkl')
REVERSE_ANIME_MAP_PATH = os.path.join(PROJECT_ROOT, 'anime_recommender', 'ml_models', 'reverse_anime_map.pkl')
MODEL_PATH = os.path.join(PROJECT_ROOT, 'anime_recommender', 'ml_models', 'nlp_model.joblib')

# Load CSVs and pickles
rating_df = pd.read_csv(RATINGS_PATH)
anime_df = pd.read_csv(ANIME_PATH)

anime_map = joblib.load(ANIME_MAP_PATH)
user_map = joblib.load(USER_MAP_PATH)
reverse_anime_map = joblib.load(REVERSE_ANIME_MAP_PATH)

# --- KNN Model ---
class ML_Models:
    def __init__(self, recommender_model, rating_df, anime_df):
        self.recommender_model = recommender_model
        self.rating_df = rating_df
        self.anime_df = anime_df


class KNN_Model(ML_Models):
    def __init__(self, anime_map, user_map, reverse_anime_map):
        super().__init__(
            recommender_model=joblib.load(MODEL_PATH),
            rating_df=rating_df,
            anime_df=anime_df
        )

        self.anime_map = anime_map
        self.user_map = user_map
        self.reverse_anime_map = reverse_anime_map

        # Build interaction matrix at initialization
        self.interaction_matrix = self._create_interaction_matrix()

    def _create_interaction_matrix(self):
        chunks = np.array_split(self.rating_df, 20)
        sparse_chunks = []
        for chunk in chunks:
            rows = chunk["user_id"].map(self.user_map)
            cols = chunk["anime_id"].map(self.anime_map)
            vals = chunk["rating"].astype(float)
            shape = (len(self.user_map), len(self.anime_map))
            sparse_chunk = coo_matrix((vals, (rows, cols)), shape=shape)
            sparse_chunks.append(sparse_chunk)
        return vstack(sparse_chunks).tocsr()

    def recommendation_identification(self, anime_id):
        if anime_id not in self.anime_map:
            return {"error": "Anime not found in recommendation dataset", "anime_id": anime_id}, 404

        target_idx = self.anime_map[anime_id]
        distances, indices = self.recommender_model.kneighbors(
            self.interaction_matrix.T[target_idx].reshape(1, -1), n_neighbors=5
        )

        similar_anime_ids = [
            int(self.reverse_anime_map[int(i)])
            for i in indices.flatten()
            if int(self.reverse_anime_map[int(i)]) != anime_id
        ]

        result = {"similar_anime_ids": similar_anime_ids}

        for aid in similar_anime_ids:
            print(self.anime_df[self.anime_df["anime_id"] == aid]["name"].values[0])

        return result


# --- Initialize global KNN object ---
KNN = KNN_Model(anime_map, user_map, reverse_anime_map)

class MAL_Access:
    def __init__(self):
        headers={"X-MAL-CLIENT-ID": "e863fdfe943adee262553933a60982f8"}
    
    def get_anime_details(anime_id):
        try:
            # Make the request to MyAnimeList API from your server
            response = request.get(
                f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,rank,popularity,media_type,genres",
                headers={"X-MAL-CLIENT-ID": "e863fdfe943adee262553933a60982f8"},
            )
            response.raise_for_status()
            return JsonResponse(response)
        except request.RequestException as e:
            return JsonResponse({"error": str(e)}), 500