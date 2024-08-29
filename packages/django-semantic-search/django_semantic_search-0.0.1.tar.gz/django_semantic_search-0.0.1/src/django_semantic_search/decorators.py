from typing import Dict, Type

from django.core.exceptions import ImproperlyConfigured
from django.db import models

from django_semantic_search.documents import Document

# Registry to store the document classes for the models
registry: Dict[Type[models.Model], Document] = {}


def register_document(document_cls: Type[Document]) -> None:
    """
    Register the document class to be used for the specified model.
    :param document_cls: document class to register
    """
    default_meta = Document.Meta
    meta = getattr(document_cls, "Meta", None)
    if meta is None:
        raise ImproperlyConfigured(
            f"Document class {document_cls.__name__} does not have a Meta class."
        )

    # Get the model class from the Meta class of the document
    model_cls = getattr(meta, "model", default_meta.model)

    # Validate all the indexes for the document
    indexes = getattr(meta, "indexes", default_meta.indexes)
    for index in indexes:
        index.validate(model_cls)

    # Check if the model is already registered with a different document
    if model_cls in registry:
        raise ImproperlyConfigured(
            f"Document class for model {model_cls.__name__} is already registered."
        )

    # Finally, register the instantiated document class
    registry[model_cls] = document_cls()
