from azure.storage.blob import BlobClient
import joblib
import io

def load_cosine_similarity_from_blob():
    blob_url = "https://edastoragehifsah.blob.core.windows.net/datasets/cosine_similarity_matrix.pkl?sp=r&st=2025-06-15T18:02:00Z&se=2025-07-05T02:02:00Z&spr=https&sv=2024-11-04&sr=b&sig=jT%2BlaSR751Uq%2BWpI442p0GufJeI55l%2B2eRB9h1vNLVo%3D"

    blob_client = BlobClient.from_blob_url(blob_url)
    blob_data = blob_client.download_blob().readall()
    cosine_sim = joblib.load(io.BytesIO(blob_data))
    return cosine_sim
