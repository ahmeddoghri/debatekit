"""Tests for the statistical-power finding: does "+1pt from debate" survive
more than the published 20 trials?"""

from __future__ import annotations

from debatekit.agents import Agent
from debatekit.corpus import QUESTIONS
from debatekit.debate import run_debate
from debatekit.eval_v2 import _measure, build_report, instability_windows

# --- the finding: the published 20-trial delta is not reproducible ---------

def test_published_headline_reproduces_at_20_trials():
    """The exact numbers in the README/eval output: single=137/240,
    vote=190/240, debate=193/240 at accuracy=0.55, trials=20."""
    accuracy, n_agents, trials = 0.55, 5, 20
    single_correct = vote_correct = debate_correct = 0
    for trial in range(trials):
        for qi, (_, correct, distractors) in enumerate(QUESTIONS):
            seed_base = trial * 1000 + qi * 10
            solo = Agent("solo", accuracy=accuracy, seed=seed_base)
            single_correct += solo.answer(correct, distractors) == correct
            panel = [Agent(f"agent{i}", accuracy=accuracy, seed=seed_base + 1 + i) for i in range(n_agents)]
            vote_correct += run_debate(panel, correct, distractors, rounds=0).correct
            panel2 = [Agent(f"agent{i}", accuracy=accuracy, seed=seed_base + 1 + i) for i in range(n_agents)]
            debate_correct += run_debate(panel2, correct, distractors, rounds=2).correct
    assert (single_correct, vote_correct, debate_correct) == (137, 190, 193)


def test_the_reported_delta_swings_across_equally_valid_20_trial_windows():
    """The published +1.3pt is one draw from a spread that includes
    negative deltas of comparable or larger magnitude."""
    windows = instability_windows(accuracy=0.55, window=20, n_windows=10)
    assert windows[0] == 1.25  # the exact published-benchmark window
    assert any(w < 0 for w in windows)
    assert max(windows) - min(windows) > 3.0  # a swing bigger than the claimed effect


# --- the fix: measure with enough trials, and report significance ---------

def test_large_sample_delta_is_not_statistically_significant():
    for accuracy in (0.45, 0.55):
        result = _measure(accuracy, trials=500)
        assert not result["significant"]
        assert abs(result["delta_points"]) < 2 * result["se_points"]


def test_standard_error_shrinks_with_more_trials():
    small = _measure(0.55, trials=20)
    large = _measure(0.55, trials=500)
    assert large["se_points"] < small["se_points"]


def test_single_agent_to_panel_vote_effect_is_large_and_real():
    """The one genuinely large, non-noise effect: independent voting alone
    massively beats a lone agent. This is not in question and should stay
    a clean, big number regardless of the debate-rounds finding."""
    accuracy, n_agents = 0.55, 5
    trials = 200
    single_c = vote_c = 0
    n_total = trials * len(QUESTIONS)
    for trial in range(trials):
        for qi, (_, correct, distractors) in enumerate(QUESTIONS):
            seed_base = trial * 1000 + qi * 10
            solo = Agent("solo", accuracy=accuracy, seed=seed_base)
            single_c += solo.answer(correct, distractors) == correct
            panel = [Agent(f"agent{i}", accuracy=accuracy, seed=seed_base + 1 + i) for i in range(n_agents)]
            vote_c += run_debate(panel, correct, distractors, rounds=0).correct
    assert (vote_c - single_c) / n_total > 0.15  # a 15+ point jump, not noise


# --- the original module is untouched ---------------------------------------

def test_original_debate_module_untouched():
    import debatekit.debate as debate_module

    assert not hasattr(debate_module, "run_debate_v2")


def test_original_eval_still_reproduces_the_published_table():
    """python -m debatekit.eval must still print the exact numbers this
    project's README quotes, even though eval_v2 shows they're noisy."""
    accuracy, n_agents, trials = 0.55, 5, 20
    n_total = trials * len(QUESTIONS)
    single_c = vote_c = debate_c = 0
    for trial in range(trials):
        for qi, (_, correct, distractors) in enumerate(QUESTIONS):
            seed_base = trial * 1000 + qi * 10
            solo = Agent("solo", accuracy=accuracy, seed=seed_base)
            single_c += solo.answer(correct, distractors) == correct
            panel = [Agent(f"agent{i}", accuracy=accuracy, seed=seed_base + 1 + i) for i in range(n_agents)]
            vote_c += run_debate(panel, correct, distractors, rounds=0).correct
            panel2 = [Agent(f"agent{i}", accuracy=accuracy, seed=seed_base + 1 + i) for i in range(n_agents)]
            debate_c += run_debate(panel2, correct, distractors, rounds=2).correct
    assert round(single_c / n_total, 2) == 0.57
    assert round(vote_c / n_total, 2) == 0.79
    assert round(debate_c / n_total, 2) == 0.80


# --- the full report ---------------------------------------------------------

def test_report_is_reproducible():
    a = build_report(trials=100)
    b = build_report(trials=100)
    assert a == b


def test_report_covers_the_full_sweep():
    report = build_report(trials=50)
    accuracies = [row["accuracy"] for row in report["sweep"]]
    assert accuracies == [0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
