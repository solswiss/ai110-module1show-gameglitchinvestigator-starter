import random
import streamlit as st
import pandas as pd
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


def get_random_emoticon(category: str) -> str:
    """Retrieve a random, theme-appropriate Kaomoji emoticon based on game state.

    Args:
        category: The current game outcome category. Acceptable options are
            "warmer", "colder", "win", or "lose".

    Returns:
        A string containing a single, randomly chosen emoticon from the matching
        category list. Returns an empty string if an unknown category is passed.
    """
    emoticons = {
        "warmer": [
            "(👍ᐛ )👍", "★⌒ヽ(╹꒳╹)", "✧٩(•⌄•๑)", "٩( ‘ω’ )و", "(⌒▽⌒)☆", "ヽ(o^ ^o)ﾉ"
        ],
        "colder": [
            "(⊙_◎)", "ヾ(°ロ°)ﾂ", "Σ(O_O)", "(•ิ_•ิ)?", "〜(＞＜)〜"
        ],
        "lose": [
            "(T_T)", "(￣ ￣|||)", "(＃＞＜)", "(´･_･｀)", "( ；∀；)", 
            "（；へ：）"
        ],
        "win": [
            "( ✪ワ✪)ノʸᵉᵃʰᵎ", "ヾ(・∀・*)ゝ♪", 
            "⋆ ˚｡⋆˚⸜(♡ ॑ᗜ ॑♡)⸝ ˚⋆｡˚ ⋆", "✿♬ﾟ+.(｡◡‿◡)♪.+ﾟ♬✿。", 
            "＼\ ٩( ᐛ )و /／"
        ]
    }

    # Standardize to lowercase to prevent casing mismatches
    normalized_category = category.lower()

    if normalized_category in emoticons:
        return random.choice(emoticons[normalized_category])
    
    return ""

# --- 1. THEME INITIALIZATION (CSS Injection) ---
st.set_page_config(page_title="NumGuesser", page_icon="🧸", layout="centered")

# Custom injection using your exact color scheme
st.markdown(f"""
    <style>
    /* Main Background & Text Color Defaults */
    .stApp {{
    }}
    
    /* Headers & Subheaders */
    h1, h2, h3, h4, h5, h6, .stSubheader {{
        color: #4F252E !important;
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #FFF7C5 !important;
        border: none;
        border-radius: 0 16px 16px 0;
        box-shadow: none;
    }}
    
    /* Style Main Buttons */
    div.stButton > button:first-child {{
        background-color: #4F252E !important;
        color: #FFF7C5 !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }}
    div.stButton > button:first-child:hover {{
        color: #F4AE52 !important;
    }}
    
    /* Custom game alert banners */
    .game-banner {{
        padding: 8px 12px;
        border: none;
        border-left: 4px solid #F4AE52;
        border-radius: 0;
        margin-bottom: 15px;
        font-size: 1.2rem;
    }}
    .banner-warmer {{
        background-color: #FFF7C5 !important;
        color: #4F252E !important;
    }}
    .banner-colder {{
        background-color: #FFF7C5 !important;
        color: #4F252E !important;
    }}
    .banner-neutral {{
        background-color: #FFF7C5 !important;
        color: #4F252E !important;
    }}
    </style>
        
    <img src="https://123emoji.com/wp-content/uploads/2017/08/sticker-3-163.png" style="position: fixed; right: 0; bottom: 0; z-index: 10;"/>
""", unsafe_allow_html=True)


# --- 2. SESSION STATE INITIALIZATION ---
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

if "hint_type" not in st.session_state:
    st.session_state.hint_type = "neutral"  # Tracking "warmer", "colder", or "neutral"

if "debug_expanded" not in st.session_state:
    st.session_state.debug_expanded = False


# --- 3. SIDEBAR & CONFIGURATION ---
st.sidebar.header("⚙️ Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.markdown(f"""
---
* **Range:** `{low}` to `{high}`
* **Allowed Attempts:** `{attempt_limit}`
""")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)


# --- 4. CALLBACK FUNCTIONS ---
def submit_logic(low_bound: int, high_bound: int):
    # Check Win/Loss states to halt runtime gracefully
    if st.session_state.status != "playing":
        hint_banner.markdown(
                f"<div class='game-banner banner-neutral '>Start a new game to play again!</div>", 
                unsafe_allow_html=True
            )
        st.stop()
        if st.session_state.status == "won":
            st.balloons()

    user_guess = st.session_state.get(f"guess_input_{difficulty}", "")
    
    if not user_guess.strip():
        st.session_state.last_message = "Please enter a valid guess before submitting!"
        st.session_state.hint_type = "neutral"
        return

    ok, guess_int, err = parse_guess(user_guess, low_bound, high_bound) 

    if not ok or guess_int is None:
        st.session_state.last_message = err
        st.session_state.hint_type = "neutral"
        return

    st.session_state.attempts += 1
    secret = st.session_state.secret
    
    current_diff = abs(guess_int - secret)
    prev_diff = None
    
    if len(st.session_state.history) > 0:
        last_valid_guess = st.session_state.history[-1]
        prev_diff = abs(last_valid_guess - secret)

    st.session_state.history.append(guess_int)
    outcome, message = check_guess(guess_int, secret) 
    
    # Assess Temperature Trend
    if outcome == "Win":
        st.session_state.hint_type = "warmer"
        st.session_state.last_message = f"{message} {get_random_emoticon("win")}"
    elif prev_diff is None:
        st.session_state.hint_type = "neutral"
        st.session_state.last_message = f"{message} {get_random_emoticon("warmer")}"
    elif current_diff < prev_diff:
        st.session_state.hint_type = "warmer"
        st.session_state.last_message = f"{message} (Getting Warmer!) {get_random_emoticon("warmer")}"
    else:
        st.session_state.hint_type = "colder"
        st.session_state.last_message = f"{message} (Getting Colder!) {get_random_emoticon("colder")}"

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

    st.session_state[f"guess_input_{difficulty}"] = ""


def reset_game():
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_message = None
    st.session_state.hint_type = "neutral"


# --- 5. GAME MAIN LAYOUT ---
st.title("NumGuessr: Cafe Edition")
st.subheader("Make a guess")

# Interactive Round Stats Info Bar
st.markdown(
    f"<div class='game-banner banner-neutral'>"
    f"Target Bounds: <strong>{low} to {high}</strong> | "
    f"Attempts: <strong>{st.session_state.attempts}/{attempt_limit}</strong>"
    f"</div>", 
    unsafe_allow_html=True
)

# Text Field
st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

# Control Elements Row
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Submit Guess 🚀", key="submit_guess", on_click=submit_logic, args=(low, high))
with col2:
    st.button("New Game 🔁", key="new_game", on_click=reset_game)
with col3:
    show_hint = st.checkbox("Show hint", value=True, key="show_hint")

# End Banner
finale_banner = st.empty()

# Hint Banner
hint_banner = st.empty()

# History Chart
history_container = st.empty()

# Debug Expander
debug_tab = st.expander("Developer Debug Info", type="compact", on_change="rerun", expanded=st.session_state.debug_expanded)
with debug_tab:
    st.write("Secret Target:", st.session_state.secret)
    st.write("Current Score:", st.session_state.score)
    st.write("Guess Trail:", st.session_state.history)

# --- 6. AFTER-ACTION COLOR-CODED HOT/COLD FEEDBACK ---
if show_hint and st.session_state.last_message is not None:
    if st.session_state.status == "won":
        finale_banner.markdown(
            f"<div class='game-banner banner-neutral '>You won! {get_random_emoticon("win")} Secret: {st.session_state.secret} | Final score: {st.session_state.score}</div>", 
            unsafe_allow_html=True
        )
    elif st.session_state.status == "lost":
        finale_banner.markdown(
            f"<div class='game-banner banner-neutral '>Out of attempts! {get_random_emoticon("lose")} Secret: {st.session_state.secret} | Final score: {st.session_state.score}</div>", 
            unsafe_allow_html=True
        )
    else:
        # Dynamic style classes matching our hex specifications
        # if st.session_state.hint_type == "warmer":
        #     banner_style = "banner-warmer"
        # elif st.session_state.hint_type == "colder":
        #     banner_style = "banner-colder"
        # else:
        #     banner_style = "banner-neutral"

        hint_banner.markdown(
            f"<div class='game-banner banner-neutral'>{st.session_state.last_message}</div>", 
            unsafe_allow_html=True
        )


# --- 7. LIVE UPDATING SUMMARY CHART ---
if len(st.session_state.history) > 0:
    if debug_tab.open:
        # Process history vectors into structural dataframe
        chart_data = pd.DataFrame({
            "Attempt": range(1, len(st.session_state.history) + 1),
            "Your Guess": st.session_state.history,
            "Secret Target": [st.session_state.secret] * len(st.session_state.history)
        }).set_index("Attempt")

        # Display line chart tracing progression against the target threshold
        history_container.line_chart(chart_data, color=["#4F252E", "#F4AE52"])
    else:
        # Process history vectors into structural dataframe
        chart_data = pd.DataFrame({
            "Attempt": range(1, len(st.session_state.history) + 1),
            "Your Guess": st.session_state.history
        }).set_index("Attempt")

        # Display line chart tracing progression against the target threshold
        history_container.line_chart(chart_data, color="#4F252E")
