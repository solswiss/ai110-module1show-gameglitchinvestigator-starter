# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience
Enter with the goal of fixing an AI-generated Streamlit secret number guessing game with scoring and hint mechanisms.  
Begin fixing glaring issues: reversed hints, mismatched difficulty settings, and faulty stats updates with Copilot.
Dive deeper into logic flow and refactor to process guesses first and update interface afterwards with Gemini.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User enters a guess of 1 → hint "Too Low"
2. User enters a guess of 100 → hint "Too High"
3. Score updates after each guess
4. Game ends after the correct guess or user exhausts tries
5. User starts a new game with difficulty selection

## 🧪 Test Results

```
tests\test_game_logic.py ................                              [100%]

============================ 16 passed in 0.13s =============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
