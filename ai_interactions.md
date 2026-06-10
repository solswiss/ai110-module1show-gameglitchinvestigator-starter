# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**
Challenge 1:
1. identify three potential "edge case" inputs (e.g., negative numbers, 
decimals, or extremely large values) that might still break the game, but do not modify the code. generate a suite of pytest cases that verify your game handles these inputs gracefully.
2. generate the tests again but with the goal of checking the game behaves as one would expect (e.g. the edge cases do not pass because the code is buggy) -- not to check if the code behaves as one would expect the code to.

**What did the agent do?**
Challenge 1: write a new file comprised of tests for expected behavior.

**What did you have to verify or fix manually?**
Challenge 1: I had to prompt the agent again to correct its line of thinking.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| negative number guess | see Challenge 1 prompts above | `test_negative_number_should_be_invalid` | X | `parse_guess` does not check negative values against the (positive) range |
| massive guess | see Challenge 1 prompts above | `test_huge_number_should_be_invalid` | X | `parse_guess` does not check values against the range |
| decimal number guess | see Challenge 1 prompts above | `test_decimal_input_should_be_rejected` | X | `parse_guess` truncates decimal value guesses instead of rejecting them |
| invalid guess | see Challenge 1 prompts above | `test_invalid_guess_does_not_penalize_score` | X | the code detracts points regardless of validity of the guess instead of dropping the guess entirely |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
