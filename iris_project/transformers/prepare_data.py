
from sklearn.model_selection import train_test_split

try:
    from mage_ai.data_preparation.decorators import transformer
except ImportError:
    def transformer(func):
        return func


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
