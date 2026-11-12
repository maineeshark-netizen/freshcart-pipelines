
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


@transformer
def train_model(df, *args, **kwargs):
    max_depth = int(os.environ.get("MAX_DEPTH", 3))

    train = df[df["split"] == "train"]
    test = df[df["split"] == "test"]

    X_train = train.drop(columns=["target", "split"])
    y_train = train["target"]

    X_test = test.drop(columns=["target", "split"])
    y_test = test["target"]

    model = DecisionTreeClassifier(
        max_depth=max_depth,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("Max depth:", max_depth)
    print("Test accuracy:", accuracy)

    return {
        "model": model,
        "accuracy": accuracy,
        "predictions": predictions.tolist(),
        "y_test": y_test.tolist()
    }


@test
def test_output(output, *args) -> None:
    assert output is not None
    assert output["accuracy"] >= 0.80
