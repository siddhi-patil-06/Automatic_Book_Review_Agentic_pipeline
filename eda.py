# eda.py
import matplotlib.pyplot as plt
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
import os

# Set your NLTK data path (adjust as needed)
nltk.data.path.append("C:/Users/ACER/AppData/Roaming/nltk_data")

def load_text(filepath="chapter_1.txt"):
    if not os.path.exists(filepath):
        print("❌ Text file not found.")
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def plot_sentence_lengths(text):
    sentences = sent_tokenize(text)
    lengths = [len(word_tokenize(sent)) for sent in sentences]

    plt.figure(figsize=(8, 4))
    plt.hist(lengths, bins=20, color='skyblue', edgecolor='black')
    plt.title("Sentence Length Distribution")
    plt.xlabel("Words per sentence")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("eda_sentence_lengths.png")
    print("📊 Saved: eda_sentence_lengths.png")

def plot_word_frequencies(text, top_n=20):
    words = [w.lower() for w in word_tokenize(text) if w.isalpha()]
    freq = Counter(words).most_common(top_n)

    labels, counts = zip(*freq)
    plt.figure(figsize=(10, 4))
    plt.bar(labels, counts, color='salmon')
    plt.title(f"Top {top_n} Word Frequencies")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("eda_word_frequencies.png")
    print("📊 Saved: eda_word_frequencies.png")

def plot_pos_distribution(text):
    tokens = word_tokenize(text)
    tags = [tag for _, tag in pos_tag(tokens)]
    tag_counts = Counter(tags)

    labels, values = zip(*tag_counts.items())
    plt.figure(figsize=(12, 4))
    plt.bar(labels, values, color='lightgreen')
    plt.title("POS Tag Distribution")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("eda_pos_tags.png")
    print("📊 Saved: eda_pos_tags.png")

def run_eda():
    text = load_text()
    if not text:
        return

    print("🔍 Running EDA on chapter_1.txt...")
    plot_sentence_lengths(text)
    plot_word_frequencies(text)
    plot_pos_distribution(text)
    print("✅ EDA complete.")

if __name__ == "__main__":
    run_eda()
