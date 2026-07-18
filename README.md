# 🗣️ debatekit

**Get a group of noisy agents to a better answer than any one of them.**

![CI](https://github.com/ahmeddoghri/debatekit/actions/workflows/ci.yml/badge.svg)
![tests](https://img.shields.io/badge/tests-10%20passing-brightgreen)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![deps](https://img.shields.io/badge/runtime%20deps-none-success)
![license](https://img.shields.io/badge/license-MIT-black)

> **A single agent at 55% accuracy gets there 57% of the time. A panel of five
> that debates for two rounds hits 80%.** Same underlying skill level, just
> more voices and a chance to reconsider: `python -m debatekit.eval`.

Ask one model a hard question and you get one shot at the truth, plus whatever
blind spot that particular model happens to carry that day. The multiagent
debate idea (Du et al., 2023) is the same fix humans figured out a long time
ago: a jury usually beats a single juror, not because any one juror is smarter,
but because bad independent guesses rarely agree with each other while good
ones converge, and a room full of people who can hear each other's reasoning
tends to end up closer to right.

debatekit simulates that dynamic without a real model. Each agent is a noisy
classifier with its own accuracy; debate is rounds of "see what the group
currently thinks, maybe update toward it" followed by a final vote. It ships a
benchmark comparing a lone agent, a one-shot majority vote with no revision,
and full multi-round debate, so the value of each layer is a number, not a
hunch.

---

## The result in one command

```bash
python -m debatekit.eval
```
```
debate benchmark: 12 hard questions, panel of 5 agents at 55% individual accuracy, averaged over 20 trials

              policy    accuracy
        single_agent  137/240 =   57%
      vote_no_debate  190/240 =   79%
     debate_2_rounds  193/240 =   80%
```

Twenty trials per question, so the numbers are stable, not one lucky run. The
big jump is going from one agent to a panel at all: 57% to 79%, just from
independent votes with zero communication, which is the classic wisdom-of-
crowds effect. Letting the panel see each other's answers and revise for two
rounds buys another point on top of that. Neither number is inflated; the
distractors in the question set are plausible wrong answers, not random noise,
so voting has to do real work to converge on the truth.

## Install

```bash
git clone https://github.com/ahmeddoghri/debatekit
cd debatekit && pip install -e .
python examples/quickstart.py
```

## Use it

```python
from debatekit.agents import Agent
from debatekit.debate import run_debate

panel = [Agent(f"agent{i}", accuracy=0.55, seed=i) for i in range(5)]

result = run_debate(panel, correct="1989", distractors=["1991", "1987", "1990"], rounds=2)

print(result.final_answer)      # "1989"
print(result.correct)           # True
print(result.rounds)            # every agent's answer, round by round
print(result.switched_count)    # how many agents changed their mind during debate
```

## How debate actually works here

```
round 0: each agent answers independently, no communication
round 1..R: each agent sees every OTHER agent's current answer
            if a clear plurality disagrees with this agent, it may switch
            (probability = persuasion, default 0.6, so agents are swayed
            but not blindly obedient)
final: majority vote over the last round's answers
```

The persuasion parameter is the interesting knob. Turn it to 1.0 and the panel
converges instantly to whatever the first-round plurality happened to be,
which can lock in a wrong answer just as fast as a right one. Turn it to 0.0
and debate does nothing, it is just an expensive way to run a vote. The
default of 0.6 models agents that take the group seriously without being
pushovers, which is closer to how a real multiagent debate protocol behaves.

## Tests

```bash
pip install pytest && pytest -q      # 10 passing
```

## License

MIT © Ahmed Doghri
