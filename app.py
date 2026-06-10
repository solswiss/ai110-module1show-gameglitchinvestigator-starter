import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Fixed up and working smoothly.")

#FIX: Refactored structure for live updates with top-down streamlit logic
# --- 1. SESSION STATE INITIALIZATION ---
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "last_message" not in st.session_state:
    st.session_state.last_message = None

# Track whether debug expander is open across reruns
if "debug_expanded" not in st.session_state:
    st.session_state.debug_expanded = False

# --- 2. SIDEBAR & CONFIGURATION ---
st.sidebar.header("Settings")

#FIX: Refactored difficulty scaling
difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)
#FIX: Refactored difficulty scaling, cont.
attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty) #FIX: Refactored logic into logic_utils.py using agent mode

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Initialize secret based on the selected difficulty range
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# --- 3. CALLBACK FUNCTIONS ---
def submit_logic(low_bound: int, high_bound: int):
    # Fetch the input value directly from session state via its key
    user_guess = st.session_state.get(f"guess_input_{difficulty}", "")
    
    if not user_guess.strip():
        st.session_state.last_message = "Please enter a valid guess before submitting!"
        return

    # Pass the explicitly provided bounds to our strict parser
    ok, guess_int, err = parse_guess(user_guess, low_bound, high_bound) 

    if not ok:
        st.session_state.last_message = err
        return  # Short-circuit immediately! No history, no score penalization.

    # --- Valid Guess Logic ---
    st.session_state.attempts += 1
    secret = st.session_state.secret
    
    # Calculate distance metrics for tracking if they are getting closer
    current_diff = abs(guess_int - secret)
    prev_diff = None
    
    if len(st.session_state.history) > 0:
        # Get the absolute difference of their last valid guess
        last_valid_guess = st.session_state.history[-1]
        prev_diff = abs(last_valid_guess - secret)

    # Log the valid integer to history
    st.session_state.history.append(guess_int)
    
    outcome, message = check_guess(guess_int, secret) 
    st.session_state.last_message = message

    # Update score using our hot/cold progression logic
    st.session_state.score = update_score(
        current_score=st.session_state.score,
        outcome=outcome,
        attempt_number=st.session_state.attempts,
        current_diff=current_diff,
        prev_diff=prev_diff
    )

    if outcome == "Win":
        st.session_state.status = "won"
    else:
        if st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"

    # Clear input field box text for the next round
    st.session_state[f"guess_input_{difficulty}"] = ""


def reset_game():
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_message = None


# --- 4. GAME MAIN LAYOUT ---
st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

with st.expander("Developer Debug Info", expanded=st.session_state.debug_expanded):
    st.checkbox("Keep Debug Info visible", key="debug_expanded")
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

# Control Elements Row
col1, col2, col3 = st.columns(3)
with col1:
    # FIX: Pass 'low' and 'high' explicitly via args to guarantee they match the sidebar configuration state!
    st.button("Submit Guess 🚀", key="submit_guess", on_click=submit_logic, args=(low, high))
with col2:
    st.button("New Game 🔁", key="new_game", on_click=reset_game)
with col3:
    show_hint = st.checkbox("Show hint", value=True, key="show_hint")

# --- 5. AFTER-ACTION GAME MESSAGES ---
if show_hint and st.session_state.last_message is not None:
    # Match layout colors cleanly to feedback type
    if st.session_state.status == "won":
        st.success(f"🎉 You won! The secret was {st.session_state.secret}. Final score: {st.session_state.score}")
        st.balloons()
    elif st.session_state.status == "lost":
        st.error(f"❌ Out of attempts! The secret was {st.session_state.secret}. Score: {st.session_state.score}")
    else:
        st.warning(st.session_state.last_message)

# Stop execution if game state is over
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

st.divider()
st.caption("Refactored to align seamlessly with Streamlit's top-to-bottom lifecycle.")