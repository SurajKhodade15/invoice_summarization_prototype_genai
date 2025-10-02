from typing import List

def precision_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    """
    Precision@k: Fraction of top-k retrieved documents that are relevant.
    """
    retrieved_k = retrieved[:k]
    relevant_set = set(relevant)
    return sum([1 for doc in retrieved_k if doc in relevant_set]) / k if k > 0 else 0.0

def recall_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    """
    Recall@k: Fraction of relevant documents that are in the top-k retrieved.
    """
    retrieved_k = set(retrieved[:k])
    relevant_set = set(relevant)
    return len(retrieved_k & relevant_set) / len(relevant_set) if relevant_set else 0.0
