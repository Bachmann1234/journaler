from hypothesis import given, assume
from hypothesis import strategies as st
from journaler.models import VALID_MEALS
from journaler.validate import validate_rating, validate_meal
import pytest


@given(st.integers(min_value=1, max_value=5))
def test_valid_ratings(valid_rating):
    # throws exception if invalid
    validate_rating(valid_rating)


@given(st.integers(max_value=0))
def test_too_small_rating(invalid_rating):
    with pytest.raises(ValueError):
        validate_rating(invalid_rating)


@given(st.integers(min_value=6))
def test_too_large_rating(invalid_rating):
    with pytest.raises(ValueError):
        validate_rating(invalid_rating)


@given(st.text())
def test_invalid_meals(invalid):
    assume(invalid not in VALID_MEALS)
    with pytest.raises(ValueError):
        validate_meal(invalid)


@given(st.sampled_from(VALID_MEALS))
def test_valid_meal(meal):
    validate_meal(meal)
