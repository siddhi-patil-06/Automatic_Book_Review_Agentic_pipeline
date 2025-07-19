from datetime import datetime
import json
import os

# Store versions in a JSON file
VERSIONS_FILE = "version_exports/versions.json"

def store_version(doc_id, content, step="writer", agent="human_pipeline"):
    timestamp = datetime.now().isoformat()
    metadata = {
        "step": step,
        "agent": agent,
        "timestamp": timestamp
    }

    data = {
        "id": doc_id,
        "metadata": metadata,
        "content": content
    }

    os.makedirs("version_exports", exist_ok=True)
    with open(f"version_exports/{doc_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Append to a global versions file
    if os.path.exists(VERSIONS_FILE):
        with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
            versions = json.load(f)
    else:
        versions = []

    versions.append(data)
    with open(VERSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(versions, f, indent=2)

    print(f"✅ Stored and exported version: {doc_id} [{step}]")

def search_versions(query_text):
    # Simple keyword-based search
    if not os.path.exists(VERSIONS_FILE):
        return []

    with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
        versions = json.load(f)

    results = []
    for v in versions:
        if query_text.lower() in v["content"].lower():
            results.append(v)
    return results[:3]

def rank_with_rl_stub(query_text, documents):
    # Very basic RL-style scorer
    scored_docs = [(doc, doc.lower().count(query_text.lower())) for doc in documents]
    ranked = sorted(scored_docs, key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked]