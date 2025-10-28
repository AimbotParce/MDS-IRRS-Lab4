import math
from functools import cache
from typing import Dict, List

from elasticsearch import AsyncElasticsearch, Elasticsearch


class TFIDFVectorizer:
    def __init__(self, es_client: Elasticsearch, index_name: str, analyzer_name: str):
        self.client = es_client
        self.index_name = index_name
        self.analyzer_name = analyzer_name

    def tokenize(self, text: str) -> List[str]:
        """
        given query string it outputs the list of preprocessed tokens from it
        using same analyzer (preprocessing pipeline) than the arxiv abstracts
        """

        # Use the analyze API on the specified index
        response = self.client.indices.analyze(
            index=self.index_name, body={"analyzer": self.analyzer_name, "text": text}
        )

        # Extract just the token strings from the response
        preprocessed_terms = [token_info["token"] for token_info in response["tokens"]]
        return preprocessed_terms

    @cache
    def doc_count(self) -> int:
        """Returns the number of documents in the index."""
        response = self.client.count(index=self.index_name)
        return response["count"]

    def _doc_terms_info(self, doc_id: str) -> Dict[str, Dict[str, int]]:
        """Retrieves term statistics for the specified document."""
        response = self.client.termvectors(
            index=self.index_name,
            id=doc_id,
            fields=["text"],
            term_statistics=True,
            positions=False,
            offsets=False,
            payloads=False,
        )
        terms_info = response.get("term_vectors", {}).get("text", {}).get("terms", {})
        return terms_info

    def _text_terms_info(self, text: str) -> Dict[str, Dict[str, int]]:
        """Retrieves term statistics for the given text."""
        response = self.client.termvectors(
            index=self.index_name,
            doc={"text": text},
            fields=["text"],
            term_statistics=True,
            positions=False,
            offsets=False,
            payloads=False,
        )
        terms_info = response.get("term_vectors", {}).get("text", {}).get("terms", {})
        return terms_info

    def tf_idf_document(self, doc_id: str) -> Dict[str, float]:
        """Computes the TF-IDF weights for terms in the specified document."""

        tf_idf_weights = {}
        doc_count = self.doc_count()
        terms_info = self._doc_terms_info(doc_id)
        for term, stats in terms_info.items():
            tf = stats.get("term_freq", 0)
            df = stats.get("doc_freq", 1)  # avoid division by zero
            idf = math.log2(doc_count / df)
            tf_idf_weights[term] = tf * idf

        return tf_idf_weights

    def tf_idf_text(self, text: str) -> Dict[str, float]:
        """Computes the TF-IDF weights for terms in the text."""
        tf_idf_weights = {}
        doc_count = self.doc_count()
        terms_info = self._text_terms_info(text)
        for term, stats in terms_info.items():
            tf = stats.get("term_freq", 0)
            df = stats.get("doc_freq", 1)  # avoid division by zero
            idf = math.log2(doc_count / df)
            tf_idf_weights[term] = tf * idf

        return tf_idf_weights


class AsyncTFIDFVectorizer:
    def __init__(self, es_client: AsyncElasticsearch, index_name: str, analyzer_name: str):
        self.client = es_client
        self.index_name = index_name
        self.analyzer_name = analyzer_name

    async def tokenize(self, text: str) -> List[str]:
        """
        given query string it outputs the list of preprocessed tokens from it
        using same analyzer (preprocessing pipeline) than the arxiv abstracts
        """

        # Use the analyze API on the specified index
        response = await self.client.indices.analyze(
            index=self.index_name, body={"analyzer": self.analyzer_name, "text": text}
        )

        # Extract just the token strings from the response
        preprocessed_terms = [token_info["token"] for token_info in response["tokens"]]
        return preprocessed_terms

    async def doc_count(self) -> int:
        """Returns the number of documents in the index."""
        response = await self.client.count(index=self.index_name)
        return response["count"]

    async def _doc_terms_info(self, doc_id: str) -> Dict[str, Dict[str, int]]:
        """Retrieves term statistics for the specified document."""
        response = await self.client.termvectors(
            index=self.index_name,
            id=doc_id,
            fields=["text"],
            term_statistics=True,
            positions=False,
            offsets=False,
            payloads=False,
        )
        terms_info = response.get("term_vectors", {}).get("text", {}).get("terms", {})
        return terms_info

    async def _text_terms_info(self, text: str) -> Dict[str, Dict[str, int]]:
        """Retrieves term statistics for the given text."""
        response = await self.client.termvectors(
            index=self.index_name,
            doc={"text": text},
            fields=["text"],
            term_statistics=True,
            positions=False,
            offsets=False,
            payloads=False,
        )
        terms_info = response.get("term_vectors", {}).get("text", {}).get("terms", {})
        return terms_info

    async def tf_idf_document(self, doc_id: str) -> Dict[str, float]:
        """Computes the TF-IDF weights for terms in the specified document."""

        tf_idf_weights = {}
        doc_count = await self.doc_count()
        terms_info = await self._doc_terms_info(doc_id)
        for term, stats in terms_info.items():
            tf = stats.get("term_freq", 0)
            df = stats.get("doc_freq", 1)  # avoid division by zero
            idf = math.log2(doc_count / df)
            tf_idf_weights[term] = tf * idf

        return tf_idf_weights

    async def tf_idf_text(self, text: str) -> Dict[str, float]:
        """Computes the TF-IDF weights for terms in the text."""
        tf_idf_weights = {}
        doc_count = await self.doc_count()
        terms_info = await self._text_terms_info(text)
        for term, stats in terms_info.items():
            tf = stats.get("term_freq", 0)
            df = stats.get("doc_freq", 1)  # avoid division by zero
            idf = math.log2(doc_count / df)
            tf_idf_weights[term] = tf * idf

        return tf_idf_weights
