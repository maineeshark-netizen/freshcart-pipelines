from sklearn.datasets import load_iris as sklearn_load_iris


@data_loader
def load_iris(*args, **kwargs):
    iris = sklearn_load_iris(as_frame=True)
    return iris.frame


@test
def test_output(output, *args) -> None:
    assert output is not None
    assert len(output) == 150
    assert 'target' in output.columns
    assert output['target'].nunique() == 3