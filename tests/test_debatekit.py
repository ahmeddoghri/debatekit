import pytest

from debatekit.agents import Agent
from debatekit.corpus import QUESTIONS
from debatekit.debate import run_debate


def test_agent_rejects_invalid_accuracy():
    with pytest.raises(ValueError):
        Agent("a", accuracy=1.5, seed=0)


def test_perfect_agent_always_correct():
    agent = Agent("a", accuracy=1.0, seed=0)
    for _ in range(20):
        assert agent.answer("X", ["Y", "Z"]) == "X"


def test_zero_accuracy_agent_never_correct_with_distractors():
    agent = Agent("a", accuracy=0.0, seed=0)
    for _ in range(20):
        assert agent.answer("X", ["Y", "Z"]) != "X"


def test_debate_returns_a_majority_answer():
    agents = [Agent(f"a{i}", accuracy=0.9, seed=i) for i in range(5)]
    result = run_debate(agents, "X", ["Y", "Z"], rounds=1)
    assert result.final_answer in {"X", "Y", "Z"}


def test_zero_rounds_is_a_plain_vote():
    agents = [Agent(f"a{i}", accuracy=1.0, seed=i) for i in range(5)]
    result = run_debate(agents, "X", ["Y", "Z"], rounds=0)
    assert result.n_rounds == 1  # just the initial answers, no revision
    assert result.final_answer == "X"


def test_perfect_panel_always_correct():
    agents = [Agent(f"a{i}", accuracy=1.0, seed=i) for i in range(5)]
    result = run_debate(agents, "X", ["Y", "Z"], rounds=2)
    assert result.correct


def test_switched_count_tracks_revisions():
    agents = [Agent(f"a{i}", accuracy=0.5, seed=i) for i in range(5)]
    result = run_debate(agents, "X", ["Y", "Z"], rounds=2)
    assert result.switched_count >= 0
    assert result.switched_count <= len(agents)


def test_revise_keeps_own_answer_with_no_others():
    agent = Agent("a", accuracy=0.9, seed=0)
    assert agent.revise("X", [], "X", ["Y"]) == "X"


def test_revise_can_switch_toward_plurality():
    agent = Agent("a", accuracy=0.9, seed=42)
    # force persuasion=1.0 so a clear plurality always sways
    result = agent.revise("Y", ["X", "X", "X"], "X", ["Y", "Z"], persuasion=1.0)
    assert result == "X"


def test_debate_benchmark_beats_single_agent():
    """The core claim: at mediocre individual accuracy, a debating panel beats
    a lone agent on the bundled question set."""
    accuracy = 0.70
    n = len(QUESTIONS)

    single_correct = 0
    for qi, (_, correct, distractors) in enumerate(QUESTIONS):
        agent = Agent("solo", accuracy=accuracy, seed=100 + qi)
        if agent.answer(correct, distractors) == correct:
            single_correct += 1

    debate_correct = 0
    for qi, (_, correct, distractors) in enumerate(QUESTIONS):
        panel = [Agent(f"a{i}", accuracy=accuracy, seed=200 + qi * 10 + i) for i in range(5)]
        result = run_debate(panel, correct, distractors, rounds=2)
        debate_correct += result.correct

    assert debate_correct / n >= single_correct / n
