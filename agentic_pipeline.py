import json
from time import time
import nltk

# Ensure NLTK uses custom download path
nltk.data.path.append("C:/Users/ACER/AppData/Roaming/nltk_data")

# === Import rule-based modules ===
from agents.writer_rules import rewrite_passage, review_passage
from versions.version_store import store_version
from rl.integrate_rl import rl_improved_text
from voice.voice_output import speak_text


class RuleBasedWriterAgent:
    def process(self, text):
        print("\n✍️ Rule-Based Writer processing...")
        output = rewrite_passage(text)
        store_version("chapter_1_writer", output, step="writer")
        speak_text("Writer step complete.")
        return output


class RuleBasedReviewerAgent:
    def process(self, text):
        print("\n📋 Rule-Based Reviewer generating feedback...")
        feedback = review_passage(text)
        store_version("chapter_1_reviewer", feedback, step="reviewer")
        speak_text("Reviewer feedback complete.")
        return feedback


class RLAgent:
    def process(self, text, iterations=20):
        print("\n🧠 RL Agent applying MCTS reward model...")
        improved = rl_improved_text(text, iterations=iterations, export_variants=True)
        store_version("chapter_1_rl_final", improved, step="rl_agent")
        speak_text("RL reward applied.")
        return improved


class HumanEditorAgent:
    def process(self, text):
        print("\n🧑 Human Editor applying final manual edits...")

        final_output = text  # fallback if edited file not found
        try:
            with open("human_edits/chapter_1_edited_by_human.md", "r", encoding="utf-8") as f:
                final_output = f.read()
            store_version("chapter_1_final", final_output, step="human_editor")
            speak_text("Final human edits applied.")
        except FileNotFoundError:
            print("⚠️ Human edited file not found. Using previous version.")

        try:
            with open("human_edits/chapter_1_feedback.json", "r", encoding="utf-8") as f:
                feedback = json.load(f)
                print(f"📝 Feedback loaded ({len(feedback.get('feedback', []))} notes):")
                for note in feedback.get("feedback", []):
                    print("   -", note)
        except FileNotFoundError:
            print("⚠️ Feedback file not found. Skipping RL notes.")

        return final_output


def run_pipeline():
    print("📥 Loading initial chapter...")
    try:
        with open("chapter_1.txt", "r", encoding="utf-8") as f:
            raw_text = f.read()
    except FileNotFoundError:
        print("❌ chapter_1.txt not found. Please ensure the file exists.")
        return

    # Initialize agents
    writer = RuleBasedWriterAgent()
    reviewer = RuleBasedReviewerAgent()
    rl_agent = RLAgent()
    editor = HumanEditorAgent()

    start = time()
    x = writer.process(raw_text)
    y = reviewer.process(x)
    z = rl_agent.process(y, iterations=20)
    final = editor.process(z)
    end = time()

    print(f"\n✅ Agentic pipeline complete in {round(end - start, 2)} seconds.")


if __name__ == "__main__":
    run_pipeline()
