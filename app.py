from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from typing import List

# Load saved files
tfidf = joblib.load("model_files/tfidf_vectorizer.pkl")
tfidf_matrix = joblib.load("model_files/tfidf_matrix.pkl")
# cos_sim = joblib.load("model_files/cosine_similarity_matrix.pkl")
from model_utils import load_cosine_similarity_from_blob
cos_sim = load_cosine_similarity_from_blob()

df = pd.read_csv("model_files/manga_metadata.csv")

# FastAPI app
app = FastAPI(title="Manga Recommendation API")

# Input model
class MangaRequest(BaseModel):
    title: str
    top_n: int = 5

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Manga Recommendation API!"}

@app.post("/recommend")
def get_recommendations(request: MangaRequest) -> List[str]:
    title = request.title
    top_n = request.top_n

    if title not in df['Name'].values:
        raise HTTPException(status_code=404, detail="Manga title not found")

    idx = df[df['Name'] == title].index[0]
    scores = list(enumerate(cos_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommendations = df['Name'].iloc[[i for i, _ in scores]].tolist()
    return recommendations
