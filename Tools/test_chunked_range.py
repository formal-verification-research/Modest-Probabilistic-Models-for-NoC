import pytest

from Tools.chunked_range import chunked_range


def _to_list_of_lists(gen):
    return [list(r) for r in gen]


def test_example_chunking():
    got = _to_list_of_lists(chunked_range(0, 15, 2, 5))
    assert got == [[0, 2, 4, 6, 8], [10, 12, 14]]


def test_single_chunk_when_chunk_large():
    # chunk large enough to hold all produced elements -> single yielded range
    got = _to_list_of_lists(chunked_range(1, 10, 3, 10))
    assert got == [[1, 4, 7]]


def test_invalid_parameters_raise():
    with pytest.raises(ValueError):
        list(chunked_range(5, 5, 1, 1))
    with pytest.raises(ValueError):
        list(chunked_range(0, 10, 0, 2))
    with pytest.raises(ValueError):
        list(chunked_range(0, 10, 1, 0))
    with pytest.raises(TypeError):
        list(chunked_range(0.0, 10, 1, 2))
