from benchmark.dataset import Dataset
from engine.base_client.configure import BaseConfigurator
from engine.clients.chroma.config import CHROMA_COLLECTION_NAME
from engine.clients.chroma.config import CHROMA_PORT

from chromadb.config import Settings
from chromadb import Client


class ChromaConfigurator(BaseConfigurator):
    def __init__(self, host, collection_params: dict, connection_params: dict):
        super().__init__(host, collection_params, connection_params)

        self.client = Client(
            Settings(
                chroma_api_impl="rest",
                chroma_server_host=host,
                chroma_server_http_port=CHROMA_PORT,
            )
        )

    def clean(self):
        self.client.delete_collection(CHROMA_COLLECTION_NAME)

    def recreate(self, dataset: Dataset, collection_params):
        self.client.create_collection(CHROMA_COLLECTION_NAME)
