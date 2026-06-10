import pytest
from utils.validators import validate_keys


# --- Normal cases ---

def test_validate_keys_all_present():
    """All required keys exist in the data — should pass silently."""
    data = {"id": 1, "title": "hello", "userId": 2}
    validate_keys(data, ["id", "title", "userId"])


def test_validate_keys_subset():
    """Only a subset of keys required — extra keys in data are fine."""
    data = {"id": 1, "title": "hello", "body": "extra field", "userId": 2}
    validate_keys(data, ["id", "title"])


def test_validate_keys_single_key():
    """Single required key present."""
    data = {"status": "ok"}
    validate_keys(data, ["status"])


# --- Edge cases ---

def test_validate_keys_empty_key_list():
    """Empty required keys list — nothing to check, always passes."""
    data = {"id": 1}
    validate_keys(data, [])


def test_validate_keys_empty_data_no_keys_required():
    """Empty data, no keys required — should pass."""
    validate_keys({}, [])


# --- Failure cases ---

def test_validate_keys_missing_one_key():
    """One required key is absent — should raise AssertionError."""
    data = {"id": 1, "title": "hello"}
    with pytest.raises(AssertionError):
        validate_keys(data, ["id", "title", "userId"])


def test_validate_keys_all_keys_missing():
    """All required keys are absent — should raise AssertionError."""
    data = {"irrelevant": "value"}
    with pytest.raises(AssertionError):
        validate_keys(data, ["id", "title", "userId"])


def test_validate_keys_empty_data_with_required_keys():
    """Empty data dict but keys are required — should raise AssertionError."""
    with pytest.raises(AssertionError):
        validate_keys({}, ["id"])


# --- Parametrized cases ---

@pytest.mark.parametrize("data, keys", [
    ({"id": 1, "title": "a", "userId": 1}, ["id", "title", "userId"]),
    ({"id": 2, "body": "b"}, ["id", "body"]),
    ({"userId": 3}, ["userId"]),
])
def test_validate_keys_parametrized_valid(data, keys):
    """Parametrized: multiple valid data/key combinations."""
    validate_keys(data, keys)


@pytest.mark.parametrize("data, keys", [
    ({}, ["id"]),
    ({"title": "hello"}, ["id", "title"]),
    ({"userId": 1}, ["id", "title", "userId"]),
])
def test_validate_keys_parametrized_invalid(data, keys):
    """Parametrized: multiple missing-key scenarios all raise AssertionError."""
    with pytest.raises(AssertionError):
        validate_keys(data, keys)
