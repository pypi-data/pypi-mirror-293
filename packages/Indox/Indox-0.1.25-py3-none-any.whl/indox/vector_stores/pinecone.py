from __future__ import annotations
import os
import uuid
from itertools import islice
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union, Type, TypeVar, Iterator
from indox.vector_stores.utils import maximal_marginal_relevance
import numpy as np
from indox.core import Document, Embeddings, VectorStore
from loguru import logger
import sys

from indox.core.vectorstore import VectorStore

# Set up logging
logger.remove()  # Remove the default logger
logger.add(sys.stdout,
           format="<green>{level}</green>: <level>{message}</level>",
           level="INFO")

logger.add(sys.stdout,
           format="<red>{level}</red>: <level>{message}</level>",
           level="ERROR")
# Last Any should be FieldInfoV1 but this leads to circular imports
T = TypeVar("T", bound=Union[Type, Callable[..., Any], Any])


class DistanceStrategy:
    """Enumerator of the Distance strategies for calculating distances
    between vectors."""

    EUCLIDEAN_DISTANCE = "EUCLIDEAN_DISTANCE"
    MAX_INNER_PRODUCT = "MAX_INNER_PRODUCT"
    DOT_PRODUCT = "DOT_PRODUCT"
    JACCARD = "JACCARD"
    COSINE = "COSINE"


def batch_iterate(size: Optional[int], iterable: Iterable[T]) -> Iterator[List[T]]:
    """Utility batching function.
    Args:
        size: The size of the batch. If None, returns a single batch.
        iterable: The iterable to batch.

    Yields:
        The batches of the iterable.
    """
    it = iter(iterable)
    while True:
        chunk = list(islice(it, size))
        if not chunk:
            return
        yield chunk


class PineconeVectorStore:
    """Pinecone vector store integration.

    """

    # from pinecone import Index

    def __init__(
            self,
            # setting default params to bypass having to pass in
            # the index and embedding objects - manually throw
            # exceptions if they are not passed in or set in environment
            # (keeping param for backwards compatibility)
            index: Optional[Any] = None,
            embedding: Optional[Embeddings] = None,
            text_key: Optional[str] = "text",
            namespace: Optional[str] = None,
            distance_strategy: Optional[DistanceStrategy] = DistanceStrategy.COSINE,
            *,
            pinecone_api_key: Optional[str] = None,
            index_name: Optional[str] = None,
    ):
        if embedding is None:
            raise ValueError("Embedding must be provided")
        self._embedding = embedding
        if text_key is None:
            raise ValueError("Text key must be provided")
        self._text_key = text_key

        self._namespace = namespace
        self.distance_strategy = distance_strategy

        if index:
            # supports old way of initializing externally
            self._index = index
        else:
            # all internal initialization
            _pinecone_api_key = (
                    pinecone_api_key or os.environ.get("PINECONE_API_KEY") or ""
            )
            if not _pinecone_api_key:
                raise ValueError(
                    "Pinecone API key must be provided in either `pinecone_api_key` "
                    "or `PINECONE_API_KEY` environment variable"
                )

            _index_name = index_name or os.environ.get("PINECONE_INDEX_NAME") or ""
            if not _index_name:
                raise ValueError(
                    "Pinecone index name must be provided in either `index_name` "
                    "or `PINECONE_INDEX_NAME` environment variable"
                )

            from pinecone import Pinecone as PineconeClient
            # needs
            client = PineconeClient(api_key=_pinecone_api_key, source_tag="indox")
            self.db = client
            self._index = client.Index(_index_name)

    @property
    def embeddings(self) -> Optional[Embeddings]:
        """Access the query embedding object if available."""
        return self._embedding

    def _add_texts(
            self,
            texts: Iterable[str],
            metadatas: Optional[List[dict]] = None,
            ids: Optional[List[str]] = None,
            namespace: Optional[str] = None,
            batch_size: int = 32,
            embedding_chunk_size: int = 1,
            *,
            async_req: bool = True,
            id_prefix: Optional[str] = None,
            **kwargs: Any,
    ) -> List[str]:
        """Run more texts through the embeddings and add to the vectorstore.

        Upsert optimization is done by chunking the embeddings and upserting them.
        This is done to avoid memory issues and optimize using HTTP based embeddings.
        For OpenAI embeddings, use pool_threads>4 when constructing the pinecone.Index,
        embedding_chunk_size>1000 and batch_size~64 for best performance.
        Args:
            texts: Iterable of strings to add to the vectorstore.
            metadatas: Optional list of metadatas associated with the texts.
            ids: Optional list of ids to associate with the texts.
            namespace: Optional pinecone namespace to add the texts to.
            batch_size: Batch size to use when adding the texts to the vectorstore.
            embedding_chunk_size: Chunk size to use when embedding the texts.
            id_prefix: Optional string to use as an ID prefix when upserting vectors.
            async_req: This parameter determines whether the function call should be asynchronous or synchronous.
             The default value is True.

        Returns:
            List of ids from adding the texts into the vectorstore.

        """
        if namespace is None:
            namespace = self._namespace

        texts = list(texts)
        ids = ids or [str(uuid.uuid4()) for _ in texts]
        if id_prefix:
            ids = [
                id_prefix + "#" + id if id_prefix + "#" not in id else id for id in ids
            ]
        metadatas = metadatas or [{} for _ in texts]
        for metadata, text in zip(metadatas, texts):
            metadata[self._text_key] = text

        # For loops to avoid memory issues and optimize when using HTTP based embeddings
        # The first loop runs the embeddings, it benefits when using OpenAI embeddings
        # The second loops runs the pinecone upsert asynchronously.
        for i in range(0, len(texts), embedding_chunk_size):
            chunk_texts = texts[i: i + embedding_chunk_size]
            chunk_ids = ids[i: i + embedding_chunk_size]
            chunk_metadatas = metadatas[i: i + embedding_chunk_size]
            embeddings = self._embedding.embed_documents(chunk_texts)
            vector_tuples = zip(chunk_ids, embeddings, chunk_metadatas)
            if async_req:
                # Runs the pinecone upsert asynchronously.
                async_res = [
                    self._index.upsert(
                        vectors=batch_vector_tuples,
                        namespace=namespace,
                        async_req=async_req,
                        **kwargs,
                    )
                    for batch_vector_tuples in batch_iterate(batch_size, vector_tuples)
                ]
                [res.get() for res in async_res]
            else:
                self._index.upsert(
                    vectors=vector_tuples,
                    namespace=namespace,
                    async_req=async_req,
                    **kwargs,
                )

        return ids

    def _similarity_search_with_score(
            self,
            query: str,
            k: int = 4,
            filter: Optional[dict] = None,
            namespace: Optional[str] = None,
    ) -> List[Tuple[Document, float]]:
        """Return pinecone documents most similar to query, along with scores.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            filter: Dictionary of argument(s) to filter on metadata
            namespace: Namespace to search in. Default will search in '' namespace.

        Returns:
            List of Documents most similar to the query and score for each
        """
        return self._similarity_search_by_vector_with_score(
            self._embedding.embed_query(query), k=k, filter=filter, namespace=namespace
        )

    def _similarity_search_by_vector_with_score(
            self,
            embedding: List[float],
            *,
            k: int = 4,
            filter: Optional[dict] = None,
            namespace: Optional[str] = None,
    ) -> List[Tuple[Document, float]]:
        """Return pinecone documents most similar to embedding, along with scores."""

        if namespace is None:
            namespace = self._namespace
        docs = []
        results = self._index.query(
            vector=[embedding],
            top_k=k,
            include_metadata=True,
            namespace=namespace,
            filter=filter,
        )
        for res in results["matches"]:
            metadata = res["metadata"]
            if self._text_key in metadata:
                text = metadata.pop(self._text_key)
                score = res["score"]
                docs.append((Document(page_content=text, metadata=metadata), score))
            else:
                logger.warning(
                    f"Found document with no `{self._text_key}` key. Skipping."
                )
        return docs

    def _similarity_search(
            self,
            query: str,
            k: int = 4,
            filter: Optional[dict] = None,
            namespace: Optional[str] = None,
            **kwargs: Any,
    ) -> List[Document]:
        """Return pinecone documents most similar to query.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            filter: Dictionary of argument(s) to filter on metadata
            namespace: Namespace to search in. Default will search in '' namespace.

        Returns:
            List of Documents most similar to the query and score for each
        """
        docs_and_scores = self._similarity_search_with_score(
            query, k=k, filter=filter, namespace=namespace, **kwargs
        )
        return [doc for doc, _ in docs_and_scores]

    def _add_document(self, documents: List[Document], **kwargs: Any) -> list[str]:
        """Run more documents through the embeddings and add to the vectorstore.

        Args:
            documents (List[Document]: Documents to add to the vectorstore.

        Returns:
            List[str]: List of IDs of the added texts.
        """
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        return self._add_texts(texts, metadatas, **kwargs)

    def add(self, docs):
        """
        Adds documents to the PostgreSQL vector store.

        Args:
            docs: The documents to be added to the vector store.
        """
        try:
            if isinstance(docs[0], Document):
                self._add_document(documents=docs)
            else:
                self._add_texts(texts=docs)
            logger.info("Document added successfully to the vector store.")
        except Exception as e:
            logger.error(f"Failed to add document: {e}")
            raise RuntimeError(f"Can't add document to the vector store: {e}")

    def retrieve(self, query: str, top_k: int = 5):
        """
        Retrieves documents similar to the given query from the PostgreSQL vector store.

        Args:
            query (str): The query to retrieve similar documents.
            top_k (int, optional): The number of top similar documents to retrieve. Defaults to 5.

        Returns:
            Tuple[List[str], List[float]]: The context and scores of the retrieved documents.
        """
        retrieved = self._similarity_search_with_score(query, k=top_k)
        context = [d[0].page_content for d in retrieved]
        scores = [d[1] for d in retrieved]
        return context, scores

    @classmethod
    def get_pinecone_index(
            cls,
            index_name: Optional[str],
            pool_threads: int = 4,
            *,
            pinecone_api_key: Optional[str] = None,
    ):
        """Return a Pinecone Index instance.

        Args:
            index_name: Name of the index to use.
            pool_threads: Number of threads to use for index upsert.
        Returns:
            Pinecone Index instance."""
        from pinecone import Pinecone as PineconeClient
        _pinecone_api_key = pinecone_api_key or os.environ.get("PINECONE_API_KEY") or ""
        client = PineconeClient(
            api_key=_pinecone_api_key, pool_threads=pool_threads, source_tag="indox"
        )
        indexes = client.list_indexes()
        index_names = [i.name for i in indexes.index_list["indexes"]]

        if index_name in index_names:
            index = client.Index(index_name)
        elif len(index_names) == 0:
            raise ValueError(
                "No active indexes found in your Pinecone project, "
                "are you sure you're using the right Pinecone API key and Environment? "
                "Please double check your Pinecone dashboard."
            )
        else:
            raise ValueError(
                f"Index '{index_name}' not found in your Pinecone project. "
                f"Did you mean one of the following indexes: {', '.join(index_names)}"
            )
        return index

    @classmethod
    def from_texts(
            cls,
            texts: List[str],
            embedding: Embeddings,
            metadatas: Optional[List[dict]] = None,
            ids: Optional[List[str]] = None,
            batch_size: int = 32,
            text_key: str = "text",
            namespace: Optional[str] = None,
            index_name: Optional[str] = None,
            upsert_kwargs: Optional[dict] = None,
            pool_threads: int = 4,
            embeddings_chunk_size: int = 1000,
            async_req: bool = True,
            *,
            id_prefix: Optional[str] = None,
            **kwargs: Any,
    ) -> PineconeVectorStore:
        """Construct Pinecone wrapper from raw documents.

        This is a user friendly interface that:
            1. Embeds documents.
            2. Adds the documents to a provided Pinecone index

        This is intended to be a quick way to get started.

        The `pool_threads` affects the speed of the upsert operations.

        Setup: set the `PINECONE_API_KEY` environment variable to your Pinecone API key.


        """
        pinecone_index = cls.get_pinecone_index(index_name, pool_threads)
        pinecone = cls(pinecone_index, embedding, text_key, namespace, **kwargs)

        pinecone._add_texts(
            texts,
            metadatas=metadatas,
            ids=ids,
            namespace=namespace,
            batch_size=batch_size,
            embedding_chunk_size=embeddings_chunk_size,
            async_req=async_req,
            id_prefix=id_prefix,
            **(upsert_kwargs or {}),
        )
        return pinecone

    @classmethod
    def from_existing_index(
            cls,
            index_name: str,
            embedding: Embeddings,
            text_key: str = "text",
            namespace: Optional[str] = None,
            pool_threads: int = 4,
    ) -> PineconeVectorStore:
        """Load pinecone vectorstore from index name."""
        pinecone_index = cls.get_pinecone_index(index_name, pool_threads)
        return cls(pinecone_index, embedding, text_key, namespace)

    def delete(
            self,
            ids: Optional[List[str]] = None,
            delete_all: Optional[bool] = None,
            namespace: Optional[str] = None,
            filter: Optional[dict] = None,
            **kwargs: Any,
    ) -> None:
        """Delete by vector IDs or filter.
        Args:
            ids: List of ids to delete.
            filter: Dictionary of conditions to filter vectors to delete.
            delete_all: Delete all documents.
        """

        if namespace is None:
            namespace = self._namespace

        if delete_all:
            self._index.delete(delete_all=True, namespace=namespace, **kwargs)
        elif ids is not None:
            chunk_size = 1000
            for i in range(0, len(ids), chunk_size):
                chunk = ids[i: i + chunk_size]
                self._index.delete(ids=chunk, namespace=namespace, **kwargs)
        elif filter is not None:
            self._index.delete(filter=filter, namespace=namespace, **kwargs)
        else:
            raise ValueError("Either ids, delete_all, or filter must be provided.")

        return None

