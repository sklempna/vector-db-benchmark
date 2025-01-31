# import multiprocessing as mp
from typing import List, Tuple

# import httpx
# from qdrant_client import QdrantClient
# from qdrant_client.http import models as rest

from engine.base_client.search import BaseSearcher

# from engine.clients.qdrant.config import QDRANT_COLLECTION_NAME

from engine.clients.chroma.config import CHROMA_COLLECTION_NAME
from engine.clients.chroma.config import CHROMA_PORT

# from engine.clients.qdrant.parser import QdrantConditionParser

from chromadb.api.models.Collection import Collection
from chromadb.config import Settings

from chromadb import Client


class ChromaSearcher(BaseSearcher):
    search_params = {}
    client: Client = None
    collection: Collection = None
    # parser = QdrantConditionParser()

    @classmethod
    def init_client(cls, host, distance, connection_params: dict, search_params: dict):
        # cls.client: QdrantClient = QdrantClient(
        #     host,
        #     prefer_grpc=True,
        #     limits=httpx.Limits(max_connections=None, max_keepalive_connections=0),
        #     **connection_params
        # )
        cls.client = Client(
            Settings(
                chroma_api_impl="rest",
                chroma_server_host=host,
                chroma_server_http_port=CHROMA_PORT,
            )
        )
        cls.collection = cls.client.get_collection(CHROMA_COLLECTION_NAME)
        cls.search_params = search_params

    # Uncomment for gRPC
    # @classmethod
    # def get_mp_start_method(cls):
    #     return "forkserver" if "forkserver" in mp.get_all_start_methods() else "spawn"

    @classmethod
    def search_one(cls, vector, meta_conditions, top) -> List[Tuple[int, float]]:
        # res = cls.client.search(
        #     collection_name=QDRANT_COLLECTION_NAME,
        #     query_vector=vector,
        #     query_filter=cls.parser.parse(meta_conditions),
        #     limit=top,
        #     search_params=rest.SearchParams(
        #         **cls.search_params.get("search_params", {})
        #     ),
        # )
        res = cls.collection.query(query_embeddings=[vector], n_results=10)
        return [(res.get("ids")[0][0], res.get("distances")[0][0])]
