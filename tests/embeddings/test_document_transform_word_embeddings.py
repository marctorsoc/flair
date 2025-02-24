from typing import Any, Dict, List

from flair.embeddings import (
    DocumentCNNEmbeddings,
    DocumentPoolEmbeddings,
    DocumentRNNEmbeddings,
    FlairEmbeddings,
    TokenEmbeddings,
    WordEmbeddings,
)
from tests.embedding_test_utils import BaseEmbeddingsTest

word: TokenEmbeddings = WordEmbeddings("turian")
flair_embedding: TokenEmbeddings = FlairEmbeddings("news-forward-fast")


class BaseDocumentsViaWordEmbeddingsTest(BaseEmbeddingsTest):
    is_document_embedding = True
    is_token_embedding = False
    base_embeddings: List[TokenEmbeddings] = [word, flair_embedding]

    def create_embedding_from_name(self, name: str):
        """Overwrite this method if it is more complex to load an embedding by name"""
        assert self.name_field is not None
        kwargs = dict(self.default_args)
        kwargs.pop(self.name_field)
        return self.embedding_cls(name, **kwargs)  # type: ignore

    def create_embedding_with_args(self, args: Dict[str, Any]):
        kwargs = dict(self.default_args)
        for k, v in args.items():
            kwargs[k] = v
        return self.embedding_cls(self.base_embeddings, **kwargs)  # type: ignore


class TestDocumentLstmEmbeddings(BaseDocumentsViaWordEmbeddingsTest):
    embedding_cls = DocumentRNNEmbeddings
    default_args = dict(
        hidden_size=128,
        bidirectional=False,
    )
    valid_args = [dict(bidirectional=False), dict(bidirectional=True)]


class TestDocumentPoolEmbeddings(BaseDocumentsViaWordEmbeddingsTest):
    embedding_cls = DocumentPoolEmbeddings
    default_args = dict(
        fine_tune_mode="nonlinear",
    )
    valid_args = [dict(pooling="mean"), dict(pooling="max"), dict(pooling="min")]


class TestDocumentCNNEmbeddings(BaseDocumentsViaWordEmbeddingsTest):
    embedding_cls = DocumentCNNEmbeddings
    default_args = dict(
        kernels=((50, 2), (50, 3)),
    )
    valid_args = [dict(reproject_words_dimension=None), dict(reproject_words_dimension=100)]
