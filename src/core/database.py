from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List
from .models import Document, SearchResult
import torch


class VectorDatabase:
    """A vector database interface for storing and searching documents using Qdrant.

    This class provides methods to store documents as vectors and perform semantic searches
    on the stored content. It uses sentence-transformers for vector embeddings and Qdrant
    as the vector search engine.

    Attributes:
        collection_name (str): Name of the Qdrant collection
        client (QdrantClient): Qdrant client instance
        model (SentenceTransformer): Embedding model for vector generation
        vector_size (int): Dimensionality of the vectors (384 for all-MiniLM-L6-v2)
    """

    def __init__(
        self,
        collection_name: str = 'documents',
        host: str = 'http://localhost:6333',
        model_name: str = 'all-MiniLM-L6-v2',
    ):
        """Initializes the vector database with specified configuration.

        Args:
            collection_name: Name of the Qdrant collection (default: 'documents')
            host: Qdrant server host address (default: 'http://localhost:6333')
            model_name: Name of the sentence-transformers model (default: 'all-MiniLM-L6-v2')

        Note:
            Automatically detects and uses GPU if available for embedding generation.
        """
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.collection_name = collection_name
        self.client = QdrantClient(host)
        self.model = SentenceTransformer(model_name, device=device)
        self.vector_size = 384  # Vector size for all-MiniLM-L6-v2 model

        # Verify or create the collection
        self._initialize_collection()

    def _initialize_collection(self):
        """Initializes the Qdrant collection if it doesn't exist.

        Creates a new collection with cosine distance metric if the specified collection
        doesn't exist in the Qdrant database.

        Raises:
            Exception: If there's any communication error with Qdrant server
        """
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size, distance=models.Distance.COSINE
                ),
            )

    def save_documents(self, documents: List[Document]):
        """Stores a list of documents in the vector database.

        Processes each document by:
        1. Generating vector embeddings using the sentence-transformers model
        2. Storing the vectors along with metadata in Qdrant

        Args:
            documents: List of Document objects to be stored

        Example:
            >>> docs = [Document(content="example text", metadata={"source": "test"})]
            >>> db = VectorDatabase()
            >>> db.save_documents(docs)
        """
        points = []
        for idx, doc in enumerate(documents):
            vector = self.model.encode(doc.content)
            points.append(
                models.PointStruct(
                    id=idx,
                    vector=vector,
                    payload={
                        'content': doc.content,
                        'metadata': doc.metadata,
                        'page_number': doc.page_number,
                    },
                )
            )

        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query: str, top_k: int = 3) -> List[SearchResult]:
        """Performs semantic search on stored documents.

        Args:
            query: Search query string
            top_k: Number of most similar documents to return (default: 3)

        Returns:
            List of SearchResult objects ordered by similarity score

        Example:
            >>> db = VectorDatabase()
            >>> results = db.search("example query")
            >>> for result in results:
            ...     print(result.content)
        """
        query_vector = self.model.encode(query)
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
        )

        return [
            SearchResult(
                content=hit.payload['content'],
                score=hit.score,
                metadata=hit.payload['metadata'],
            )
            for hit in results
        ]
