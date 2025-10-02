"""
typing_speed_test.py
--------------------
A console-based typing speed test game.

Features:
- Displays a random sentence (from sentences.txt if available, else default list).
- Ensures no repeats in a session until all sentences are used.
- Measures typing speed in Words Per Minute (WPM).
- Calculates accuracy using difflib similarity ratio.
- Shows word-level correctness and a character-level diff.

Usage:
    python typing_speed_test.py
"""

import random
import time
import difflib
import os
import textwrap

# Default fallback sentences if sentences.txt not found
DEFAULT_SENTENCES = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing well takes practice and patience.",
    "Generative AI is reshaping how we build software.",
    "Practice makes progress, not perfection.",
    "Always write code that other developers can read.",
    "Small, consistent steps produce big changes over time.",
    "Debugging becomes easier when you isolate the problem.",
    "Clean code is a pleasure to maintain and extend.",
    "Focus on fundamentals first, then learn the tools.",
    "A problem well stated is a problem half solved."
]

# This will store the current shuffled list for the session
_shuffled_sentences = []
_index = 0


def load_sentences(filename="sentences.txt"):
    """Load sentences from a file if it exists, else return defaults."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            sentences = [line.strip() for line in f if line.strip()]
        if sentences:
            return sentences
    return DEFAULT_SENTENCES


def get_next_sentence(sentences):
    """
    Return the next random sentence without repeats in the same session.
    Once all are used, reshuffle and start over.
    """
    global _shuffled_sentences, _index
    if not _shuffled_sentences or _index >= len(_shuffled_sentences):
        _shuffled_sentences = sentences[:]
        random.shuffle(_shuffled_sentences)
        _index = 0
    sentence = _shuffled_sentences[_index]
    _index += 1
    return sentence


def show_instructions():
    """Print game instructions."""
    print("=" * 60)
    print("          Typing Speed Test")
    print("=" * 60)
    print("Instructions:")
    print("1) A sentence will appear.")
    print("2) Press Enter to start typing and then type the sentence.")
    print("3) Press Enter when done to stop the timer.")
    print("Results will show WPM and accuracy.")
    print("-" * 60)


def format_time(seconds):
    """Format elapsed time into human-readable string."""
    if seconds < 60:
        return f"{seconds:.2f} sec"
    minutes = int(seconds // 60)
    sec = seconds % 60
    return f"{minutes} min {sec:.2f} sec"


def compute_wpm(char_count, elapsed_seconds):
    """Compute words per minute (WPM)."""
    minutes = elapsed_seconds / 60 if elapsed_seconds > 0 else 1 / 60
    return (char_count / 5) / minutes


def compute_accuracy(target, typed):
    """Compute typing accuracy (percentage)."""
    matcher = difflib.SequenceMatcher(None, target, typed)
    return matcher.ratio() * 100


def word_stats(target, typed):
    """Return number of correct words vs total and typed words count."""
    t_words = target.split()
    u_words = typed.split()
    correct = sum(1 for tw, uw in zip(t_words, u_words) if tw == uw)
    return correct, len(t_words), len(u_words)


def char_diff(target, typed):
    """Return a readable diff between target and typed input."""
    diff = list(difflib.ndiff(list(target), list(typed)))
    lines = []
    for d in diff:
        sign, ch = d[:2], d[2:]
        if sign == "  ":
            lines.append(ch)
        elif sign == "- ":
            lines.append(f"[-{ch}]")  # missing
        elif sign == "+ ":
            lines.append(f"[+{ch}]")  # extra
    return "".join(lines)


def run_test():
    """Run the typing speed test."""
    show_instructions()
    sentences = load_sentences()
    target = get_next_sentence(sentences)

    print("\nType the following sentence:\n")
    print(textwrap.fill(target, width=70))
    input("\nPress Enter when you're ready to start...")

    print("\nStart typing now and press Enter when finished.")
    start = time.perf_counter()
    typed = input()
    end = time.perf_counter()

    elapsed = end - start
    char_count = len(typed)
    wpm = compute_wpm(char_count, elapsed)
    accuracy = compute_accuracy(target, typed)
    correct_words, total_words, typed_words = word_stats(target, typed)
    diff = char_diff(target, typed)

    print("\n" + "=" * 60)
    print("Results:")
    print(f"Time taken      : {format_time(elapsed)}")
    print(f"Characters typed: {char_count}")
    print(f"Words typed     : {typed_words} (target words: {total_words})")
    print(f"WPM             : {wpm:.2f}")
    print(f"Accuracy        : {accuracy:.2f}%")
    print(f"Correct words   : {correct_words} / {total_words}")
    print("\nTarget sentence:")
    print(textwrap.fill(target, width=70))
    print("\nYour input:")
    print(textwrap.fill(typed, width=70))
    print("\nCharacter-level diff ([-X] missing, [+Y] extra):")
    print(diff)
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_test()
    except KeyboardInterrupt:
        print("\nTest aborted. Goodbye!")
