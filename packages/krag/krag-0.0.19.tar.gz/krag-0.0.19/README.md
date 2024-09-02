# Krag

Krag is a Python package designed for evaluating retrieval-augmented generation (RAG) systems. It provides tools to calculate various evaluation metrics such as hit rate, recall, precision, MRR (Mean Reciprocal Rank), MAP (Mean Average Precision), NDCG (Normalized Discounted Cumulative Gain), and more.

Krag는 RAG 시스템(Retrieval-Augmented Generation)을 평가하기 위해 설계된 Python 패키지입니다. Hit Rate, Recall, Precision, MRR(Mean Reciprocal Rank), MAP(Mean Average Precision), NDCG(Normalized Discounted Cumulative Gain) 등 다양한 평가 지표를 계산하는 도구를 제공합니다.

## Installation / 설치 방법

You can install Krag using pip:

```bash
pip install krag
```

## Usage / 사용 예시

Here is a simple example of how to use the `KragDocument` and `OfflineRetrievalEvaluators` classes provided by this package.

다음은 Krag 패키지에서 제공하는 `KragDocument` 및 `OfflineRetrievalEvaluators` 클래스를 사용하는 간단한 예제입니다.

```python
from krag.document import KragDocument
from krag.evaluators import OfflineRetrievalEvaluators

# 각 쿼리에 대한 정답 문서 
actual_docs = [
    # Query 1
    [
        KragDocument(metadata={'id': 1}, page_content='1'),
        KragDocument(metadata={'id': 2}, page_content='2'),
        KragDocument(metadata={'id': 3}, page_content='3'),
    ],
    # Query 2
    [
        KragDocument(metadata={'id': 4}, page_content='4'),
        KragDocument(metadata={'id': 5}, page_content='5'),
        KragDocument(metadata={'id': 6}, page_content='6'),
    ],
    # Query 3
    [
        KragDocument(metadata={'id': 7}, page_content='7'),
        KragDocument(metadata={'id': 8}, page_content='8'),
        KragDocument(metadata={'id': 9}, page_content='9'),
    ],
]

# 각 쿼리에 대한 검색 결과 
predicted_docs = [
    # Query 1
    [
        KragDocument(metadata={'id': 1}, page_content='1'),
        KragDocument(metadata={'id': 4}, page_content='4'),
        KragDocument(metadata={'id': 7}, page_content='7'),
        KragDocument(metadata={'id': 2}, page_content='2'),
        KragDocument(metadata={'id': 5}, page_content='5'),
        KragDocument(metadata={'id': 8}, page_content='8'),
        KragDocument(metadata={'id': 3}, page_content='3'),
        KragDocument(metadata={'id': 6}, page_content='6'),
        KragDocument(metadata={'id': 9}, page_content='9')
    ],

    # Query 2
    [
        KragDocument(metadata={'id': 4}, page_content='4'),
        KragDocument(metadata={'id': 1}, page_content='1'),
        KragDocument(metadata={'id': 7}, page_content='7'),
        KragDocument(metadata={'id': 5}, page_content='5'),
        KragDocument(metadata={'id': 2}, page_content='2'),
        KragDocument(metadata={'id': 8}, page_content='8'),
        KragDocument(metadata={'id': 6}, page_content='6'),
        KragDocument(metadata={'id': 3}, page_content='3'),
        KragDocument(metadata={'id': 9}, page_content='9')
    ],
    
    # Query 3
    [
        KragDocument(metadata={'id': 7}, page_content='7'),
        KragDocument(metadata={'id': 2}, page_content='2'),
        KragDocument(metadata={'id': 4}, page_content='4'),
        KragDocument(metadata={'id': 8}, page_content='8'),
        KragDocument(metadata={'id': 5}, page_content='5'),
        KragDocument(metadata={'id': 3}, page_content='3'),
        KragDocument(metadata={'id': 9}, page_content='9'),
        KragDocument(metadata={'id': 6}, page_content='6'),
        KragDocument(metadata={'id': 1}, page_content='1')
    ]
]

# Initialize the evaluator / 평가도구 초기화 
evaluator = OfflineRetrievalEvaluators(actual_docs, predicted_docs, match_method="text")

# Calculate evaluation metrics / 평가지표 계산 
## k=None (전체 문서)일 때 평가지표 계산
hit_rate_all = evaluator.calculate_hit_rate()
mrr_all = evaluator.calculate_mrr()
recall_all = evaluator.calculate_recall()
precision_all = evaluator.calculate_precision()
map_all = evaluator.calculate_map()
ndcg_all = evaluator.calculate_ndcg()

## k=5일 때 평가지표 계산
hit_rate_at_5 = evaluator.calculate_hit_rate(k=5)
mrr_at_5 = evaluator.calculate_mrr(k=5)
recall_at_5 = evaluator.calculate_recall(k=5)
precision_at_5 = evaluator.calculate_precision(k=5)
map_at_5 = evaluator.calculate_map(k=5)
ndcg_at_5 = evaluator.calculate_ndcg(k=5)

## Print results / 결과 출력
print(f"Hit Rate (All): {hit_rate_all}")
print(f"MRR (All): {mrr_all}")
print(f"Recall (All): {recall_all}")
print(f"Precision (All): {precision_all}")
print(f"MAP (All): {map_all}")
print(f"NDCG (All): {ndcg_all}")

print(f"Hit Rate @5: {hit_rate_at_5}")
print(f"MRR @5: {mrr_at_5}")
print(f"Recall @5: {recall_at_5}")
print(f"Precision @5: {precision_at_5}")
print(f"MAP @5: {map_at_5}")
print(f"NDCG @5: {ndcg_at_5}")
```

### Key Features / 주요 기능

1. **Document Matching (문서 매칭)**:
    - The evaluator provides multiple methods to match actual and predicted documents, including exact text match and ROUGE-based matching (`rouge1`, `rouge2`, `rougeL`).
    - 평가자는 실제 문서와 예측된 문서를 매칭하기 위한 여러 가지 방법을 제공합니다. 여기에는 정확한 텍스트 매칭과 ROUGE 기반 매칭(`rouge1`, `rouge2`, `rougeL`)이 포함됩니다.

2. **Evaluation Metrics (평가지표)**:
    - **Hit Rate**: Measures the proportion of actual documents correctly identified in the predicted set.
    - **Recall**: Evaluates how many relevant documents are present in the top-k predictions.
    - **Precision**: Evaluates the precision of the top-k predictions.
    - **MRR (Mean Reciprocal Rank)**: Averages the reciprocal of the rank of the first relevant document.
    - **MAP (Mean Average Precision)**: Averages precision across top-k ranks where relevant documents appear.
    - **NDCG (Normalized Discounted Cumulative Gain)**: Evaluates the ranking quality considering the order of documents based on relevance scores, with softmax normalization applied when using ROUGE scores.

    - **Hit Rate (적중률)**: 예측된 문서 집합에서 실제 문서가 올바르게 식별된 비율을 측정합니다.
    - **Recall**: 상위 k개의 예측에서 얼마나 많은 관련 문서가 포함되었는지를 평가합니다.
    - **Precision**: 상위 k개의 예측의 정밀도를 평가합니다.
    - **MRR (Mean Reciprocal Rank, 평균 역순위)**: 첫 번째 관련 문서의 순위의 역수를 평균내어 계산합니다.  
    - **MAP (Mean Average Precision)**: 상위 k위 안에 관련 문서가 등장하는 순위에서의 정밀도를 평균냅니다.    
    - **NDCG (Normalized Discounted Cumulative Gain)**: 관련성 점수를 바탕으로 문서 순서를 고려하여 순위 품질을 평가합니다.


3. **ROUGE Score Matching (ROUGE 점수 매칭)**:
    - The `RougeOfflineRetrievalEvaluators` class extends the basic evaluator to use ROUGE scores (`rouge1`, `rouge2`, `rougeL`) for matching and evaluating retrieval quality.
    - `RougeOfflineRetrievalEvaluators` 클래스는 기본 평가자 기능을 확장하여 ROUGE 점수(`rouge1`, `rouge2`, `rougeL`)를 사용한 매칭과 검색 품질 평가를 수행합니다.

#### Example with ROUGE Matching / ROUGE 매칭 사용 예제

```python
from krag.document import KragDocument
from krag.evaluators import RougeOfflineRetrievalEvaluators

# Initialize the evaluator with ROUGE matching / ROUGE 매칭을 사용한 평가도구 초기화 
evaluator = RougeOfflineRetrievalEvaluators(actual_docs, predicted_docs, match_method="rouge1", threshold=0.8)

# Calculate evaluation metrics / 평가지표 계산 
## k=None (전체 문서)일 때 평가지표 계산
hit_rate_all = evaluator.calculate_hit_rate()
mrr_all = evaluator.calculate_mrr()
recall_all = evaluator.calculate_recall()
precision_all = evaluator.calculate_precision()
map_all = evaluator.calculate_map()
ndcg_all = evaluator.calculate_ndcg()

## k=5일 때 평가지표 계산
hit_rate_at_5 = evaluator.calculate_hit_rate(k=5)
mrr_at_5 = evaluator.calculate_mrr(k=5)
recall_at_5 = evaluator.calculate_recall(k=5)
precision_at_5 = evaluator.calculate_precision(k=5)
map_at_5 = evaluator.calculate_map(k=5)
ndcg_at_5 = evaluator.calculate_ndcg(k=5)

## Print results / 결과 출력
print(f"Hit Rate (All): {hit_rate_all}")
print(f"MRR (All): {mrr_all}")
print(f"Recall (All): {recall_all}")
print(f"Precision (All): {precision_all}")
print(f"MAP (All): {map_all}")
print(f"NDCG (All): {ndcg_all}")

print(f"Hit Rate @5: {hit_rate_at_5}")
print(f"MRR @5: {mrr_at_5}")
print(f"Recall @5: {recall_at_5}")
print(f"Precision @5: {precision_at_5}")
print(f"MAP @5: {map_at_5}")
print(f"NDCG @5: {ndcg_at_5}")
```

## License

This project is licensed under the MIT License - see the [MIT License](https://opensource.org/licenses/MIT) for more details.

## Contact

If you have any questions, feel free to reach out via [email](mailto:ontofinances@gmail.com).

---
