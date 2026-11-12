
import pandas as pd



@data_exporter
def save_results(data, *args, **kwargs):
    results = pd.DataFrame({
        "actual": data["y_test"],
        "predicted": data["predictions"]
    })

    results.to_csv("iris_predictions.csv", index=False)

    print("Model accuracy:", data["accuracy"])
    print("Predictions saved to iris_predictions.csv")

    return results


@test
def test_output(output, *args) -> None:
    assert output is not None
    assert len(output) == 30
    assert "actual" in output.columns
    assert "predicted" in output.columns
