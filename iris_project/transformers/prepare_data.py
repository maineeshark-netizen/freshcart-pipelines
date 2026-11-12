
from mage_ai.data_preparation.decorators import transformer, test
from sklearn.model_selection import train_test_split


@transformer
def transform(df, *args, **kwargs):
    train_idx, test_idx = train_test_split(
        df.index,
        test_size=0.2,
        random_state=42,
        stratify=df["target"]
    )

    out = df.copy()
    out["split"] = "train"
    out.loc[test_idx, "split"] = "test"

    return out


@test
def test_output(output, *args) -> None:
    assert output is not None
    assert len(output) == 150
    assert (output["split"] == "train").sum() == 120
    assert (output["split"] == "test").sum() == 30
