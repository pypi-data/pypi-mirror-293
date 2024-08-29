# This is a reference file for the settings.py file in the django_semantic_search app.
# It contains the default settings for the app.

# TODO: fill the gaps and document each property with inline comments

SEMANTIC_SEARCH = {
    "vector_store": {
        # TODO: use import_string from Django to import the backend class
        "backend": "django_semantic_search.backends.QdrantBackend",
        "configuration": {
            "location": "http://localhost:6333",
        },
    },
    "default_embeddings": {
        "model": "django_semantic_search.embeddings.SentenceTransformerModel",
        "configuration": {
            "model_name": "all-MiniLM-LM6-v2",
        },
    },
}
