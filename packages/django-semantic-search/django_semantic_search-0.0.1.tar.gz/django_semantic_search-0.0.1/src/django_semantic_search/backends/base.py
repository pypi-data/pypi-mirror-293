import abc
from typing import List

from django_semantic_search.documents import VectorIndex


class BaseVectorSearchBackend(abc.ABC):
    """
    Base class for all the vector search backends, such as Qdrant.
    """

    def configure_indexes(self, indexes: List[VectorIndex]):
        """
        Configure the indexes for the backend.
        :param indexes: list of indexes to configure.
        """
        raise NotImplementedError

    def search(self, query: List[float], top_k: int = 10):
        """
        Search for the documents similar to the query vector in the backend.
        :param query:
        :param top_k:
        :return:
        """
        raise NotImplementedError
