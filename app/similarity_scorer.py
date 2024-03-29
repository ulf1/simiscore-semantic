import uuid
from typing import Dict

import sentence_transformers as sbert


class SimilarityScorer:
    """Computes similarity scores between text strings"""

    def __init__(
        self,
        model: str = "paraphrase-multilingual-MiniLM-L12-v2",
    ) -> None:
        self._model = sbert.SentenceTransformer(model)
        self._model_name = model

    @property
    def model_name(self) -> str:
        return self._model_name

    def compute_similarity_matrix(
        self, query_sents: Dict[uuid.UUID, str]
    ) -> Dict[str, list]:
        """
        Compute similarity scores for sequence of text strings.

        Parameters:
            query_sents: Union[dict, list]
                Sequence of text strings to be processed.
        Returns: Dict[str, list]
            A dictionary storing sentence ids and the similarity matrix.
        """
        ids = list(query_sents.keys())
        query_embeddings = self._model.encode(list(query_sents.values()))
        similarity_matrix = sbert.util.cos_sim(
            query_embeddings, query_embeddings
        ).tolist()
        return {"ids": ids, "matrix": similarity_matrix}
