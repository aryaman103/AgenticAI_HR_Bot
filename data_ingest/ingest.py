from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding

def build_knowledge_base(data_dir = "./data_ingest"):
    documents = SimpleDirectoryReader(data_dir).load_data()
    embed_model = OpenAIEmbedding()
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    return index