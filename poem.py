import random
import re
from pathlib import Path

def clean_text(text):
    # lowercase
    text = text.lower()
    # remove punctuation/special chars, keep word chars and whitespace
    text = re.sub(r"[^\w\s]", "", text)
    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def load_corpus(path):
    text = Path(path).read_text(encoding="utf-8")
    # Basic cleanup: lowercase, remove punctuation, normalize spaces
    text = clean_text(text)
    return text

def build_bigram_model(text):
    words = text.split()
    model = {}

    for w1, w2 in zip(words, words[1:]):
        model.setdefault(w1, []).append(w2)

    return model

def generate_poem(model, num_words=80, line_length=7, start_word=None):
    # Choose a start word if not given or invalid
    if not start_word or start_word not in model:
        start_word = random.choice(list(model.keys()))

    word = start_word
    output_words = [word]

    for _ in range(num_words - 1):
        choices = model.get(word)
        if not choices:
            # restart from a random word if stuck
            word = random.choice(list(model.keys()))
            output_words.append("\n")  # force a line break
            output_words.append(word)
            continue

        word = random.choice(choices)
        output_words.append(word)

    # Insert line breaks every N words
    lines = []
    line = []
    for i, w in enumerate(output_words, 1):
        if w == "\n":
            if line:
                lines.append(" ".join(line))
                line = []
            continue
        line.append(w)
        if i % line_length == 0:
            lines.append(" ".join(line))
            line = []
    if line:
        lines.append(" ".join(line))

    return "\n".join(lines)

if __name__ == "__main__":
    # 1) Point this to a text file containing your training poems
    corpus_path = "poems.txt"
    text = load_corpus(corpus_path)

    # 2) Build model
    model = build_bigram_model(text)

    # 3) Generate and print a poem
    poem = generate_poem(model, num_words=80, line_length=6)
    print(poem)
