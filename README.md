# 🗣️ debatekit

**Get a group of noisy agents to a better answer than any one of them.**

![CI](https://github.com/ahmeddoghri/debatekit/actions/workflows/ci.yml/badge.svg)
![tests](https://img.shields.io/badge/tests-19%20passing-brightgreen)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![deps](https://img.shields.io/badge/runtime%20deps-none-success)
![license](https://img.shields.io/badge/license-MIT-black)

> **A single agent at 55% accuracy gets there 57% of the time. A panel of five
> that debates for two rounds hits 80%.** Same underlying skill level, just
> more voices and a chance to reconsider: `python -m debatekit.eval`.
>
> **Update:** the panel jump (57%→79%) is real and huge. The extra "+1pt
> from debate" on top of it is not: it's measured over 20 trials, and
> resampling that same 20-trial size across ten equally valid windows
> swings from -3.8pt to +1.3pt. Run it properly (2000+ trials, standard
> errors reported) and the true delta from adding debate rounds never
> once clears one standard error, at any accuracy tested.
> `python -m debatekit.eval_v2`.

Ask one model a hard question and you get one shot at the truth, plus
whatever blind spot that particular model happens to be carrying around that
day like a grudge. The multiagent debate idea (Du et al., 2023) is the same
fix humans figured out a long time ago, we just called it a jury instead of
an ensemble method: a jury usually beats a single juror, not because any one
juror is smarter, but because bad independent guesses rarely agree with each
other while good ones converge, and a room full of people who can hear each
other's reasoning tends to end up closer to right, assuming nobody's just
loud.

debatekit simulates that dynamic without a real model, which is refreshing
in a field where every demo needs an API key before it'll say hello. Each
agent is a noisy classifier with its own accuracy; debate is rounds of "see
what the group currently thinks, maybe update toward it" followed by a final
vote. It ships a benchmark comparing a lone agent, a one-shot majority vote
with no revision, and full multi-round debate, so the value of each layer is
a number, not a hunch someone had after a conference talk.

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

The big jump is going from one agent to a panel at all: 57% to 79%, just from
independent votes with zero communication, which is the classic wisdom-of-
crowds effect, and it's a large, reliable result. The distractors in the
question set are plausible wrong answers, not random noise, so voting has to
do real work to converge on the truth.

The extra point from letting the panel revise for two rounds is a different
story: twenty trials is not actually enough to call that stable. [See below](#twenty-trials-is-not-enough-to-trust-the-debate-rounds-number)
before you take it at face value.

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

The persuasion parameter is the interesting knob, the one that decides
whether your panel is a jury or a mob. Turn it to 1.0 and the panel converges
instantly to whatever the first-round plurality happened to be, which locks
in a wrong answer exactly as fast as a right one, groupthink with extra
steps. Turn it to 0.0 and debate does nothing, it's just an expensive way to
run a vote. The default of 0.6 models agents that take the group seriously
without being pushovers, which is closer to how a real multiagent debate
protocol behaves, and closer to how you'd want an actual jury to behave too.

## Twenty trials is not enough to trust the debate-rounds number

I went back and checked how stable the "+1pt from debate" claim actually
is. Twenty trials per question at 55% accuracy, resampled across ten
different, equally valid 20-trial windows instead of the one the README
happens to quote:

```
+1.2p, +0.8p, -0.4p, +0.0p, +0.4p, -0.4p, +1.2p, +0.0p, -3.8p, -0.8p
```

The published +1.3p is one draw from a spread that swings by more than 5
points and includes deltas well into negative territory. That is not a
stable measurement, it is noise with a headline attached.

```bash
python -m debatekit.eval_v2
```
```
  accuracy      vote    debate     delta      SE    significant?
      0.35     42.3%     42.2%    -0.03p   0.45p              no
      0.40     50.9%     50.8%    -0.03p   0.46p              no
      0.45     59.1%     59.2%    +0.17p   0.45p              no
      0.50     67.3%     67.2%    -0.03p   0.43p              no
      0.55     74.6%     74.6%    -0.02p   0.40p              no
      0.60     81.1%     81.2%    +0.10p   0.36p              no
```

At 2000 trials per point, backed by 12,000-trial checks across the same
range, the delta between a plain independent vote and two rounds of
debate never once clears one standard error, at any accuracy tested. The
honest reading: in this simulation, letting the panel revise for two
rounds after voting does not measurably beat voting alone. The real,
load-bearing effect is the panel itself, one agent to five independent
votes is a 20+ point jump, five to ten times the noise floor, not the
extra debate rounds on top of it.

`debatekit/eval_v2.py` doesn't change `debate.py` or `agents.py` at all;
this isn't a code bug, the simulation does exactly what it says. It's a
sample-size problem in how the headline number was measured. The original
`python -m debatekit.eval` output is untouched and still reproduces the
exact published table; `eval_v2` is the properly-powered companion
measurement, not a replacement.

## Tests

```bash
pip install pytest && pytest -q      # 19 passing
```

## License

MIT © Ahmed Doghri
