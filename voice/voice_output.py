import pyttsx3

# You can globally disable voice if needed
ENABLE_VOICE = True

def speak_text(text, tag="Narrator"):
    if not ENABLE_VOICE:
        return

    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 185)
        engine.setProperty('volume', 0.9)

        # Optional: Set voice (0 = male, 1 = female, may vary by OS)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

        speak_line = f"{tag} says: {text}"
        engine.say(speak_line)
        engine.runAndWait()

    except Exception as e:
        print(f"🔇 Voice output failed: {e}")
