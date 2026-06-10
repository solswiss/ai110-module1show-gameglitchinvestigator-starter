from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def test_get_range_for_difficulty_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_get_range_for_difficulty_normal():
    assert get_range_for_difficulty("Normal") == (1, 50)


def test_get_range_for_difficulty_hard():
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_parse_guess_empty():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_invalid():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_float_string():
    ok, value, err = parse_guess("42.0")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_integer_string():
    ok, value, err = parse_guess("17")
    assert ok is True
    assert value == 17
    assert err is None


def test_check_guess_win():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_check_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_check_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_update_score_win_minimum_points():
    assert update_score(0, "Win", 9) == 10


def test_update_score_win_normal_points():
    assert update_score(0, "Win", 2) == 70


def test_update_score_too_high_even_attempt():
    assert update_score(10, "Too High", 2) == 15


def test_update_score_too_high_odd_attempt():
    assert update_score(10, "Too High", 3) == 5


def test_update_score_too_low():
    assert update_score(10, "Too Low", 3) == 5


def test_update_score_unknown_outcome():
    assert update_score(10, "Invalid", 1) == 10
