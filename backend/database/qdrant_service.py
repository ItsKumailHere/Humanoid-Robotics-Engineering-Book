# Qdrant Service for Vector Storage
# Provides methods to interact with Qdrant vector database

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
from database.qdrant_config import qdrant_settings, COLLECTION_CONFIG

class QdrantService:
    def __init__(self):
        # Initialize Qdrant client
        if qdrant_settings.QDRANT_HOST:
            # Connect to Qdrant Cloud
            self.client = QdrantClient(
                url=qdrant_settings.QDRANT_HOST,
                api_key=qdrant_settings.QDRANT_API_KEY,
                port=qdrant_settings.QDRANT_PORT
            )
        else:
            # Connect to local Qdrant (for development)
            self.client = QdrantClient(path="qdrant_data")
        
        self.collection_name = qdrant_settings.COLLECTION_NAME
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize the collection if it doesn't exist"""
        collection_exists = True
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            collection_exists = False
            # Create collection if it doesn't exist with free-tier optimized settings
            from qdrant_client.http.models import Distance
            # Convert string distance metric to Distance enum
            distance_map = {
                'Cosine': Distance.COSINE,
                'Euclid': Distance.EUCLID,
                'Manhattan': Distance.MANHATTAN,
                'Dot': Distance.DOT
            }
            distance_enum = distance_map.get(qdrant_settings.DISTANCE_METRIC, Distance.COSINE)

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=qdrant_settings.EMBEDDING_DIM,
                    distance=distance_enum
                ),
                on_disk_payload=qdrant_settings.ON_DISK,
                # Apply free-tier optimized settings from COLLECTION_CONFIG
                hnsw_config=models.HnswConfigDiff(
                    m=COLLECTION_CONFIG.get("hnsw_config", {}).get("m", 16),
                    ef_construct=COLLECTION_CONFIG.get("hnsw_config", {}).get("ef_construct", 100),
                )

                # BELOW IS COMMENTED OUT BECAUSE OF VERSION CONFLICTS:
                 # - optimzer_config was removed back in Qdrant >=1.7.0
                 # - my current qdrant-client version is 1.11.0 which does not support it
                # optimizer_config=models.OptimizersConfigDiff(
                #     max_segment_size=COLLECTION_CONFIG.get("optimizer_config", {}).get("max_segment_size", 50000),
                #     default_segment_number=COLLECTION_CONFIG.get("optimizer_config", {}).get("default_segment_number", 2),
                #     indexing_threshold=COLLECTION_CONFIG.get("optimizer_config", {}).get("indexing_threshold", 20000),
                # )
            )

        # Always ensure the required payload index exists for filtering by chapter_id
        # regardless of whether we just created the collection or not
        try:
            # Try to create an index for the chapter_id field to enable filtering
            # According to the Qdrant documentation for payload field indexes
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="chapter_id",
                field_schema=models.KeywordIndexParams()
            )
            print("Created payload index for chapter_id field")
        except Exception as e:
            # This might mean the index already exists, which is fine
            print(f"Payload index for chapter_id may already exist or could not be created: {str(e)}")
            # Don't throw an error, as this is likely just the index already existing
    
    def store_embeddings(self,
                        chapter_id: str,
                        text_chunks: List[str],
                        embeddings: List[List[float]],
                        metadata_list: Optional[List[Dict[str, Any]]] = None):
        """Store text chunks with their embeddings in Qdrant"""
        if metadata_list is None:
            metadata_list = [{}] * len(text_chunks)

        # Generate unique IDs for the points
        point_ids = [str(uuid.uuid4()) for _ in range(len(text_chunks))]

        # Prepare the points to be uploaded
        points = []
        for i, (chunk, embedding, metadata) in enumerate(zip(text_chunks, embeddings, metadata_list)):
            payload = {
                'chapter_id': chapter_id,
                'text': chunk,
                'metadata': metadata
            }
            points.append(
                models.PointStruct(
                    id=point_ids[i],
                    vector=embedding,
                    payload=payload
                )
            )

        # Upload points to Qdrant in batches to be more efficient for free tier
        # Qdrant upload_points accepts batched operations
        self.client.upload_points(
            collection_name=self.collection_name,
            points=points,
            # Use a smaller batch size for free tier
            batch_size=64
        )
    
    def search_similar(self, 
                      query_embedding: List[float], 
                      chapter_filter: Optional[str] = None, 
                      top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar content based on embedding"""
        # Prepare filters if needed
        if chapter_filter:
            filter_condition = models.Filter(
                must=[
                    models.FieldCondition(
                        key="chapter_id",
                        match=models.MatchValue(value=chapter_filter)
                    )
                ]
            )
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=filter_condition,
                limit=top_k
            )
        else:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )
        
        # Format the results
        formatted_results = []
        for result in results:
            payload = result.payload if result.payload else {}
            formatted_results.append({
                'id': result.id,
                'text': payload.get('text', ''),
                'chapter_id': payload.get('chapter_id', ''),
                'metadata': payload.get('metadata', {}),
                'score': result.score
            })
        
        return formatted_results
    
    def delete_by_chapter_id(self, chapter_id: str):
        """Delete all points related to a specific chapter"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="chapter_id",
                            match=models.MatchValue(value=chapter_id)
                        )
                    ]
                )
            )
        )
    
    def count_points(self) -> int:
        """Get the total number of points in the collection"""
        collection_info = self.client.get_collection(self.collection_name)
        return collection_info.points_count or 0

# Global instance of Qdrant service
qdrant_service = QdrantService()