
@transformer
def validate_data(df, *args, **kwargs):
    assert df.isnull().sum().sum() == 0, "Missing values found"
    assert df["target"].nunique() == 3, "Expected 3 classes"

    print("No missing values found")
    print("Exactly 3 classes found")

    return df


@test
def test_output(output, *args):
    assert output is not None
    assert output.isnull().sum().sum() == 0
    assert output["target"].nunique() == 3
