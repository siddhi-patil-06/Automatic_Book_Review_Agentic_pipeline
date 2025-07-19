import os
from agentic_pipeline import run_pipeline
from voice.voice_input import get_voice_input


def run_scraper():
    print("\n🔍 Running scraper...")
    try:
        os.system("python scraper.py")
    except Exception as e:
        print("❌ Scraper failed:", e)


def run_eda():
    print("\n📊 Running EDA...")
    try:
        os.system("python eda.py")
    except Exception as e:
        print("❌ EDA failed:", e)


def run_pipeline_from_cli():
    print("\n🚀 Running Agentic Pipeline...")
    try:
        run_pipeline()
    except Exception as e:
        print("❌ Pipeline encountered an error:", e)


def test_voice_input():
    print("\n🎤 Listening for input... (speak clearly)")
    try:
        voice_text = get_voice_input()
        print("🔊 Recognized voice input:", voice_text)
    except Exception as e:
        print("❌ Voice recognition failed:", e)


def main_menu():
    while True:
        print("\n📘 Automated Book Publication Workflow - CLI")
        print("1. 📥 Scrape Chapter from Wikisource")
        print("2. 🧠 Run Full Agentic Pipeline")
        print("3. 📊 Perform EDA on Chapter")
        print("4. 🎤 Test Voice Input")
        print("5. ❌ Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            run_scraper()
        elif choice == '2':
            run_pipeline_from_cli()
        elif choice == '3':
            run_eda()
        elif choice == '4':
            test_voice_input()
        elif choice == '5':
            print("👋 Exiting. Thank you!")
            break
        else:
            print("⚠️ Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main_menu()
