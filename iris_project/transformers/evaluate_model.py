
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
import pandas as pd


@transformer
def evaluate_model(data, *args, **kwargs):
    y_test = data["y_test"]
    predictions = data["predictions"]

    cm = confusion_matrix(y_test, predictions)

    metrics = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1-score"],
        "Score": [
            accuracy_score(y_test, predictions),
            precision_score(y_test, predictions, average="weighted", zero_division=0),
            recall_score(y_test, predictions, average="weighted", zero_division=0),
            f1_score(y_test, predictions, average="weighted", zero_division=0)
        ]
    })

    print("Confusion Matrix:")
    print(cm)

    print("\nEvaluation Metrics:")
    print(metrics.to_string(index=False))

    return {
        "confusion_matrix": cm,
        "metrics": metrics
    }


@test
def test_output(output, *args):
    assert output is not None
