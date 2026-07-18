"""Sixty-second tour of debatekit.

    python examples/quickstart.py
"""
from debatekit.agents import Agent
from debatekit.debate import run_debate

correct = "1989"
distractors = ["1991", "1987", "1990"]

# Five mediocre agents, each right about 55% of the time on their own.
panel = [Agent(f"agent{i}", accuracy=0.55, seed=i) for i in range(5)]

result = run_debate(panel, correct, distractors, rounds=2)

print(f"round 0 (independent): {result.rounds[0]}")
print(f"round 1 (revised):     {result.rounds[1]}")
print(f"round 2 (revised):     {result.rounds[2]}")
print(f"final answer: {result.final_answer}  (correct: {result.correct})")
print(f"agents that switched an answer during debate: {result.switched_count}")
