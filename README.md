#  Auto Book Publisher — Rule-Based RL Agentic Pipeline

## Overview
A locally executable, modular book processing pipeline that:
-  Scrape and extract public domain chapters
-  Rewrite text using handcrafted linguistic rules
-  Optimize output through MCTS-based reward assessment
-  Enable voice input and text-to-speech interaction
-  Enable exploratory data analysis (EDA) utilities

---

###  Demo
 [Watch Demo](https://drive.google.com/file/d/1DI2eMp8xOh0m-vu4wUQHgFmgXJjzThXE/view?usp=sharing)

---

###   Features

- ✅ Chapter scraping through Playwright + BeautifulSoup
- ✅ Sentence rewriting based on rules (simplification, synonym substitution, adverb elimination)
- ✅ Monte Carlo Tree Search (MCTS) for choosing output
- ✅ Readability + grammar + reward scoring based on feedback
- ✅ Voice input (speech-to-text) and output (text-to-speech)
- ✅ CLI-based interface for modular operation
- ✅ Generation of EDA report for readability and grammar measures

---

##  Project Structure

```

auto_book_pub/
├── main.py                 # CLI controller for scraping, pipeline, EDA, voice
├── scraper.py              # Web scraping logic
├── agentic_pipeline.py     # Full MCTS reward-based agentic pipeline
├── eda.py                  # Exploratory Data Analysis for text quality
├── voice/
│   ├── voice_input.py      # Speech-to-text functionality
│   └── voice_output.py      # Text-to-speech functionality
├── agents/
│   └── write_rules.py    # Rule-based sentence rewriting methods
├── rl/
│   ├── integrate_rl.py 
│   └── reward_mcts.py           # Reward scoring function used in MCTS
├──version_exports/
│   ├── chapter_1_final.json       # Raw scraped chapter
│   ├── chapter_1_reviewer.json
│   ├── chapter_1_rL_final.json
│   ├── chapter_1_writer.json    # Final selected rewrite
│   └── versions.json      # Generated EDA report
├── human_edits/
│   └── feedback.json
├──chapter_1_variants.txt
├──chapter_1.png
├──chapter_1.txt
├── eda_pos_tags.png
├── eda_sentence_lengths.png
├── eda_word_frequencies.png   # Human feedback for reward shaping
└── requirements.txt        # Python dependencies
```

---

##  Quick Start

```bash
# Step 1: Install virtual environment
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate

# Step 2: Install all dependencies
pip install -r requirements.txt

# Step 3: Run from command line
python main.py
```

---

##  Pipeline Stages

### 1. Scraping
- Source: Wikisource
- Tools: Playwright (headless browser), BeautifulSoup (HTML parser)
- Output: Clean `.txt` file and screenshot image

### 2. Rule-Based Rewriting
- Techniques:
  - Sentence simplification
  - Adverb/article removal
  - Synonym replacement
  - Sentence order shuffling
- Output: Multiple rewritten candidates

### 3. MCTS Reward Optimization
- Search: Monte Carlo Tree Search (depth-limited)
- Reward Components:
  - Readability (Flesch Reading Ease)
  - Grammar score (LanguageTool)
- Token overlap similarity
- Word uniqueness
- Human feedback alignment

### 4. Voice Interaction
- Speech-to-text: `speech_recognition` (Mic input)
- Text-to-speech: `pyttsx3` (Offline TTS)
- Integration: Interactive input and spoken output of final draft

### 5. EDA & Reporting
- Metrics:
  - Sentence count
  - Readability score
  - Grammar error count
  - Word distribution
- Output: `eda_report.txt` with human-readable stats

--- 

##  Reward Function Weights

| Metric         | Source               | Impact  |
|----------------|----------------------|---------|
| Readability    | textstat (Flesch)    | ↑ Positive |
| Grammar Score  | language_tool_python | ↓ Penalize |
| Similarity     | Cosine Word Overlap  | Balanced |
| Uniqueness     | Token Set Distance   | ↑ Positive |
| Feedback Match | JSON Heuristic Match | ↑ Positive |

---

##  CLI Options

```
???? Automated Book Publication Workflow - CLI

1. ???? Scrape Chapter from Wikisource
2. ???? Run Full Agentic Pipeline
3. ???? Perform EDA on Chapter
4. ???? Test Voice Input
5. ❌ Exit
```

---

##  Requirements

```txt
playwright
beautifulsoup4
textstat
language_tool_python
speechrecognition
pyttsx3
nltk
```

---

## Future Improvements

- Sentence-level feedback visualization
- Parallel MCTS rollouts for faster convergence  
- GUI frontend for agent interaction  

---

##Author

- **Name**:Siddhi Patil 
- **Email**: siddhipatil64@gmail.com 
   

---
