import uuid
from typing import Dict

from sentence_transformers import SentenceTransformer, util


class SimilarityScorer:
    def __init__(
        self,
        model: str = "paraphrase-multilingual-MiniLM-L12-v2",
    ) -> None:
        self.model = SentenceTransformer(model)
        self.model_name = model

    def compute_similarity_matrix(
        self, query_sents: Dict[uuid.UUID, str]
    ) -> Dict[str, list]:
        ids = list(query_sents.keys())
        query_embeddings = self.model.encode(list(query_sents.values()))
        similarity_matrix = util.cos_sim(
            query_embeddings, query_embeddings
        ).tolist()
        return {"ids": ids, "matrix": similarity_matrix}
