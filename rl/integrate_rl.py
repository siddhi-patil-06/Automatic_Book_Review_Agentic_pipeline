from rl.reward_mcts import mcts_search

def rl_improved_text(text, iterations=15, export_variants=False, verbose=True):
    if verbose:
        print("🚀 Improving text using MCTS-based RL reward...")

    improved_text = mcts_search(text, iterations=iterations)

    if export_variants:
        filename = "chapter_1_variants.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(improved_text + "\n")
        if verbose:
            print(f"📄 Exported improved variant to {filename}")

    return improved_text