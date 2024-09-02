# krag/evaluators.py

import math  
from typing import Union, List
from krag.document import KragDocument as Document
from korouge_score import rouge_scorer

class OfflineRetrievalEvaluators:
    def __init__(self, actual_docs: List[List[Document]], predicted_docs: List[List[Document]], match_method="text"):
        self.actual_docs = actual_docs 
        self.predicted_docs = predicted_docs  
        self.match_method = match_method  

    def text_match(self, actual_text: str, predicted_text: Union[str, List[str]]) -> bool:
        if isinstance(predicted_text, list):
            return any(actual_text in text for text in predicted_text)
        return actual_text in predicted_text

    def calculate_hit_rate(self, k: int = None) -> float:
        total_queries = len(self.actual_docs)
        full_matches = sum(
            1 for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs)
            if all(self.text_match(actual_doc.page_content, [pred_doc.page_content for pred_doc in predicted_docs[:k]])
                   for actual_doc in actual_docs)
        )
        return full_matches / total_queries if total_queries > 0 else 0.0

    def calculate_mrr(self, k: int = None) -> float:
        cumulative_reciprocal = 0
        Q = len(self.actual_docs)
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            for rank, predicted_doc in enumerate(predicted_docs[:k], start=1):
                if any(self.text_match(actual_doc.page_content, predicted_doc.page_content) for actual_doc in actual_docs):
                    cumulative_reciprocal += 1 / rank
                    break
        return cumulative_reciprocal / Q if Q > 0 else 0.0

    def calculate_recall(self, k: int = None) -> float:
        total_recall = sum(
            sum(1 for actual_doc in actual_docs if self.text_match(actual_doc.page_content, [pred_doc.page_content for pred_doc in predicted_docs[:k]]))
            for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs)
        )
        total_docs = sum(len(actual_docs) for actual_docs in self.actual_docs)
        return total_recall / total_docs if total_docs > 0 else 0.0

    def calculate_precision(self, k: int = None) -> float:
        total_precision = sum(
            sum(
                1 for predicted_text in [pred_doc.page_content for pred_doc in predicted_docs[:k]]
                if any(self.text_match(actual_doc.page_content, predicted_text) for actual_doc in actual_docs)
            ) / len(predicted_docs[:k])
            for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs)
            if len(predicted_docs[:k]) > 0
        )
        total_queries = len(self.actual_docs)
        return total_precision / total_queries if total_queries > 0 else 0.0

    def calculate_map(self, k: int = None) -> float:
        total_map = 0
        total_queries = len(self.actual_docs)
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            num_relevant = 0
            precision_at_i = 0
            for i, predicted_doc in enumerate(predicted_docs[:k], start=1):
                if any(self.text_match(actual_doc.page_content, predicted_doc.page_content) for actual_doc in actual_docs):
                    num_relevant += 1
                    precision_at_i += num_relevant / i
            total_map += precision_at_i / num_relevant if num_relevant > 0 else 0
        return total_map / total_queries if total_queries > 0 else 0.0
    
    def _calculate_dcg(self, relevance_scores: List[float], k: int = None) -> float:
        if k is None:
            k = len(relevance_scores)
        return sum(relevance_scores[i] / math.log2(i + 2) for i in range(min(len(relevance_scores), k)))

    def _convert_ndcg(self, relevance_scores: List[float], k: int = None) -> float:
        if k is None:
            k = len(relevance_scores)
        dcg = self._calculate_dcg(relevance_scores, k)
        idcg = self._calculate_dcg(sorted(relevance_scores, reverse=True), k)
        return dcg / idcg if idcg > 0 else 0.0
    
    def calculate_ndcg(self, k: int = None) -> float:
        total_ndcg = 0
        total_queries = len(self.actual_docs)
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            relevance_scores = [
                max(1 if self.text_match(actual_doc.page_content, pred_doc.page_content) else 0 for actual_doc in actual_docs)
                for pred_doc in predicted_docs[:k]
            ]
            total_ndcg += self._convert_ndcg(relevance_scores, k)
        return total_ndcg / total_queries if total_queries > 0 else 0.0

class RougeOfflineRetrievalEvaluators(OfflineRetrievalEvaluators):
    def __init__(self, actual_docs: List[List[Document]], predicted_docs: List[List[Document]], match_method="rouge1", threshold=0.8):
        super().__init__(actual_docs, predicted_docs, match_method)
        self.threshold = threshold
        self.scorer = rouge_scorer.RougeScorer([match_method], use_stemmer=True)
    
    def text_match(self, actual_text: str, predicted_text: Union[str, List[str]]) -> bool:
        if self.match_method in ["rouge1", "rouge2", "rougeL"]:
            if isinstance(predicted_text, list):
                return any(self.scorer.score(actual_text, text)[self.match_method].fmeasure >= self.threshold for text in predicted_text)
            else:
                score = self.scorer.score(actual_text, predicted_text)[self.match_method].fmeasure
                return score >= self.threshold
        else:
            return super().text_match(actual_text, predicted_text)

    def calculate_ndcg(self, k: int = None) -> float:
        total_ndcg = 0
        total_queries = len(self.actual_docs)
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            relevance_scores = [
                max(self.scorer.score(actual_doc.page_content, pred_doc.page_content)[self.match_method].fmeasure for actual_doc in actual_docs)
                for pred_doc in predicted_docs[:k]
            ]
            total_ndcg += self._convert_ndcg(relevance_scores, k)
        return total_ndcg / total_queries if total_queries > 0 else 0.0
