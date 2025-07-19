import random
import copy
import json
import re
import language_tool_python
from textstat import flesch_reading_ease
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
import nltk

# Ensure NLTK uses the correct data path
nltk.data.path.append("C:/Users/ACER/AppData/Roaming/nltk_data")

# Optional: Reproducibility
random.seed(42)

# === LOAD HUMAN FEEDBACK ===
try:
    with open("human_edits/chapter_1_feedback.json", "r", encoding="utf-8") as f:
        feedback_data = json.load(f)
        feedback = feedback_data.get("feedback", [])
except FileNotFoundError:
    feedback = []

# === RULE-BASED REWRITING ===

def simplify_sentence(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    simplified = []
    for s in sentences:
        words = s.split()
        if len(words) > 25:
            midpoint = len(words) // 2
            s1 = ' '.join(words[:midpoint]) + '.'
            s2 = ' '.join(words[midpoint:]) + '.'
            simplified.extend([s1, s2])
        else:
            simplified.append(s)
    return ' '.join(simplified)

def remove_adverbs(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    filtered = [word for word, tag in tagged if tag != 'RB']
    return ' '.join(filtered)

def remove_fillers(text):
    fillers = ['just', 'really', 'very', 'actually', 'basically', 'quite', 'perhaps']
    pattern = r'\b(' + '|'.join(fillers) + r')\b'
    return re.sub(pattern, '', text, flags=re.IGNORECASE)

def remove_articles(text):
    return re.sub(r'\b(the|a|an)\b', '', text, flags=re.IGNORECASE)

def replace_synonyms(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    new_words = []

    for word, tag in tagged:
        if tag.startswith(('NN', 'VB', 'JJ')):
            syns = wordnet.synsets(word)
            if syns:
                lemma_names = syns[0].lemma_names()
                if lemma_names and lemma_names[0].lower() != word.lower():
                    new_words.append(lemma_names[0].replace('_', ' '))
                    continue
        new_words.append(word)

    return ' '.join(new_words)

def shuffle_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    random.shuffle(sentences)
    return ' '.join(sentences)

def rewrite_text(text):
    if random.random() < 0.7:
        text = simplify_sentence(text)
    if random.random() < 0.5:
        text = remove_adverbs(text)
    if random.random() < 0.4:
        text = remove_fillers(text)
    if random.random() < 0.3:
        text = remove_articles(text)
    if random.random() < 0.3:
        text = replace_synonyms(text)
    if random.random() < 0.2:
        text = shuffle_sentences(text)
    return text.strip()

def generate_paraphrases(text, num_return_sequences=3):
    return [rewrite_text(text) for _ in range(num_return_sequences)]

# === REWARD FUNCTION ===

tool = language_tool_python.LanguageTool('en-US')

def evaluate(text, original_text):
    try:
        readability = flesch_reading_ease(text) / 100
        orig_readability = flesch_reading_ease(original_text) / 100
        delta = readability - orig_readability

        orig_words = set(original_text.lower().split())
        new_words = set(text.lower().split())
        common_ratio = len(orig_words & new_words) / max(1, len(orig_words))

        grammar_errors = len(tool.check(text))
        grammar_score = 1 - min(grammar_errors / 10, 1)

        words = text.split()
        unique_ratio = len(set(words)) / len(words) if words else 0

        tone_bonus = 0
        if "!" in text: tone_bonus += 0.05
        if "?" in text: tone_bonus += 0.05

        feedback_bonus = 0
        if any("verbose" in f.lower() for f in feedback):
            feedback_bonus += 0.1
        if any("tone" in f.lower() for f in feedback):
            feedback_bonus += 0.05

        reward = 0.4 + delta + grammar_score * 0.2 + unique_ratio * 0.2 + tone_bonus + feedback_bonus
        reward = max(0, min(1, reward))

        print(f"🧪 Reward: {reward:.4f} [ΔRead: {delta:.2f}, Sim: {common_ratio:.2f}, Grammar: {grammar_score:.2f}, Unique: {unique_ratio:.2f}]")
        return reward

    except Exception as e:
        print(f"⚠️ Evaluation error: {e}")
        return 0

# === MCTS ALGORITHM ===

class MCTSNode:
    def __init__(self, text, parent=None):
        self.text = text
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0

    def is_leaf(self):
        return len(self.children) == 0

    def expand(self):
        variations = generate_paraphrases(self.text)
        for var in variations:
            self.children.append(MCTSNode(var, parent=self))

    def best_child(self, c=1.4):
        if not self.children:
            return self
        return max(
            self.children,
            key=lambda child: (child.reward / max(1, child.visits)) +
                              c * ((2 * (self.visits + 1)) / max(1, child.visits)) ** 0.5
        )

def mcts_search(root_text, iterations=50):
    root = MCTSNode(root_text)
    for _ in range(iterations):
        node = root
        while not node.is_leaf():
            node = node.best_child()
        node.expand()
        for child in node.children:
            reward = evaluate(child.text, root.text)
            backpropagate(child, reward)
    best = root.best_child()
    print(f"🏆 Final Choice: Reward={best.reward:.4f}, Visits={best.visits}")
    return best.text

def backpropagate(node, reward):
    while node:
        node.visits += 1
        node.reward += reward
        node = node.parent