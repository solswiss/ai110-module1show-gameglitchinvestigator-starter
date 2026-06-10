# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
- Attempts start at 1
- Hints are backwards
- Guesses with hint toggled only appear in history after the following guess; seems like hints make other elements slow to update
- New Game button does not clear score, history, or banner
- New Game button does not allow another game (forced to reload)
- Show hint occasionally does not register
- Final score does not update upon winning

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|     1 | Go higher hint    | Go lower hint   | N/A                    |
|   100 | Register guess    | Same hist&score | N/A                    |
| New G | New game          | Already won     | N/A                    |

---

## 2. How did you use AI as a teammate?
I initially used Copilot then pivoted to Gemini. Copolit was able to fix glaring issues e.g. the mismatched hints and function refactoring but when I prompted it to ensure show_hint persists with each submission, it was not an effective fix and Copilot neglected to update the value of the hint. I tested the larger fix by running `app.py`.  
With Gemini, I wanted it to one-shot refactoring the code "such that all relevant data updates upon submission and the debug toggle stays open if it was opened", which it completed fine and (as may be expected from Gemini) added some cheeky updates here and there e.g. "An AI-generated guessing game. Fixed up and working smoothly." I first verified Gemini's code by skimming it as I am a little familiar with streamlit's logic, then by runnning `app.py`.

---

## 3. Debugging and testing your fixes
I verified the validity of a fix by reviewing the refactored code (first and most important pass) and then testing functionality live by running `app.py`. Initially, as required, I ran tests with `pytest` and the code passed all 16 tests Copilot wrote itself--mind you, I only asked for "a pytest test case".  
There were no hiccups overall, but I learned that if the overseer (me!) doesn't specify the desired effect, then the AI may not know how best to implement a fix, although the choice may be obvious to a human developer.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
