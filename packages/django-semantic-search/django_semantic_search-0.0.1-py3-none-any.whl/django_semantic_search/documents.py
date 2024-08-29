import abc
import logging
from functools import cache
from typing import Iterable, List, Optional, Type

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


@cache
def load_default_embedding_model():
    """
    Load the default embedding model, as specified in the settings.
    :return: default embedding model instance.
    """
    semantic_search_settings = settings.SEMANTIC_SEARCH
    model_cls = import_string(semantic_search_settings["default_embeddings"]["model"])
    model_config = semantic_search_settings["default_embeddings"]["configuration"]
    return model_cls(**model_config)


@cache
def load_backend():
    """
    Load the backend, as specified in the settings.
    :return: backend instance.
    """
    semantic_search_settings = settings.SEMANTIC_SEARCH
    backend_cls = import_string(semantic_search_settings["vector_store"]["backend"])
    backend_config = semantic_search_settings["vector_store"]["configuration"]
    return backend_cls(**backend_config)


class VectorIndex:
    """
    A definition of a single vector index. It contains the name of the index and the fields that should be indexed,
    but also allows to surpass the default settings of django-semantic-search.
    """

    def __init__(
        self,
        *fields: str,
        index_name: Optional[str] = None,
    ):
        """
        :param fields: model fields to index together.
        :param index_name: name of the index to use in a backend. By default, it is the concatenation of the fields.
        """
        self.fields: List[str] = list(fields)
        self._index_name = index_name or "_".join(fields)
        self._backend = load_backend()
        self._embedding_model = load_default_embedding_model()

    def validate(self, model_cls: Type[models.Model]):
        """
        Validate the index configuration for the model.
        :param model_cls: model class to validate the index for.
        """
        for field in self.fields:
            if not hasattr(model_cls, field):
                raise ValueError(
                    f"Field {field} is not present in the model {model_cls.__name__}"
                )


class Document(abc.ABC):
    """
    Base class for all the documents. There is a one-to-one mapping between the document subclass and the model class,
    to configure how a specific model instances should be converted to a document.
    """

    def __init__(self):
        self.register_handlers()

    def register_handlers(self):
        """
        Register all the model signals to update the documents in the vector store.
        """

        logger.info(f"Registering handlers for {self.Meta.model}")

        @receiver(models.signals.post_save, sender=self.Meta.model)
        def update_document(sender, instance, **kwargs):
            logger.debug(f"Updating document for {instance}")
            pass

        @receiver(models.signals.post_delete, sender=self.Meta.model)
        def delete_document(sender, instance, **kwargs):
            logger.debug(f"Deleting document for {instance}")
            pass

    class Meta:
        # The model this document is associated with
        model: models.Model = None
        # Namespace for the documents in the vector store, defaults to the model name
        namespace: Optional[str] = None
        # List of vector indexes created out of the model fields
        indexes: Iterable[VectorIndex] = []
        # Model fields that should be included in the metadata
        include_fields: List[str] = ["*"]
        # Flag to disable signals on the model, so the documents are not updated on model changes
        disable_signals: bool = False
