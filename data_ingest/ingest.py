from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding
from data_ingest.document_parser import HRDocumentParser

def build_knowledge_base(data_dir="./data_ingest"):
    """Build knowledge base using enhanced document parser."""
    
    # Try using the enhanced parser first
    try:
        parser = HRDocumentParser(data_dir)
        documents = parser.parse_directory()
        
        if documents:
            print(f"✓ Parsed {len(documents)} documents using enhanced parser")
            embed_model = OpenAIEmbedding()
            index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
            return index
        else:
            print("No documents found with enhanced parser, falling back to simple reader")
            
    except Exception as e:
        print(f"Enhanced parser failed: {e}, falling back to simple reader")
    
    # Fallback to simple directory reader
    try:
        documents = SimpleDirectoryReader(data_dir).load_data()
        embed_model = OpenAIEmbedding()
        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
        return index
    except Exception as e:
        print(f"Failed to build knowledge base: {e}")
        raise

def get_document_stats(data_dir="./data_ingest"):
    """Get statistics about available documents."""
    parser = HRDocumentParser(data_dir)
    return parser.get_parsing_stats()