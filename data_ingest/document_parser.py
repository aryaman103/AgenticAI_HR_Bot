"""
Document Parser for HR Documents
Supports PDF, DOCX, TXT, and other formats
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from llama_index.core import Document
from llama_index.readers.file import (
    PDFReader,
    DocxReader,
    SimpleDirectoryReader
)

class HRDocumentParser:
    """Parser for HR documents with support for multiple formats."""
    
    def __init__(self, data_dir: str = "./data_ingest"):
        self.data_dir = Path(data_dir)
        self.supported_extensions = {'.pdf', '.docx', '.txt', '.md'}
    
    def parse_document(self, file_path: str) -> Document:
        """Parse a single document based on its extension."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if file_path.suffix.lower() not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        try:
            if file_path.suffix.lower() == '.pdf':
                reader = PDFReader()
                documents = reader.load_data(file_path)
            elif file_path.suffix.lower() == '.docx':
                reader = DocxReader()
                documents = reader.load_data(file_path)
            else:  # .txt, .md
                reader = SimpleDirectoryReader()
                documents = reader.load_data(str(file_path))
            
            if documents:
                return documents[0]
            else:
                raise ValueError(f"No content extracted from {file_path}")
                
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            raise
    
    def parse_directory(self) -> List[Document]:
        """Parse all supported documents in the data directory."""
        documents = []
        
        if not self.data_dir.exists():
            print(f"Data directory not found: {self.data_dir}")
            return documents
        
        for file_path in self.data_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                try:
                    doc = self.parse_document(str(file_path))
                    # Add metadata about the source file
                    doc.metadata.update({
                        'source_file': file_path.name,
                        'file_type': file_path.suffix.lower(),
                        'file_size': file_path.stat().st_size
                    })
                    documents.append(doc)
                    print(f"✓ Parsed: {file_path.name}")
                except Exception as e:
                    print(f"✗ Failed to parse {file_path.name}: {e}")
        
        return documents
    
    def get_parsing_stats(self) -> Dict[str, Any]:
        """Get statistics about parsed documents."""
        if not self.data_dir.exists():
            return {"error": "Data directory not found"}
        
        stats = {
            "total_files": 0,
            "parsed_files": 0,
            "failed_files": 0,
            "by_type": {}
        }
        
        for file_path in self.data_dir.iterdir():
            if file_path.is_file():
                file_type = file_path.suffix.lower()
                if file_type in self.supported_extensions:
                    stats["total_files"] += 1
                    stats["by_type"][file_type] = stats["by_type"].get(file_type, 0) + 1
        
        return stats

# Example usage
if __name__ == "__main__":
    parser = HRDocumentParser()
    stats = parser.get_parsing_stats()
    print("Document parsing statistics:")
    print(stats) 