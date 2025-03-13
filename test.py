import textwrap

import openai
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.postgres import PGVectorStore

embedding_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    embed_batch_size=64,
)

documents = SimpleDirectoryReader("./data/bavarian_beer").load_data()
print("Document ID:", documents[0].text)

vector_store = PGVectorStore.from_params(
    database="mydatabase",
    host="localhost",
    password="mypassword",
    port=6000,
    user="myuser",
    table_name="paul_graham_essay",
    embed_dim=384,  # openai embedding dimension
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True,
    embed_model=embedding_model,
)
