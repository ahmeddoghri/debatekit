"""Run a debate: agents answer independently, then revise across rounds while
seeing each other's current answers, and the final round is decided by majority.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from debatekit.agents import Agent


@dataclass
class DebateResult:
    final_answer: str
    rounds: list[list[str]] = field(default_factory=list)   # each agent's answer per round
    correct: bool = False

    @property
    def n_rounds(self) -> int:
        return len(self.rounds)

    @property
    def switched_count(self) -> int:
        """How many agents changed their answer between the first and last round."""
        if len(self.rounds) < 2:
            return 0
        first, last = self.rounds[0], self.rounds[-1]
        return sum(1 for a, b in zip(first, last) if a != b)


def _majority(answers: list[str]) -> str:
    return Counter(answers).most_common(1)[0][0]


def run_debate(agents: list[Agent], correct: str, distractors: list[str],
                rounds: int = 2, persuasion: float = 0.6) -> DebateResult:
    """Run a full debate: independent answers, then ``rounds`` of revision.

    ``rounds`` is the number of revision passes after the initial independent
    answer. rounds=0 is equivalent to a single simultaneous vote with no
    revision (still often better than one agent alone). rounds=1 or 2 is where
    real debate protocols typically converge.
    """
    current = [a.answer(correct, distractors) for a in agents]
    history = [list(current)]

    for _ in range(rounds):
        next_round = []
        for i, agent in enumerate(agents):
            others = [current[j] for j in range(len(agents)) if j != i]
            next_round.append(agent.revise(current[i], others, correct, distractors, persuasion))
        current = next_round
        history.append(list(current))

    final = _majority(current)
    return DebateResult(final_answer=final, rounds=history, correct=(final == correct))
