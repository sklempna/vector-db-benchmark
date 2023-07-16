# import time
# from typing import List, Optional

# from qdrant_client import QdrantClient
# from qdrant_client.http.models import Batch, CollectionStatus

from typing import List, Optional
from engine.base_client.upload import BaseUploader

from engine.clients.chroma.config import CHROMA_COLLECTION_NAME

# from engine.clients.qdrant.config import QDRANT_COLLECTION_NAME

from chromadb.api.models.Collection import Collection
from chromadb.config import Settings
from chromadb import Client


class ChromaUploader(BaseUploader):
    client = None
    upload_params = {}
    collection: Collection = None

    @classmethod
    def init_client(cls, host, distance, connection_params, upload_params):
        # cls.client = QdrantClient(host=host, prefer_grpc=True, **connection_params)
        cls.client = Client(
            Settings(
                chroma_api_impl="rest",
                chroma_server_host=host,
                chroma_server_http_port=connection_params["port"],
            )
        )
        cls.collection = cls.client.get_or_create_collection(CHROMA_COLLECTION_NAME)
        cls.upload_params = upload_params

    # @classmethod
    # def upload_batch(
    #     cls, ids: List[int], vectors: List[list], metadata: Optional[List[dict]]
    # ):
    #     cls.client.upsert(
    #         collection_name=QDRANT_COLLECTION_NAME,
    #         points=Batch.construct(
    #             ids=ids,
    #             vectors=vectors,
    #             payloads=[payload or {} for payload in metadata],
    #         ),
    #     )

    @classmethod
    def upload_batch(
        cls, ids: List[int], vectors: List[list], metadata: Optional[List[dict]]
    ):
        id_strings = [str(elem) for elem in ids]
        cls.collection.add(ids=id_strings, embeddings=vectors)
        # cls.client.upsert(
        #     collection_name=QDRANT_COLLECTION_NAME,
        #     points=Batch.construct(
        #         ids=ids,
        #         vectors=vectors,
        #         payloads=[payload or {} for payload in metadata],
        #     ),
        # )

    # @classmethod
    # def post_upload(cls, _distance):
    #     cls.wait_collection_green()
    #     return {}

    # @classmethod
    # def wait_collection_green(cls):
    #     wait_time = 5.0
    #     total = 0
    #     while True:
    #         time.sleep(wait_time)
    #         total += wait_time
    #         collection_info = cls.client.get_collection(QDRANT_COLLECTION_NAME)
    #         if collection_info.status != CollectionStatus.GREEN:
    #             continue
    #         time.sleep(wait_time)
    #         collection_info = cls.client.get_collection(QDRANT_COLLECTION_NAME)
    #         if collection_info.status == CollectionStatus.GREEN:
    #             break
    #     return total

    @classmethod
    def delete_client(cls):
        if cls.client is not None:
            del cls.client
