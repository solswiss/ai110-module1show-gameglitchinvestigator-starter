def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str, low: int, high: int):
    """Strictly parse user input into an int guess within the allowed bounds."""
    if raw is None or not raw.strip():
        return False, None, "Please enter a guess."

    clean_raw = raw.strip()

    if "." in clean_raw:
        return False, None, f"Decimals are not allowed. Please enter a whole number between {low} and {high}."

    try:
        value = int(clean_raw)
    except ValueError:
        return False, None, "That is not a valid number. Please enter digits only."

    if value < low or value > high:
        return False, None, f"Out of bounds! Your guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """Compare guess to secret and return (outcome, message)."""
    try:
        secret_value = int(secret)
    except (TypeError, ValueError):
        secret_value = secret

    if guess == secret_value:
        return "Win", "🎉 Correct!"
    if guess > secret_value:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int, current_diff: int = None, prev_diff: int = None):
    """
    Update score dynamically:
    - Winning grants a massive completion bonus.
    - If it's the first guess, no trend exists (0 points).
    - If the user gets closer to the secret, award +5 points.
    - If the user gets farther away (or stays exactly as far away), deduct -5 points.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        return current_score + max(points, 10)

    # If there's no previous guess to compare against, score doesn't change yet
    if current_diff is None or prev_diff is None:
        return current_score

    # Logical validation: Did the distance shrink?
    if current_diff < prev_diff:
        return current_score + 5  # Warmer!
    else:
        return current_score - 5  # Colder or stagnated