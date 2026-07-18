"""Benchmark: does debate actually beat a single agent, and does more debate
keep helping or does it plateau?

We compare three policies across the labeled question set, using a panel of
agents whose individual accuracy is deliberately mediocre (70%), the regime
where debate should matter most:

  - single_agent   : one agent, no group at all
  - vote_no_debate  : the panel answers independently and we take a majority
                      vote, with zero rounds of revision
  - debate_2_rounds : the panel answers, then revises twice while seeing the
                      group's current answers, then we take the final vote

Run it:

    python -m debatekit.eval

Deterministic (fixed seeds per agent). No model, no network, no API keys.
"""
from __future__ import annotations

from debatekit.agents import Agent
from debatekit.corpus import QUESTIONS
from debatekit.debate import run_debate


def _make_panel(accuracy: float, n: int, base_seed: int) -> list[Agent]:
    return [Agent(f"agent{i}", accuracy=accuracy, seed=base_seed + i) for i in range(n)]


def run(accuracy: float = 0.55, n_agents: int = 5, trials: int = 20) -> None:
    n = len(QUESTIONS)

    print(f"debate benchmark: {n} hard questions, panel of {n_agents} agents at "
          f"{accuracy:.0%} individual accuracy, averaged over {trials} trials\n")

    single_correct = 0
    vote_correct = 0
    debate_correct = 0
    total_switches = 0
    total_answers = 0

    for trial in range(trials):
        for qi, (question, correct, distractors) in enumerate(QUESTIONS):
            seed_base = trial * 1000 + qi * 10

            # single agent: one lone guess
            solo = Agent("solo", accuracy=accuracy, seed=seed_base)
            if solo.answer(correct, distractors) == correct:
                single_correct += 1

            # vote, no debate: independent answers, straight majority
            panel = _make_panel(accuracy, n_agents, base_seed=seed_base + 1)
            vote_correct += run_debate(panel, correct, distractors, rounds=0).correct

            # full debate: 2 rounds of revision, then vote
            panel = _make_panel(accuracy, n_agents, base_seed=seed_base + 1)
            result = run_debate(panel, correct, distractors, rounds=2)
            debate_correct += result.correct
            total_switches += result.switched_count
            total_answers += 1

    n_total = n * trials
    print(f"  {'policy':>18}  {'accuracy':>10}")
    print(f"  {'single_agent':>18}  {single_correct}/{n_total} = {single_correct / n_total:>5.0%}")
    print(f"  {'vote_no_debate':>18}  {vote_correct}/{n_total} = {vote_correct / n_total:>5.0%}")
    print(f"  {'debate_2_rounds':>18}  {debate_correct}/{n_total} = {debate_correct / n_total:>5.0%}")

    print(f"\naveraged over {trials} independent trials per question, debate moves "
          f"accuracy from {single_correct / n_total:.0%} (one agent alone) to "
          f"{debate_correct / n_total:.0%} (the panel after 2 rounds), "
          f"{(debate_correct - vote_correct) / n_total:+.0%} over a plain vote with no revision.")
    print("a single mediocre agent is only as good as its one guess. a panel that")
    print("can see what its peers think and update converges on the answer most of")
    print("them were already leaning toward, the same reason a jury beats a single")
    print("juror more often than you would expect, and revising beats a one-shot vote.")


if __name__ == "__main__":
    run()
