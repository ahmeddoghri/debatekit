"""debatekit: get a group of noisy agents to a better answer than any one of them.

Ask one model a hard question and you get one shot at the truth, with whatever
bias and blind spots that one model carries. The multiagent debate idea (Du et
al., 2023) is that if you ask several independent agents, show each of them
what the others answered, and let them revise, the group converges on a better
answer than any individual one, the same reason a jury usually beats a single
juror.

This package simulates that process without calling a real model. Each agent is
a noisy classifier with its own error profile; debate is implemented as rounds
of exposure to the group's current answers followed by revision, weighted
toward the consensus. It ships a benchmark comparing single-agent accuracy,
first-round majority vote, and full multi-round debate on a labeled question
set, so you can see exactly how much debate buys you and where it stops paying
off.
"""
from debatekit.agents import Agent
from debatekit.debate import DebateResult, run_debate

__all__ = ["Agent", "run_debate", "DebateResult"]

__version__ = "0.1.0"
