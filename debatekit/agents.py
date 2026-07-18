"""Noisy agents: each one answers correctly with some fixed probability, and
wrong answers are drawn from a set of plausible distractors.

This is a deliberately simple model of what a real LLM looks like on a hard
question: right more often than wrong, but not perfectly, and wrong in ways
that cluster around a handful of plausible-but-incorrect answers rather than
being uniformly random. That clustering matters: it is what makes majority
voting work at all. If wrong answers were perfectly uniform, voting would
still help, but real wrong answers cluster around a couple of common
misconceptions, and debate has to contend with that.
"""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class Agent:
    name: str
    accuracy: float          # probability of answering correctly, independent per question
    seed: int

    def __post_init__(self) -> None:
        if not 0.0 <= self.accuracy <= 1.0:
            raise ValueError("accuracy must be in [0, 1]")
        self._rng = random.Random(self.seed)

    def answer(self, correct: str, distractors: list[str]) -> str:
        """Independently answer one question."""
        if self._rng.random() < self.accuracy:
            return correct
        if not distractors:
            return correct
        return self._rng.choice(distractors)

    def revise(self, own_answer: str, others_answers: list[str], correct: str,
               distractors: list[str], persuasion: float = 0.6) -> str:
        """Revise an answer after seeing what the other agents said.

        If a clear plurality of the other agents disagrees with this agent, it
        switches to that plurality answer with probability ``persuasion``. This
        models an agent being swayed by group consensus, not by re-deriving the
        answer from scratch. If there is no clear plurality (a tie, or everyone
        already agrees), the agent keeps its own answer.
        """
        if not others_answers:
            return own_answer
        counts: dict[str, int] = {}
        for a in others_answers:
            counts[a] = counts.get(a, 0) + 1
        best_answer, best_count = max(counts.items(), key=lambda kv: kv[1])
        # only sway if the plurality answer differs from this agent's own,
        # and it is not just a coin-flip tie with the agent's own answer
        own_count = counts.get(own_answer, 0)
        if best_answer != own_answer and best_count > own_count:
            if self._rng.random() < persuasion:
                return best_answer
        return own_answer
