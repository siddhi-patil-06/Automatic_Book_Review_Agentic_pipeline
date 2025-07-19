def rewrite_passage(text: str) -> str:
    lines = text.split(".")
    shortened = [line.strip() + "." for line in lines if len(line.split()) < 25]
    return "\n".join(shortened)

def review_passage(text: str) -> str:
    return "\n".join([
        "- Avoid long run-on sentences.",
        "- Keep a consistent narrative tone.",
        "- Use simpler transitions between scenes.",
        "- Watch for repetitive phrasing."
    ])
