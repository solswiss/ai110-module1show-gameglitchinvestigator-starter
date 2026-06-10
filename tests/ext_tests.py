import pytest
from logic_utils import parse_guess, check_guess, update_score

# --- Expected Behavior 1: Out-of-Bounds Inputs Should Be Rejected ---

def test_negative_number_should_be_invalid():
    """
    EXPECTATION: A negative number is outside the difficulty range (e.g., 1 to 50).
    The game must reject it during parsing.
    """
    # Range set to Normal difficulty: 1 to 50
    ok, value, err = parse_guess("-50", low=1, high=50)
    
    assert ok is False
    assert value is None
    assert "out of bounds" in err.lower()


def test_huge_number_should_be_invalid():
    """
    EXPECTATION: An extremely large number is way outside the maximum range (100).
    The game must reject it during parsing.
    """
    # Range set to Hard difficulty: 1 to 100
    ok, value, err = parse_guess("999999", low=1, high=100)
    
    assert ok is False
    assert value is None
    assert "out of bounds" in err.lower()


# --- Expected Behavior 2: Floats/Decimals Should Be Invalid ---

def test_decimal_input_should_be_rejected():
    """
    EXPECTATION: Decimal inputs must be explicitly blocked. The parser shouldn't
    silently truncate them into valid guesses.
    """
    ok, value, err = parse_guess("25.999", low=1, high=50)
    
    assert ok is False
    assert value is None
    assert "decimals are not allowed" in err.lower()


def test_malformed_string_should_be_rejected():
    """
    EXPECTATION: Non-numeric strings or strings with trailing characters must fail.
    """
    ok, value, err = parse_guess("12abc", low=1, high=50)
    
    assert ok is False
    assert value is None
    assert "not a valid number" in err.lower()


# --- Expected Behavior 3: State Protection (Drop Guesses) ---

def test_invalid_guess_signals_app_to_drop_state_changes():
    """
    EXPECTATION: If an input is invalid, ok must return False. This signals app.py
    to completely skip history logging, attempt increments, and score penalties.
    """
    # Testing an out-of-bounds scenario
    ok, value, err = parse_guess("150", low=1, high=100)
    
    # Asserting ok is False guarantees app.py will hit the `if not ok:` branch,
    # which drops the guess safely.
    assert ok is False