import pytest
from logic_utils import parse_guess, check_guess, update_score

# --- Expected Behavior 1: Out-of-Bounds Inputs Should Be Rejected ---

def test_negative_number_should_be_invalid():
    """
    EXPECTATION: A negative number is outside any difficulty range (e.g., 1 to 20/50/100).
    The game should recognize this as an invalid guess and reject it during parsing.
    
    NOTE: This test will FAIL on the current code because parse_guess allows '-50'.
    """
    ok, value, err = parse_guess("-50")
    
    assert ok is False, "Game should reject negative numbers as invalid guesses."
    assert "between" in err.lower() or "valid" in err.lower()


def test_huge_number_should_be_invalid():
    """
    EXPECTATION: An extremely large number is way outside the maximum range (100).
    The game should reject it so the player doesn't waste an attempt or lose points.
    
    NOTE: This test will FAIL on the current code because parse_guess allows '999999'.
    """
    ok, value, err = parse_guess("999999")
    
    assert ok is False, "Game should reject numbers outside the difficulty upper bound."


# --- Expected Behavior 2: Floats/Decimals Should Be Invalid ---

def test_decimal_input_should_be_rejected():
    """
    EXPECTATION: This is a whole-number guessing game. If a user inputs a decimal 
    like '25.999', the game should tell them to enter a whole number, rather than 
    silently slicing off the decimal and guessing '25' without their consent.
    
    NOTE: This test will FAIL on the current code because parse_guess secretly converts floats to ints.
    """
    ok, value, err = parse_guess("25.999")
    
    assert ok is False, "Game should reject decimal numbers entirely."
    assert "integer" in err.lower() or "whole number" in err.lower()


# --- Expected Behavior 3: No Score Penalty for Invalid Input Format ---

def test_invalid_guess_does_not_penalize_score():
    """
    EXPECTATION: If a user makes a typo or enters an out-of-bounds number, 
    their score should remain untouched because it wasn't a valid strategic guess.
    
    NOTE: This test will FAIL on the current code because passing a negative number 
    results in a 'Too Low' outcome, which actively docks 5 points from the score.
    """
    initial_score = 100
    
    # Simulate what happens logded inside app.py using the current utility logic
    ok, value, err = parse_guess("-50")
    
    # If the parser mistakenly lets it through as True, we check if check_guess punishes them
    if ok:
        outcome, message = check_guess(value, secret=25)
        new_score = update_score(current_score=initial_score, outcome=outcome, attempt_number=1)
        
        assert new_score == initial_score, "Player score should not decrease on an out-of-bounds input."
    else:
        # If the code was working correctly, ok would be False, meaning we wouldn't even call update_score
        assert True