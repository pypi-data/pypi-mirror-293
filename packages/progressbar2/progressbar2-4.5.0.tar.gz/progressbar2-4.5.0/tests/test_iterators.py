import time

import pytest

import progressbar


def test_list() -> None:
    """Progressbar can guess max_value automatically."""
    p = progressbar.ProgressBar()
    for _i in p(range(10)):
        time.sleep(0.001)


def test_iterator_with_max_value() -> None:
    """Progressbar can't guess max_value."""
    p = progressbar.ProgressBar(max_value=10)
    for _i in p(iter(range(10))):
        time.sleep(0.001)


def test_iterator_without_max_value_error() -> None:
    """Progressbar can't guess max_value."""
    p = progressbar.ProgressBar()

    for _i in p(iter(range(10))):
        time.sleep(0.001)

    assert p.max_value is progressbar.UnknownLength


def test_iterator_without_max_value() -> None:
    """Progressbar can't guess max_value."""
    p = progressbar.ProgressBar(
        widgets=[
            progressbar.AnimatedMarker(),
            progressbar.FormatLabel('%(value)d'),
            progressbar.BouncingBar(),
            progressbar.BouncingBar(marker=progressbar.RotatingMarker()),
        ],
    )
    for _i in p(iter(range(10))):
        time.sleep(0.001)


def test_iterator_with_incorrect_max_value() -> None:
    """Progressbar can't guess max_value."""
    p = progressbar.ProgressBar(max_value=10)
    with pytest.raises(ValueError):
        for _i in p(iter(range(20))):
            time.sleep(0.001)


def test_adding_value() -> None:
    p = progressbar.ProgressBar(max_value=10)
    p.start()
    p.update(5)
    p += 2
    p.increment(2)
    with pytest.raises(ValueError):
        p += 5
