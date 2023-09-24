#----------------------------------------
# Function definition for text embedding
#-----------------------------------------

from vertexai.language_models import TextEmbeddingModel

def text_embedding(text) -> list:
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([text])
    for embedding in embeddings:
        vector = embedding.values
    return vector


