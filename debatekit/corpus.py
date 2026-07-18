"""A set of hard questions, each with the correct answer and plausible
distractors, the kind of question where a single model is right more often
than not but wrong often enough to matter.

The distractors matter as much as the correct answer. A benchmark where wrong
answers are uniformly random makes voting trivially easy. Real wrong answers
cluster around a couple of common misconceptions, which is what makes the
group dynamic during debate actually interesting to simulate.
"""
from __future__ import annotations

# (question, correct_answer, distractors)
QUESTIONS: list[tuple[str, str, list[str]]] = [
    ("what year did the Berlin Wall fall", "1989", ["1991", "1987", "1990"]),
    ("who wrote The Origin of Species", "Darwin", ["Wallace", "Huxley", "Lamarck"]),
    ("what is the atomic number of gold", "79", ["78", "80", "47"]),
    ("what is the tallest mountain in Africa", "Kilimanjaro", ["Kenya", "Meru", "Atlas"]),
    ("who developed the theory of general relativity", "Einstein", ["Newton", "Bohr", "Planck"]),
    ("what is the capital of Australia", "Canberra", ["Sydney", "Melbourne", "Perth"]),
    ("what year was the transistor invented", "1947", ["1954", "1945", "1950"]),
    ("what is the smallest prime number", "2", ["1", "3", "0"]),
    ("who painted the Sistine Chapel ceiling", "Michelangelo", ["Raphael", "Da Vinci", "Donatello"]),
    ("what gas do plants absorb for photosynthesis", "carbon dioxide", ["oxygen", "nitrogen", "hydrogen"]),
    ("what is the longest river in the world", "Nile", ["Amazon", "Yangtze", "Mississippi"]),
    ("what year did World War 2 end", "1945", ["1944", "1946", "1943"]),
]
